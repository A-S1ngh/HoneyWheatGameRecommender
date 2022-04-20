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
        "racing": survey_data.racing
    }
    total = sum(genres.values())
    games = []

    selected_ids = set()
    for genre, rating in sorted(genres.items(), key=lambda item: item[1], reverse=True):
        genreURL = BASE_GENRE_URL + genre  # create the api call to games in this genre
        response = requests.get(genreURL)
        response = response.json()
        id_list = list(response)
        numOfGames = floor((rating / total) * 36)
        if id_list:
            for i in range(numOfGames):
                randID = random.randint(1,100)
                while(id_list[randID] in selected_ids):
                    randID = random.randint(1,100)
                selected_ids.add(id_list[randID])
                current_game = {}  # below code adds all game details to its own dictionary
                GAME_REVIEW_URl = REVIEWS_URL + str(id_list[randID]) + "?json=1"
                res = requests.get(GAME_REVIEW_URl)
                review_list = []
                data = res.json()
                for j in data['reviews']:
                    review_list.append(j['review'])

                current_game["reviews"] = tuple(review_list)
                details_path = BASE_DETAILS_URL + str(id_list[randID])
                current_game["details"] = details_path
                poster_path = BASE_IMAGE_URL + str(id_list[randID]) + "/header.jpg"
                current_game["image"] = poster_path
                current_game["title"] = str(response[id_list[randID]]["name"])
                current_game["price"] = int(response[id_list[randID]]["price"])
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
    GAME_REVIEW_URl = REVIEWS_URL + "1222670" + "?json=1"
    response = requests.get(GAME_REVIEW_URl)
    data = response.json()
    for j in data['reviews']:
      review_list.append(j['review'])
    current_game["reviews"] = review_list
    games.append(current_game)
    return games

