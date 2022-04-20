import requests


def queryreviews():
    REVIEW_URL = "https://store.steampowered.com/appreviews/1222670?json=1"
    response = requests.get(REVIEW_URL)
    response_json = response.json()
    print(response_json["reviews"][0].get("review"))


queryreviews()
