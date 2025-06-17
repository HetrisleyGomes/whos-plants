def get_rows(version, used_values, data, rand):
    rows = []
    values_to_use = used_values[0] if version == 0 else (used_values[1] if version == 1 else (used_values[2] if version == 2 else (used_values[3] if version == 3 else used_values[len(used_values)-1])))
    for value in values_to_use:
        sun_cust = data['Sun Cust'].iloc[value - 1]
        tought = data['Tought'].iloc[value - 1]
        damage = data['Damage'].iloc[value - 1]
        recarga = data['Recarga'].iloc[value - 1]
        row = {
            'name': data['Name'].iloc[value - 1],
            'type': data['Type'].iloc[value - 1],
            'sun_cust': int(sun_cust) if sun_cust.is_integer() else sun_cust,
            'tought': int(tought) if tought.is_integer() else tought,
            'damage': int(damage) if damage.is_integer() else damage,
            'recarga': int(recarga) if recarga.is_integer() else recarga,
            'rarity': data['Rarity'].iloc[value - 1],
            'usage': [data['Single use'].iloc[value - 1],data['Instant use'].iloc[value - 1]],
            'plant_origin': data['Plant_Origin'].iloc[value -1],
            'origin': data['Origin'].iloc[value - 1],
            'classification': data['Classification'].iloc[value - 1],
            'appearances': data['Appearances'].iloc[value - 1],
            'background': get_background(data['Appearances'].iloc[value - 1], data, rand),
            'img_link': data['img_link'].iloc[value - 1],
        }
        rows.append(row)
    rows.reverse()
    
    return rows

def get_all(data, rand):
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
            'background-appearances': get_background(value['Appearances'], data, rand),
            'img_link': value['img_link'],
        }
        rows.append(row)

    return rows

def get_all_plants(data):
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
            'img_link': value['img_link'],
        }
        rows.append(row)

    return rows

def get_background(values, data, rand):
    row_aparicoes = [appearance.strip() for appearance in values.split(',')]
    data_aparicoes = [appearance.strip() for appearance in data['Appearances'][rand-1].split(',')]

    if set(row_aparicoes) == set(data_aparicoes):
        return 'background-verde'
    # Verificar se existe alguma correspondência
    if any(appearance in data_aparicoes for appearance in row_aparicoes):
        return 'background-amarelo'
    # Se não houver nenhuma correspondência
    return 'background-vermelho'

def check_victory(victory):
    for i in range(4):
        if not victory[i]:  # Se algum valor for False, retorna False
            return False
    return True  # Se todos os valores forem True, retorna True