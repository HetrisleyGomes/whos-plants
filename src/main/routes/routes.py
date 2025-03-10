from flask import render_template, url_for, request, redirect, Blueprint
import pandas as pd
import random
from datetime import datetime

main_bp = Blueprint("main_bp", __name__)


file_path = 'data/PVZ.xlsx'
last_sheet = ''

used_values = []
choosed_names = []
chinease_used_values = []
chinease_choosed_names = []

victory = False
chinease_victory = False
number_of_trys = [0,0,0]

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
        used_values = used_values,
        choosed_names = choosed_names,
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
        used_values = chinease_used_values,
        choosed_names = chinease_choosed_names,
        rand = rand,
        victory = chinease_victory,
        number_of_trys = number_of_trys
        )

@main_bp.route("/makeguess", methods=["GET","POST"])
def guesser():
    guess = request.form.get('guess')
    print(guess.capitalize())
    item = data[data['Name'].str.lower() == guess.lower()]
    global victory
    used_values.append(int(item['ID'].iloc[0]))
    choosed_names.append(item['Name'].iloc[0])
    if data['Name'][rand-1] == item['Name'].iloc[0]:
        victory = True
        number_of_trys[0] = used_values.__len__()

    return redirect(url_for('main_bp.index'))
    
@main_bp.route("/makeguess_chinease", methods=["GET","POST"])
def guesser_chinease():
    guess = request.form.get('guess')
    print(guess.capitalize())
    item = data[data['Name'].str.lower() == guess.lower()]
    global chinease_victory
    chinease_used_values.append(int(item['ID'].iloc[0]))
    chinease_choosed_names.append(item['Name'].iloc[0])
    if data['Name'][rand-1] == item['Name'].iloc[0]:
        chinease_victory = True
        number_of_trys[1] = chinease_used_values.__len__()

    return redirect(url_for('main_bp.chinease'))

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


def get_data(sheet_name):
    global last_sheet
    last_sheet = sheet_name
    data = pd.read_excel(file_path, sheet_name=sheet_name, header=0)
    df = data[data['Name'].notna()]

    return df

def get_rows(version):
    rows = []
    values_to_use = used_values if version == 0 else chinease_used_values
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
        }
        rows.append(row)
    rows.reverse()
    
    return rows


if last_sheet == '':
    last_sheet = 'Database'
# Testar a função
rand = gerar_numero_aleatorio(last_sheet)
#print(f"O número aleatório gerado para hoje é: {rand}")
data = get_data(last_sheet)
