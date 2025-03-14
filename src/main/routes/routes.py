from flask import render_template, url_for, request, redirect, Blueprint, send_file
import pandas as pd
import random
import hashlib
from datetime import datetime
import requests
import os

main_bp = Blueprint("main_bp", __name__)
CACHE_DIR = 'cache'

file_path = 'data/PVZ.xlsx'
last_sheet = ''

used_values = [[],[],[],[]]
choosed_names = [[],[],[],[]]

victory = [False, False, False, False]
number_of_trys = [0,0,0,0]

infinity_number = 999

@main_bp.route("/")
@main_bp.route("/index")
def index():
    if last_sheet != 'Database':
        global rand, data
        rand = gerar_numero_aleatorio('Database')
        data = get_data('Database')

    names = data['Name'].tolist()

    return render_template(
        "index.html",
        data = data,
        names = names,
        rows = get_rows(0),
        used_values = used_values[0],
        choosed_names = choosed_names[0],
        rand = rand,
        victory = victory,
        number_of_trys = number_of_trys
        )

@main_bp.route("/chinease")
def chinease():
    if last_sheet != 'Chinese_Database':
        global rand, data
        rand = gerar_numero_aleatorio('Chinese_Database')
        data = get_data('Chinese_Database')

    names = data['Name'].tolist()

    return render_template(
        "chinease_version.html",
        data = data,
        names = names,
        rows = get_rows(1),
        used_values = used_values[1],
        choosed_names = choosed_names[1],
        rand = rand,
        victory = victory,
        number_of_trys = number_of_trys
        )

@main_bp.route("/all")
def all():
    if last_sheet != 'All_data':
        global rand, data
        rand = gerar_numero_aleatorio('All_data')
        data = get_data('All_data')

    names = data['Name'].tolist()

    return render_template(
        "all_mode.html",
        data = data,
        names = names,
        rows = get_rows(2),
        used_values = used_values[2],
        choosed_names = choosed_names[2],
        rand = rand,
        victory = victory,
        number_of_trys = number_of_trys
        )

@main_bp.route("/infinity")
def infinity():
    global rand, data, infinity_number
    if last_sheet != 'Database':
        data = get_data('Database')
    if infinity_number == 999:
        rand = gerar_numero_aleatorio_random('Database')
        infinity_number = rand
    
    print(infinity_number)
    names = data['Name'].tolist()

    return render_template(
        "infinity.html",
        data = data,
        names = names,
        rows = get_rows(9),
        used_values = used_values[len(used_values)-1],
        choosed_names = choosed_names[len(choosed_names)-1],
        rand = rand,
        victory = victory[len(victory)-1]
        )

@main_bp.route("/test")
def testes():
    if last_sheet != 'Database':
        data = get_data('Database')

    global rand
    rand = gerar_numero_aleatorio_random('Database')

    names = data['Name'].tolist()

    return render_template(
        "test.html",
        data = data,
        names = names,
        rows = get_all()
        )

@main_bp.route("/makeguess", methods=["GET","POST"])
def guesser():
    id = int(request.form.get("id"))
    guess = request.form.get('guess')
    item = data[data['Name'].str.lower() == guess.lower()]

    global victory
    used_values[id].append(int(item['ID'].iloc[0]))
    choosed_names[id].append(item['Name'].iloc[0])

    if data['Name'][rand-1] == item['Name'].iloc[0]:
        victory[id] = True
        number_of_trys[id] = used_values[id].__len__()

    if id == 0:
        return redirect(url_for('main_bp.index'))
    elif id ==1:
        return redirect(url_for('main_bp.chinease'))
    elif id ==2:
        return redirect(url_for('main_bp.all'))
    else:
        return redirect(url_for('main_bp.infinity'))
   
@main_bp.route("/reset_infinity")
def reset_infinity():
    global rand
    rand = gerar_numero_aleatorio_random('Database')
    global victory
    used_values[len(victory)-1].clear()
    choosed_names[len(victory)-1].clear()
    victory[len(victory)-1] = False
    return redirect(url_for('main_bp.infinity'))


def gerar_numero_aleatorio(sheet_name):
    global last_sheet
    last_sheet = sheet_name
    # Carregar o arquivo Excel
    data = pd.read_excel(file_path, sheet_name=sheet_name)
    df = data[data['Name'].notna()]  # remove apenas as linhas onde todos os valores são NaN

    # Obter o número de ocorrências (número de linhas no arquivo)
    num_ocorrencias = len(df)

    # Garantir que o número de ocorrências seja no mínimo 1
    if num_ocorrencias < 1:
        raise ValueError("O arquivo não possui dados suficientes.")

    # Usar a data atual como semente para garantir que o número não mude durante o dia
    # Exemplo de cálculo: gerando um número a partir da data
    data_atual = datetime.now().date()
    semente = int(data_atual.strftime("%Y%m%d"))  # Formato YYYYMMDD, ex: 20250219

    # Definir o limite superior como o número de ocorrências
    limite_superior = num_ocorrencias

    # Gerar o número aleatório com base na semente
    random.seed(semente)  # Usando a data como semente
    numero_aleatorio = random.randint(1, limite_superior)

    return numero_aleatorio

