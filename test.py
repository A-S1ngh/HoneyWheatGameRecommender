import requests

DESCRIPTION = "https://store.steampowered.com/api/appdetails?appids=1222670"

res = requests.get(DESCRIPTION)
data = res.json()
print(data["1222670"]["data"].get("about_the_game"))
