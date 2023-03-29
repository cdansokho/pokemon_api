import csv
import os
import pathlib
import shutil
import unittest
import json
from pokemon_api import app


class TestsPokemons(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        app.config['TESTING'] = True
        path_base = pathlib.Path("test_pokemon.csv").parent.absolute().__str__()
        self.file_source = path_base + '/../data/test_pokemon.csv'
        self.csv_file_test_backup = path_base + '/../data/test_pokemon_backup.csv'
        app.config['CSV_PATH'] = self.file_source
        shutil.copy2(self.file_source, self.csv_file_test_backup)

    def tearDown(self):
        os.remove(self.file_source)
        shutil.copy2(self.csv_file_test_backup, self.file_source)
        os.remove(self.csv_file_test_backup)
        print('Test terminé')

    def test_get_pokemon_by_id(self):
        # Test avec un ID valide
        response = self.app.get('/1')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['#'], '1')

        # Test avec un ID invalide
        response = self.app.get('/10000')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Pokemon non trouvées')

    def test_get_pokemon_by_name(self):
        # Test avec un nom de pokemon valide
        response = self.app.get('/Bulbasaur')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['Name'], 'Bulbasaur')

        # Test avec un nom de pokemon invalide
        response = self.app.get('/Pikapika')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Pokemon non trouvées')

    def test_update_pokemon_by_id(self):
        # Test avec un ID valide
        data = {
            "Name": "Updated Pokemon",
            "Type 1": "New Type",
            "Type 2": "",
            "Total": 600,
            "HP": 100,
            "Attack": 150,
            "Defense": 100,
            "Sp. Atk": 150,
            "Sp. Def": 100,
            "Speed": 100,
            "Generation": 1,
            "Legendary": "False"
        }
        response = self.app.post('/update/2', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.get_data(as_text=True)), {'message': 'Données mises à jour avec succès'})

    def test_update_pokemon_by_name(self):
        # Test avec un nom de pokemon valide
        data = {
            "Name": "Updated Pokemon",
            "Type 1": "New Type",
            "Type 2": "",
            "Total": 600,
            "HP": 100,
            "Attack": 150,
            "Defense": 100,
            "Sp. Atk": 150,
            "Sp. Def": 100,
            "Speed": 100,
            "Generation": 1,
            "Legendary": "False"
        }
        response = self.app.post('/update/Charmander', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.get_data(as_text=True)), {'message': 'Données mises à jour avec succès'})

    def test_update_pokemon_not_found(self):
        # Test avec un pokemon inexistant
        data = {
            "Name": "Updated Pokemon",
            "Type 1": "New Type",
            "Type 2": "",
            "Total": 600,
            "HP": 100,
            "Attack": 150,
            "Defense": 100,
            "Sp. Atk": 150,
            "Sp. Def": 100,
            "Speed": 100,
            "Generation": 1,
            "Legendary": "False"
        }
        response = self.app.post('/update/PokemonNonExistant', json=data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.get_data(as_text=True)), {'error': 'Pokemon PokemonNonExistant non trouvé.'})

    def test_update_pokemon_invalid_data(self):
        # Test avec des données invalides
        data = {
            "Name": "Updated Pokemon",
            "Type 1": "New Type",
            "Type 2": "",
            "Total": "invalid",
            "HP": 100,
            "Attack": 150,
            "Defense": 100,
            "Sp. Atk": 150,
            "Sp. Def": 100,
            "Speed": 100,
            "Generation": 1,
            "Legendary": "False"
        }
        response = self.app.post('/update/1', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.get_data(as_text=True)), {'error': 'Les données ne sont pas au bon format.'})

    def test_delete_pokemon_by_id(self):
        # Suppression d'un pokemon avec un ID valide
        response = self.app.delete('/delete/1')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Données supprimées avec succès')

        # Vérification que le pokemon a bien été supprimé
        with open(app.config['CSV_PATH'], 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                self.assertNotEqual(row[0], '1')

        # Suppression d'un pokemon avec un ID invalide
        response = self.app.delete('/delete/10001')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['error'], 'Pokemon 10001 non trouvé.')

    def test_delete_pokemon_by_name(self):
        # Suppression d'un pokemon avec un nom valide
        response = self.app.delete('/delete/Bulbasaur')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Données supprimées avec succès')

        # Vérification que le pokemon a bien été supprimé
        with open(app.config['CSV_PATH'], 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                self.assertNotEqual(row[1], 'Bulbasaur')

        # Suppression d'un pokemon avec un nom invalide
        response = self.app.delete('/delete/Bulbasaur')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['error'], 'Pokemon Bulbasaur non trouvé.')

    def test_get_all_pokemon(self):
        # Test de la route
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
