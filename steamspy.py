import os
import requests

IMAGE_URL = os.getenv("IMAGE_URL")
GENRE_URL = os.getenv("GENRE_URL")
DETAILS_URL = os.getenv("DETAILS_URL")


def querygames():
    """querygames"""
    # In the end this method should take a list of genres as a parameter and query a certain (random?) amount of games from each genre.
    # Currently this method only searches for games of a single genre
    # will add more specific game tags when we have more things worked out

    image = []  # collect poster images
    details = []  # keep path to details for individual game pages
    title = []  # collect game titles
    price = []  # collect game prices
    genres = GENRE_URL + "action"  # current test query
    response = requests.get(genres)
    response_json = response.json()
    appid = list(response_json)[:5]
    for i in range(len(appid)):
        details_path = DETAILS_URL + str(appid[i])
        details.append(
            details_path
        )  # adds the current game details path to the details list
        poster_path = IMAGE_URL + str(appid[i]) + "/header.jpg"
        image.append(poster_path)  # adds the current poster path to the image list
        details_response = requests.get(details_path)
        details_json = details_response.json()
        title.append(str(details_json["name"]))  # adds current title to title list
        price.append(int(details_json["price"]))  # adds current price to price list
        if price == 0:  # For better formatting than "$0"
            price[i] = "Free to Play"
    print(appid)
    print(title)
    print(details)
    print(image)
