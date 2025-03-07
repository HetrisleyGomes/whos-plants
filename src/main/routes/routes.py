from flask import render_template, url_for, request, redirect, Blueprint, jsonify
import pandas as pd
import json, os, random
from datetime import datetime

main_bp = Blueprint("main_bp", __name__)


file_path = 'data/PVZ.xlsx'
used_values = []
choosed_names = []
victory = False

@main_bp.route("/")
@main_bp.route("/index")
def index():
    names = data['Name'].tolist()

    return render_template(
        "index.html",
        data = data,
        names = names,
        rows = get_rows(),
        used_values = used_values,
        choosed_names = choosed_names,
        rand = rand,
        victory = victory
        )

@main_bp.route("/makeguess", methods=["GET","POST"])
def guesser():
    guess = request.form.get('guess')
    print(guess.capitalize())
    item = data[data['Name'].str.lower() == guess.lower()]
    global victory
    if data['Name'][rand-1] == item['Name'].iloc[0]:
        print("Acertou")
        used_values.append(int(item['ID'].iloc[0]))
        choosed_names.append(item['Name'].iloc[0])
        victory = True
    else:
        print('errou')
        used_values.append(int(item['ID'].iloc[0]))
        choosed_names.append(item['Name'].iloc[0])
    return redirect(url_for('main_bp.index'))
    

def gerar_numero_aleatorio():
    # Carregar o arquivo Excel
    file_path = 'data/PVZ.xlsx'
    data = pd.read_excel(file_path, sheet_name='Database')
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


def get_data():
    file_path = 'data/PVZ.xlsx'
    data = pd.read_excel(file_path, sheet_name='Database', header=0)
    df = data[data['Name'].notna()]

    return df

def get_rows():
    rows = []
    for value in used_values:
        print(data['Recarga'].iloc[value - 1])
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
            'origin': data['Origin'].iloc[value - 1]
        }
        rows.append(row)

    rows.reverse()
    
    return rows


# Testar a função
rand = gerar_numero_aleatorio()
#print(f"O número aleatório gerado para hoje é: {rand}")
data = get_data()
