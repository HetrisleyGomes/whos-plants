from flask import render_template, url_for, request, redirect, Blueprint, send_file, session
import hashlib
import requests
import os
import random
from datetime import datetime, timedelta
from ..utils.rand_num_generators import gerar_numero_aleatorio, gerar_numero_aleatorio_img, gerar_numero_aleatorio_random, get_data
from ..utils.data_controllers import get_rows, get_all, check_victory, get_all_plants
from ..utils.json_data import load_user_access, save_user_access, today_str_func

main_bp = Blueprint("main_bp", __name__)
CACHE_DIR = 'cache'

last_sheet = ''
last_mode = 'normal'

used_values = [[],[],[],[],[]]
choosed_names = [[],[],[],[],[]]

victory = [False, False, False, False, False]
number_of_trys = [0,0,0,0,0]

infinity_number = 999

@main_bp.route("/")
@main_bp.route("/index")
def index():
    global rand, data, last_mode, last_sheet
    if last_sheet != 'Database':
        data, last_sheet = get_data('Database')
    if last_mode != 'normal':
        rand = gerar_numero_aleatorio('Database')
        last_mode = 'normal'

    names = data['Name'].tolist()
    today_str, yesterday_str = today_str_func()

    return render_template(
        "index.html",
        data = data,
        names = names,
        rows = get_rows(0,used_values, data, rand),
        used_values = used_values[0],
        choosed_names = choosed_names[0],
        rand = rand,
        victory = victory,
        number_of_trys = number_of_trys,
        user_access = load_user_access(),
        today = today_str,
        yesterday = yesterday_str
        )

@main_bp.route("/chinease")
def chinease():
    global rand, data, last_mode, last_sheet
    if last_sheet != 'Chinese_Database':
        rand = gerar_numero_aleatorio('Chinese_Database')
        data, last_sheet = get_data('Chinese_Database')
        last_mode = 'chinease'

    names = data['Name'].tolist()
    today_str, yesterday_str = today_str_func()

    return render_template(
        "chinease_version.html",
        data = data,
        names = names,
        rows = get_rows(1,used_values, data, rand),
        used_values = used_values[1],
        choosed_names = choosed_names[1],
        rand = rand,
        victory = victory,
        number_of_trys = number_of_trys,
        user_access = load_user_access(),
        today = today_str,
        yesterday = yesterday_str
        )

@main_bp.route("/all")
def all():
    global rand, data, last_mode, last_sheet
    if last_sheet != 'All_data':
        rand = gerar_numero_aleatorio('All_data')
        data, last_sheet = get_data('All_data')
        last_mode = 'all'

    names = data['Name'].tolist()
    today_str, yesterday_str = today_str_func()

    return render_template(
        "all_mode.html",
        data = data,
        names = names,
        rows = get_rows(2,used_values, data, rand),
        used_values = used_values[2],
        choosed_names = choosed_names[2],
        rand = rand,
        victory = victory,
        number_of_trys = number_of_trys,
        user_access = load_user_access(),
        today = today_str,
        yesterday = yesterday_str
        )

@main_bp.route("/img_guess")
def img_guess():
    global rand, data, last_mode, last_sheet
    if last_sheet != 'Database':
        data, last_sheet = get_data('Database')
    if last_mode != 'image':
        rand = gerar_numero_aleatorio_img('Database')
        last_mode = 'image'

    names = data['Name'].tolist()
    today_str, yesterday_str = today_str_func()

    return render_template(
        "image_guess.html",
        data = data,
        names = names,
        rows = get_rows(3,used_values, data, rand),
        used_values = used_values[3],
        choosed_names = choosed_names[3],
        used_values_len = len(used_values[3]),
        rand = rand,
        victory = victory,
        number_of_trys = number_of_trys,
        user_access = load_user_access(),
        today = today_str,
        yesterday = yesterday_str
        )

