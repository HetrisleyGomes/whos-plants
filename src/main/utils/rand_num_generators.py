from datetime import datetime
import pandas as pd
import random

file_path = 'data/PVZ.xlsx'

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


def gerar_numero_aleatorio_img(sheet_name):
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
    semente = int(data_atual.strftime("%m%Y%d"))  # Formato MMYYYYDD, ex: 20250219

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