def gerar_numero_aleatorio_random(sheet_name):
    global last_sheet
    last_sheet = sheet_name
    # Carregar o arquivo Excel
    data = pd.read_excel(file_path, sheet_name=sheet_name)
    df = data[data['Name'].notna()]  # remove apenas as linhas onde todos os valores são NaN

    # Obter o número de ocorrências (número de linhas no arquivo)
    num_ocorrencias = len(df)

    # Garantir que o número de ocorrências seja no mínimo 1
    if num_ocorrencias < 1:
        raise ValueError("O arquivo não possui dados suficientes.")

    # Definir o limite superior como o número de ocorrências
    limite_superior = num_ocorrencias

    numero_aleatorio = random.randint(1, limite_superior)

    return numero_aleatorio

def get_data(sheet_name):
    global last_sheet
    last_sheet = sheet_name
    data = pd.read_excel(file_path, sheet_name=sheet_name, header=0)
    df = data[data['Name'].notna()]

    return df

def get_rows(version):
    rows = []
    values_to_use = used_values[0] if version == 0 else (used_values[1] if version == 1 else (used_values[2] if version == 2 else used_values[len(used_values)-1]))
    for value in values_to_use:
        row = {
            'name': data['Name'].iloc[value - 1],
            'type': data['Type'].iloc[value - 1],
            'sun_cust': int(data['Sun Cust'].iloc[value - 1]),
            'tought': int(data['Tought'].iloc[value - 1]),
            'damage': int(data['Damage'].iloc[value - 1]),
            'recarga': int(data['Recarga'].iloc[value - 1]),
            'rarity': data['Rarity'].iloc[value - 1],
            'usage': [data['Single use'].iloc[value - 1],data['Instant use'].iloc[value - 1]],
            'plant_origin': data['Plant_Origin'].iloc[value -1],
            'origin': data['Origin'].iloc[value - 1],
            'classification': data['Classification'].iloc[value - 1],
            'appearances': data['Appearances'].iloc[value - 1],
            'background': get_background(data['Appearances'].iloc[value - 1]),
            'img_link': data['img_link'].iloc[value - 1],
        }
        rows.append(row)
    rows.reverse()
    
    return rows

def get_all():
    rows = []
    for index, value in data.iterrows():
        row = {
            'name': value['Name'],
            'type': value['Type'],
            'sun_cust': int(value['Sun Cust']),
            'tought': int(value['Tought']),
            'damage': int(value['Damage']),
            'recarga': int(value['Recarga']),
            'rarity': value['Rarity'],
            'usage': [value['Single use'],value['Instant use']],
            'plant_origin': value['Plant_Origin'],
            'origin': value['Origin'],
            'classification': value['Classification'],
            'appearances': value['Appearances'],
            'background-appearances': get_background(value['Appearances']),
            'img_link': value['img_link'],
        }
        rows.append(row)

    return rows

@main_bp.route("/proxy-image")
def proxy_image():
    #img_url = request.args.get("img_link")  # Obtém o link da imagem pela query string
    #if not img_url:
    #    return "URL da imagem não fornecida", 400
    #
    #response = requests.get(img_url, stream=True)
    #if response.status_code == 200:
    #    return send_file(response.raw, mimetype="image/jpeg")
    #
    #return "Imagem não encontrada", 404
    image_url = request.args.get("img_link")  # Substitua pelo link real da imagem

    # Baixa a imagem ou retorna a versão do cache
    cached_image = download_image(image_url)

    # Retorna a imagem do cache
    return send_file(cached_image, mimetype='image/jpeg')

def get_cache_filename(url):
    """Gera um nome único para o arquivo a partir da URL da imagem (usando hash)."""
    return os.path.join(CACHE_DIR, hashlib.md5(url.encode('utf-8')).hexdigest())

def download_image(url):
    """Baixa a imagem de um link externo e a armazena no cache local."""
    cache_filename = get_cache_filename(url)

    if not os.path.exists(cache_filename):
        # Se a imagem não estiver no cache, baixe-a
        print(f"Baixando a imagem de {url}")
        response = requests.get(url)
        
        if response.status_code == 200:
            # Salva a imagem no cache
            with open(cache_filename, 'wb') as f:
                f.write(response.content)
        else:
            raise Exception(f"Erro ao baixar a imagem: {response.status_code}")
    
    return cache_filename

def get_background(values):
    row_aparicoes = [appearance.strip() for appearance in values.split(',')]
    data_aparicoes = [appearance.strip() for appearance in data['Appearances'][rand-1].split(',')]

    if set(row_aparicoes) == set(data_aparicoes):
        return 'background-verde'
    # Verificar se existe alguma correspondência
    if any(appearance in data_aparicoes for appearance in row_aparicoes):
        return 'background-amarelo'
    # Se não houver nenhuma correspondência
    return 'background-vermelho'

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

if last_sheet == '':
    last_sheet = 'Database'
# Testar a função
rand = gerar_numero_aleatorio(last_sheet)
#print(f"O número aleatório gerado para hoje é: {rand}")
data = get_data(last_sheet)