@main_bp.route("/infinity")
def infinity():
    global rand, data, infinity_number, last_mode, last_sheet
    if last_sheet != 'Database':
        data, last_sheet = get_data('Database')
        last_mode = 'infinity'
    if infinity_number == 999:
        rand = gerar_numero_aleatorio_random('Database')
        infinity_number = rand
    
    print(infinity_number)
    names = data['Name'].tolist()
    today_str, yesterday_str = today_str_func()
    return render_template(
        "infinity.html",
        data = data,
        names = names,
        rows = get_rows(9,used_values, data, rand),
        used_values = used_values[len(used_values)-1],
        choosed_names = choosed_names[len(choosed_names)-1],
        rand = rand,
        victory = victory[len(victory)-1],
        user_access = load_user_access(),
        today = today_str,
        yesterday = yesterday_str
        )

_cached_data = None
_last_sheet_loaded = None
_card_collection = []

@main_bp.route("/test")
def testes():
    global _cached_data, _last_sheet_loaded # Para simular o cache de dados globalmente neste exemplo

    if _last_sheet_loaded != 'Database' or _cached_data is None:
        _cached_data, _last_sheet_loaded = get_data('Database')

    sorted_cards_for_template = session.get('sorted_cards', []) 
    # Ao recuperar da sessão, converta a lista de volta para um set para manter a unicidade
    user_card_collection_list = session.get('user_card_collection', [])
    user_card_collection = set(user_card_collection_list)

    today_str, yesterday_str = today_str_func()
    
    return render_template(
        "test.html",
        data = _cached_data,
        rows = get_all_plants(_cached_data),
        user_access = load_user_access(),
        sorted_cards = sorted_cards_for_template, # As cartas sorteadas para exibir
        today = today_str,
        yesterday = yesterday_str,
        cards = user_card_collection
        )

@main_bp.route("/sortearcards")
def sortearcards():
    global _cached_data
    if _cached_data is None:
        _cached_data, _ = get_data('Database')

    sorted_cards = select_cards_by_rarity(get_all_plants(_cached_data))

    # 1. Recupera a coleção existente da sessão (ou cria uma nova lista vazia se não houver)
    # E converte para set para garantir a unicidade durante a adição
    user_card_collection_list = session.get('user_card_collection', [])
    user_card_collection_set = set(user_card_collection_list) # Convertido para set

    # 2. Adiciona os nomes das novas cartas à coleção usando .add() no set
    for card in sorted_cards:
        user_card_collection_set.add(card['name'])

    # 3. Armazena a coleção atualizada de volta na sessão, convertendo o set para list
    session['user_card_collection'] = list(user_card_collection_set) # Convertido de volta para list
    
    session['sorted_cards'] = sorted_cards
    return redirect(url_for('main_bp.testes'))

@main_bp.route("/test/<id>")
def testes_id(id):
    global data, last_sheet
    if last_sheet != 'Database':
        data, last_sheet = get_data('Database')

    plant = data.iloc[int(id)]

    return render_template(
        "test.html",
        data = data,
        plant = plant,
        )

@main_bp.route("/makeguess", methods=["GET","POST"])
def guesser():
    global victory, data
    
    id = int(request.form.get("id"))
    guess = request.form.get('guess')
    item = data[data['Name'].str.lower() == guess.lower()]

    used_values[id].append(int(item['ID'].iloc[0]))
    choosed_names[id].append(item['Name'].iloc[0])

    if data['Name'][rand-1] == item['Name'].iloc[0]:
        victory[id] = True
        number_of_trys[id] = used_values[id].__len__()

    info = load_user_access()
    today_str, yesterday_str = today_str_func()

    if check_victory(victory):
        values = {
            "last_acess": info["last_acess"],
            "daily_sequence": info['daily_sequence'],
            "total_victories": {
                "main": info['total_victories']["main"],
                "chinease": info['total_victories']["chinease"]+1,
                "crazy": info['total_victories']["crazy"]+1,
                "gnome": info['total_victories']["gnome"]+1
            }
        }
        save_user_access(values)
    elif victory[0] == True and info['last_acess'] != today_str:
        keep_sequence = info['daily_sequence']
        if info['last_acess'] == yesterday_str or info['last_acess'] == " ":
            keep_sequence = int(info['daily_sequence']) +1
        else:
            keep_sequence = 1
        values = {
            "last_acess": today_str,
            "daily_sequence": keep_sequence,
            "total_victories": {
                "main": info['total_victories']["main"]+1,
                "chinease": info['total_victories']["chinease"],
                "crazy": info['total_victories']["crazy"],
                "gnome": info['total_victories']["gnome"]
            }
        }
        save_user_access(values)

    if id == 0:
        return redirect(url_for('main_bp.index'))
    elif id ==1:
        return redirect(url_for('main_bp.chinease'))
    elif id ==2:
        return redirect(url_for('main_bp.all'))
    elif id ==3:
        return redirect(url_for('main_bp.img_guess'))
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

