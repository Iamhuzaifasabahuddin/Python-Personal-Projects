import requests

app_id = 'bc8e03f2'
app_key = 'd263a2d7110848ad2682bf7e99bd826f'
search_query = "onion and chicken"

url = f"https://api.edamam.com/search"
params = {
    "app_id": app_id,
    "app_key": app_key,
    "q": search_query
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
