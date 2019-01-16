# import necessary libraries
from flask import Flask, render_template
import os
import pandas as pd
import requests

# create instance of Flask app
app = Flask(__name__)

base_url = "http://www.recipepuppy.com/api/?"
labels = pd.read_csv('meta/labels.csv', header=None)

ingredient_dict = {}
# for label in labels[0]:
#     dish_name = label
#     query_url = base_url + "q=" + dish_name
#     response = requests.get(query_url)
#     try:
#         ingredients = response.json()['results'][0]['ingredients']
#         ingredient_list = [ingredient for ingredient in ingredients.split(', ')]
#         ingredient_dict[dish_name] = ingredient_list
#     except:
#         print("Error: no results for " + dish_name)


dish_name = 'Fried rice'
query_url = base_url + "q=" + dish_name
response = requests.get(query_url)
try:
    ingredients = response.json()['results'][0]['ingredients']
    ingredient_list = [ingredient for ingredient in ingredients.split(', ')]
    ingredient_dict[dish_name] = ingredient_list
except:
    print("Error: no results for " + dish_name)

@app.route("/")
def index():
    dish = 'Fried rice'
# def inspect(dish):
    allergens = ['egg', 'eggs', 'fish', 'soy sauce', 'soybean', 'peanut', 'nut', 'shrimp', 'lobster', 'crab', 'milk', 'wheat']
    ingredients = [x for x in ingredient_dict[dish]]
    print(f"Common ingredients in {dish}: {ingredients}")

    allergen_dict = {}
    ind = 0
    for ingredient in ingredients:
        if (ingredient in allergens):
            ind += 1
            allergen_dict[ind] = ingredient
            # print(f'Allergen alert: "{ingredient}" is a common food allergen')
    return render_template("index.html", dict = allergen_dict)


# create route that renders index.html template
# @app.route("/")
# def index():
#     player_dictionary = {"player_1": "Jessica",
#                          "player_2": "Mark"}
#     return render_template("index.html", dict=player_dictionary)


if __name__ == "__main__":
    app.run(debug=True)
