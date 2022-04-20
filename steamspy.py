"""Steam Spy API Functions"""
import os
import requests
from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv())

IMAGE_URL = os.getenv("IMAGE_URL")
GENRE_URL = os.getenv("GENRE_URL")
DETAILS_URL = os.getenv("DETAILS_URL")


def querygames(survey_data):
    """querygames"""
    user_data = survey_data  # pull ratings for each genre for the current user
    action = user_data.action
    adventure = user_data.adventure
    roleplaying = user_data.roleplaying
    strategy = user_data.strategy
    sports = user_data.sports
    simulation = user_data.simulation
    racing = user_data.racing
    genres = {
        "action": action,
        "adventure": adventure,
        "roleplaying": roleplaying,
        "strategy": strategy,
        "sports": sports,
        "simulation": simulation,
        "racing": racing,
    }
    games = []

    for genrename in genres:
        if genres[genrename] > 1:  # No results for genres with a 1
            genre = GENRE_URL + genrename  # create the api call to games in this genre
            response = requests.get(genre)
            response_json = response.json()
            if genres[genrename] > 7:  # Covers 10-8
                results = slice(0, 8)
            elif genres[genrename] > 4:  # Covers 7-5
                results = slice(0, 6)
            else:  # Covers 4-2
                results = slice(0, 3)
            appid = list(response_json)[results]
            for i in range(len(appid)):  # work gets done for each genre call
                current_game = (
                    {}
                )  # below code adds all game details to its own dictionary
                details_path = DETAILS_URL + str(appid[i])
                current_game["details"] = details_path
                poster_path = IMAGE_URL + str(appid[i]) + "/header.jpg"
                current_game["image"] = poster_path
                current_game["title"] = str(response_json[appid[i]]["name"])
                current_game["price"] = int(response_json[appid[i]]["price"])
                current_game["gameid"] = appid[i]
                games.append(current_game)
                games = [
                    dict(tupleized)
                    for tupleized in set(tuple(game.items()) for game in games)
                ]
    if games:
        return games
    current_game = {}
    poster_path = IMAGE_URL + "1222670" + "/header.jpg"
    current_game["image"] = poster_path
    current_game["title"] = "The Sim's 4"
    current_game["price"] = 4000
    current_game["details"] = DETAILS_URL + "1222670"
    games.append(current_game)
    return games


def query_favorites(list_of_favoriteids):
    games = []
    i = 0
    for favid in list_of_favoriteids:
        image_path = IMAGE_URL + str(favid) + "/header.jpg"
        details_path = DETAILS_URL + str(favid)
        response = requests.get(details_path)
        response_json = response.json()
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
    else:
        current_game = {}
        poster_path = IMAGE_URL + "1222670" + "/header.jpg"
        current_game["image"] = poster_path
        current_game["title"] = "The Sim's 4"
        current_game["price"] = 4000
        current_game["details"] = DETAILS_URL + "1222670"
        games.append(current_game)
        return games
