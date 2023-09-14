import json
import requests

app_id = json.load(open("Edamam_token.json", 'r'))["TOKEN"]["APP_ID"]
app_key = json.load(open("Edamam_token.json", 'r'))["TOKEN"]["APP_KEY"]
search_query = "onion and chicken"

url = f"https://api.edamam.com/search"
params = {
    "app_id": app_id,
    "app_key": app_key,
    "q": search_query,
    "to": 10  # Number of results
}
response = requests.get(url, params=params)
data = response.json()

for recipe in data['hits']:
    recipe = recipe['recipe']
    print("Title:", recipe['label'])
    print("Calories:", recipe['calories'])
    print("Cautions:", recipe['cautions'])
    print("Diet Labels:", recipe['dietLabels'])
    print("Health Labels:", recipe['healthLabels'])
    print("URL:", recipe['url'])
    print("Ingredients:", recipe['ingredientLines'])
    print()
