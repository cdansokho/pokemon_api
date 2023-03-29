import csv
import pathlib
from flask import Flask, request, jsonify, render_template
from flask_paginate import Pagination, get_page_args

# Initialisation de l'application Flask
app = Flask(__name__)

# Définition des variables de configuration de l'application
app.config['CSV_PATH'] = pathlib.Path("pokemon.csv").parent.absolute().__str__() + '/data/pokemon.csv'
app.config['ITEMS_PER_PAGE'] = 10


def get_last_id():
    # Récupération de l'id du dernier champ dans le fichier CSV
    path_file_csv = app.config['CSV_PATH']
    with open(path_file_csv, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        last_row = list(csv_reader)[-1]
        last_id = int(last_row[0])
    return last_id


def check_json_data(request):
    # Vérification des données du formulaire d'ajout d'un Pokémon
    data = request.get_json()
    try:
        # Récupération des données et vérification de leur type
        name = str(data['Name'])
        type1 = str(data['Type 1'])
        type2 = str(data['Type 2'])
        total = int(data['Total'])
        hp = int(data['HP'])
        attack = int(data['Attack'])
        defense = int(data['Defense'])
        sp_atk = int(data['Sp. Atk'])
        sp_def = int(data['Sp. Def'])
        speed = int(data['Speed'])
        generation = int(data['Generation'])
        legendary = bool(data['Legendary'])
        return name, type1, type2, total, hp, attack, defense, sp_atk, sp_def, speed, generation, legendary
    except (KeyError, TypeError, ValueError):
        # En cas d'erreur, renvoie une erreur 400 (Bad Request)
        return jsonify({'error': 'Les données ne sont pas au bon format.'}), 400


# Définition de la route pour récupérer toutes les données du fichier CSV
@app.route('/', methods=['GET'])
def get_all_pokemon():
    # Récupération de toutes les données du fichier CSV
    path_file_csv = app.config['CSV_PATH']
    with open(path_file_csv, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # saute la première ligne si nécessaire
        data = []
        for row in csv_reader:
            data.append(row)

    if data is None:
        # En cas d'erreur, renvoie une erreur 500 (Internal Server Error)
        return render_template('error.html', message='Erreur lors de la récupération des données.'), 500

    # Pagination des données
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    per_page = app.config['ITEMS_PER_PAGE']
    total = len(data)
    pagination_donnees = data[offset: offset + per_page]
    pagination = Pagination(page=page, per_page=per_page, total=total)

    # Renvoi des données paginées sous forme de HTML
    return render_template('data.html', donnees=pagination_donnees, pagination=pagination)



# Définir la route pour récupérer une ligne spécifique du fichier CSV
@app.route('/<id_or_name>', methods=['GET'])
def get_pokemon(id_or_name):
    path_file_csv = app.config['CSV_PATH']
    with open(path_file_csv, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['#'] == id_or_name or row['Name'] == id_or_name:
                return jsonify(row)
    return jsonify({'message': 'Pokemon non trouvées'})


# Définir la route pour ajouter des données au fichier CSV
@app.route('/add', methods=['POST'])
def add_pokemon():
    path_file_csv = app.config['CSV_PATH']
    # Vérification du type de chaque champ
    if len(check_json_data(request)) > 2:
        name, type1, type2, total, hp, attack, defense, sp_atk, sp_def, speed, generation, legendary = check_json_data(
            request)
    else:
        return check_json_data(request)

    with open(path_file_csv, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['#', 'Name', 'Type 1', 'Type 2', 'Total', 'HP', 'Attack', 'Defense',
                                                  'Sp. Atk', 'Sp. Def', 'Speed', 'Generation', 'Legendary'])
        writer.writerow(
            {'#': get_last_id() + 1, 'Name': name, 'Type 1': type1, 'Type 2': type2, 'Total': total, 'HP': hp,
             'Attack': attack,
             'Defense': defense, 'Sp. Atk': sp_atk, 'Sp. Def': sp_def, 'Speed': speed, 'Generation': generation,
             'Legendary': legendary})

    return jsonify({'message': 'Données ajoutées avec succès'})


# Définir la route pour mettre à jour une ligne spécifique du fichier CSV
@app.route('/update/<id_or_name>', methods=['POST'])
def update_pokemon(id_or_name):
    path_file_csv = app.config['CSV_PATH']

    if len(check_json_data(request)) > 2:
        name, type1, type2, total, hp, attack, defense, sp_atk, sp_def, speed, generation, legendary = check_json_data(request)
    else:
        return check_json_data(request)

    # Recherche de la ligne à mettre à jour
    updated = False
    with open(path_file_csv, 'r', newline='') as file:
        reader = csv.DictReader(file)
        rows = []
        for row in reader:
            if row['#'] == id_or_name or row['Name'] == id_or_name:
                row['Name'] = name
                row['Type 1'] = type1
                row['Type 2'] = type2
                row['Total'] = total
                row['HP'] = hp
                row['Attack'] = attack
                row['Defense'] = defense
                row['Sp. Atk'] = sp_atk
                row['Sp. Def'] = sp_def
                row['Speed'] = speed
                row['Generation'] = generation
                row['Legendary'] = legendary
                rows.append(row)
                updated = True
            else:
                rows.append(row)

    # Mise à jour du fichier CSV si la ligne a été trouvée
    if updated:
        with open(path_file_csv, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['#', 'Name', 'Type 1', 'Type 2', 'Total', 'HP', 'Attack',
                                                      'Defense', 'Sp. Atk', 'Sp. Def', 'Speed', 'Generation',
                                                      'Legendary'])
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
        return jsonify({'message': 'Données mises à jour avec succès'})
    else:
        return jsonify({'error': 'Pokemon {} non trouvé.'.format(id_or_name)}), 404


# Définir la route pour supprimer une ligne spécifique du fichier CSV
@app.route('/delete/<id_or_name>', methods=['DELETE'])
def delete_pokemon(id_or_name):
    path_file_csv = app.config['CSV_PATH']

    # Recherche de la ligne à supprimer
    deleted = False
    with open(path_file_csv, 'r+', newline='') as file:
        reader = csv.DictReader(file)
        rows = []
        for row in reader:
            if row['#'] != id_or_name and row['Name'] != id_or_name:
                rows.append(row)
            else:
                deleted = True

        # Mise à jour du fichier CSV si la ligne a été trouvée
        if deleted:
            file.seek(0)
            writer = csv.DictWriter(file, fieldnames=['#', 'Name', 'Type 1', 'Type 2', 'Total', 'HP', 'Attack',
                                                      'Defense', 'Sp. Atk', 'Sp. Def', 'Speed', 'Generation',
                                                      'Legendary'])
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
            file.truncate()
            return jsonify({'message': 'Données supprimées avec succès'})
        else:
            return jsonify({'error': 'Pokemon {} non trouvé.'.format(id_or_name)}), 404


if __name__ == '__main__':
    app.run(port=8000, debug=True)
