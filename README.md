# Flask API for Pokemon Data
> This is a Flask API that allows you to access and manipulate data on Pokemon. It uses a CSV file as the data source and provides endpoints for getting all Pokemon, getting a specific Pokemon, adding a Pokemon, updating a Pokemon, and deleting a Pokemon.

## Installation
##### Clone this repository: 
```py
git clone https://github.com/cdansokho/pokemon_api.git
```
##### Navigate to the project directory: 
```py
cd pokemon_api
```
##### Create a virtual environment: 
```py
python3 -m venv venv
```
##### Activate the virtual environment:
```py
source venv/bin/activate
```

##### Install the required packages: 
```py
pip3 install -r requirements.txt
```

# Usage
##### Start the Flask app: 
```py
 python3 pokemon_api.py
```
Open your web browser and go to http://localhost:8000
# GET all Pokemon
### /
This endpoint returns all the Pokemon data in the CSV file.

# GET a specific Pokemon
### /<id_or_name>
This endpoint returns the data for a specific Pokemon based on either the # or Name column in the CSV file. 
Replace <id_or_name> with the value you want to search for.

# POST add a Pokemon
### /add
This endpoint allows you to add a new Pokemon to the CSV file. You can add a Pokemon by sending 
a JSON object in the request body with the following keys: Name, Type 1, Type 2, Total, HP, Attack,
Defense, Sp. Atk, Sp. Def, Speed, Generation, and Legendary. Example JSON object:
```
 {
    "Name": "Bulbasaur",
    "Type 1": "Grass",
    "Type 2": "Poison",
    "Total": 318,
    "HP": 45,
    "Attack": 49,
    "Defense": 49,
    "Sp. Atk": 65,
    "Sp. Def": 65,
    "Speed": 45,
    "Generation": 1,
    "Legendary": "False"
}
```

## POST update a Pokemon

### /update/<id_or_name>
This endpoint allows you to update an existing Pokemon in the CSV file. You can update a Pokemon
by sending a JSON object in the request body with the same keys as the POST add a Pokemon endpoint. Replace <id_or_name> with the value of the Pokemon you want to update.

```
 {
    "Name": "Bulbasaur",
    "Type 1": "Grass",
    "Type 2": "Poison",
    "Total": 318,
    "HP": 45,
    "Attack": 49,
    "Defense": 49,
    "Sp. Atk": 65,
    "Sp. Def": 65,
    "Speed": 45,
    "Generation": 1,
    "Legendary": "False"
}
```
# DELETE a Pokemon
### /delete/<id_or_name>
This endpoint allows you to delete an existing Pokemon from the CSV file. Replace <id_or_name>
with the value of the Pokemon you want to delete.
