import requests
from py_edamam import Edamam

account = Edamam(recipes_appid="bc8e03f2", recipes_appkey="d263a2d7110848ad2682bf7e99bd826f")

recipes_listed = account.search_recipe("peas")

for index, recipe in enumerate(recipes_listed):
    print(f"Recipe: {recipes_listed['hits'][index]['recipe']['label']}")
    print("Ingredients are listed below")
    ingredients = recipes_listed['hits'][index]['recipe']['ingredientLines']
    url = recipes_listed['hits'][index]['recipe']['url']
    for i, ing in enumerate(ingredients, start=1):
        print(f"{i}) {ing}")
    print(f"Full detailed recipe: {url}\n")
