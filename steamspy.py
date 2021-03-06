"""Steam Spy API Functions"""
from math import floor
import os
import random
import requests
from dotenv import find_dotenv, load_dotenv



load_dotenv(find_dotenv())


BASE_IMAGE_URL = os.getenv("IMAGE_URL")
BASE_GENRE_URL = os.getenv("GENRE_URL")
BASE_DETAILS_URL = os.getenv("DETAILS_URL")
REVIEWS_URL = os.getenv("REVIEWS_URL")


def querygames(survey_data):
    """querygames"""
    genres = {
        "action": survey_data.action,
        "adventure": survey_data.adventure,
        "rpg": survey_data.roleplaying,
        "strategy": survey_data.strategy,
        "sports": survey_data.sports,
        "simulation": survey_data.simulation,
        "racing": survey_data.racing,
    }
    total = sum(genres.values())
    games = []

    selected_ids = set()
    for genre, rating in sorted(genres.items(), key=lambda item: item[1], reverse=True):
        genre_url = BASE_GENRE_URL + genre  # create the api call to games in this genre
        response = requests.get(genre_url)
        response = response.json()
        id_list = list(response)
        num_of_games = floor((rating / total) * 36)
        if id_list:
            for i in range(num_of_games):
                print(i)
                rand_id = random.randint(1, 100)
                while id_list[rand_id] in selected_ids:
                    rand_id = random.randint(1, 100)
                selected_ids.add(id_list[rand_id])
                current_game = (
                    {}
                )  # below code adds all game details to its own dictionary
                game_rev_url = REVIEWS_URL + str(id_list[rand_id]) + "?json=1"
                res = requests.get(game_rev_url)
                review_list = []
                data = res.json()
                for j in data["reviews"]:
                    review_list.append(j["review"])

                current_game["reviews"] = tuple(review_list)
                details_path = BASE_DETAILS_URL + str(id_list[rand_id])
                current_game["details"] = details_path
                poster_path = BASE_IMAGE_URL + str(id_list[rand_id]) + "/header.jpg"
                current_game["image"] = poster_path
                current_game["title"] = str(response[id_list[rand_id]]["name"])
                current_game["price"] = int(response[id_list[rand_id]]["price"])
                current_game["gameid"] = id_list[rand_id]
                games.append(current_game)
    if games:
        return games

    current_game = {}
    poster_path = BASE_IMAGE_URL + "1222670" + "/header.jpg"
    current_game["image"] = poster_path
    current_game["title"] = "The Sim's 4"
    current_game["price"] = 4000
    current_game["details"] = BASE_DETAILS_URL + "1222670"
    review_list = []
    game_rev_url = REVIEWS_URL + "1222670" + "?json=1"
    response = requests.get(game_rev_url)
    data = response.json()
    for j in data["reviews"]:
        review_list.append(j["review"])
    current_game["reviews"] = review_list
    games.append(current_game)
    return games


def query_favorites(list_of_favoriteids):
    """Takes a list of game ID's as input and
    returns a list containing a useful dictionary
    for each game."""
    games = []
    i = 0
    for favid in list_of_favoriteids:
        # Acquire image and details url
        image_path = BASE_IMAGE_URL + str(favid) + "/header.jpg"
        details_path = BASE_DETAILS_URL + str(favid)
        response = requests.get(details_path)
        response_json = response.json()
        # Fill in details of current game using the JSON response from the details url
        current_game = {}
        current_game["image"] = image_path
        current_game["title"] = response_json["name"]
        current_game["price"] = response_json["price"]
        current_game["details"] = details_path
        current_game["gameid"] = favid
        games.append(current_game)
        i += 1
    if games:
        return games
        # If the API crashes, which it sometimes does,
        # return a single dictionary which contains info
        # about the Sims
    current_game = {}
    poster_path = BASE_IMAGE_URL + "1222670" + "/header.jpg"
    current_game["image"] = poster_path
    current_game["title"] = "The Sim's 4"
    current_game["price"] = 4000
    current_game["details"] = BASE_DETAILS_URL + "1222670"
    games.append(current_game)
    return games
