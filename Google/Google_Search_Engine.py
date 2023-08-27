import json

import requests  # type: ignore

apikey = json.load(open("Search_Engine_Credentials.json", "r"))["KEYS"]["API"]
engineid = json.load(open("Search_Engine_Credentials.json", "r"))["KEYS"]["ENGINEID"]


def Search(query, nums, sorting=None):
    url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": apikey,
        "cx": engineid,
        # "searchType": "text" or image
        "num": nums,
        "sort": sorting

    }
    response = requests.get(url, params=params)
    data = response.json()

    if "items" in data:
        for item in data["items"]:
            Title = item.get("title", "No Title")
            Link = item.get("link", "No Link")
            print(f"Found result {Title} and link {Link}")


if __name__ == '__main__':
    Search("cats", 10, )