@main_bp.route("/proxy-image")
def proxy_image():
    # Substitua pelo link real da imagem
    image_url = request.args.get("img_link")  

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

def select_cards_by_rarity(all_plants_data, num_cards=5):
    # Dicionário para armazenar plantas por raridade
    plants_by_rarity = {}
    for plant in all_plants_data:
        rarity = plant['rarity']
        if rarity not in plants_by_rarity:
            plants_by_rarity[rarity] = []
        plants_by_rarity[rarity].append(plant)

    # --- Defina os pesos para cada raridade ---
    # Você pode ajustar esses pesos conforme a sua necessidade.
    # A soma dos pesos não precisa ser 1, mas as proporções importam.
    rarity_weights = {
        'Common': 1,    # 50% de chance
        'Uncommon': 0.0,  # 30% de chance
        'Rare': 0.0,     # 15% de chance
        'Epic': 0.0,    # 4% de chance
        'Legendary': 0.0,  # 1% de chance
        'Mythical': 0.0
    }

    # As raridades disponíveis no seu jogo
    available_rarities = list(rarity_weights.keys())
    selected_cards = []

    for _ in range(num_cards):

        if _ == 1:
            rarity_weights['Common'] = 0.5
            rarity_weights['Uncommon'] = 0.5
        elif _ == 2:
            rarity_weights['Common'] = 0.15
            rarity_weights['Uncommon'] = 0.5
            rarity_weights['Rare'] = 0.35
        elif _ == 3:
            rarity_weights['Common'] = 0.0
            rarity_weights['Uncommon'] = 0.4
            rarity_weights['Rare'] = 0.4
            rarity_weights['Epic'] = 0.2
        elif _ == 4:
            rarity_weights['Uncommon'] = 0.0
            rarity_weights['Rare'] = 0.45
            rarity_weights['Epic'] = 0.30
            rarity_weights['Mythical'] = 0.20
            rarity_weights['Legendary'] = 0.05

        # Os pesos correspondentes às raridades
        weights = [rarity_weights[r] for r in available_rarities]


        # Escolhe uma raridade baseada nos pesos
        chosen_rarity = random.choices(available_rarities, weights=weights, k=1)[0]

        # Filtra as plantas disponíveis para a raridade escolhida
        # Garante que só sorteia plantas da raridade que acabou de ser escolhida.
        possible_plants_for_rarity = plants_by_rarity.get(chosen_rarity, [])

        if not possible_plants_for_rarity:
            print(f"Aviso: Não há plantas disponíveis para a raridade '{chosen_rarity}'. Pulando esta seleção.")
            continue # Pula para a próxima iteração se não houver plantas dessa raridade

        # Seleciona uma planta aleatoriamente dentro da raridade escolhida
        selected_plant = random.choice(possible_plants_for_rarity)
        selected_cards.append(selected_plant)
    
    return selected_cards

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

if last_sheet == '':
    last_sheet = 'Database'

access_info = load_user_access()

# Testar a função
rand = gerar_numero_aleatorio(last_sheet)
#print(f"O número aleatório gerado para hoje é: {rand}")
data, last_sheet = get_data(last_sheet)
