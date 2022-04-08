import os
import requests
from dotenv import find_dotenv, load_dotenv
from models import Survey

load_dotenv(find_dotenv())

IMAGE_URL = os.getenv("IMAGE_URL")
GENRE_URL = os.getenv("GENRE_URL")
DETAILS_URL = os.getenv("DETAILS_URL")


def querygames(survey_data, userid):
    """querygames"""
    user_data = survey_data
    action = user_data.action
    adventure = user_data.adventure
    roleplaying = user_data.roleplaying
    strategy = user_data.strategy
    sports = user_data.sports
    simulation = user_data.simulation
    racing = user_data.racing
    genres = {
        "action": action,
        "adventure" : adventure,
        "roleplaying": roleplaying,
        "strategy": strategy,
        "sports": sports,
        "simulation": simulation,
        "racing": racing
    }
    games = []
   
    # In the end this method should take a list of genres as a parameter and query a certain (random?) amount of games from each genre.
    # Currently this method only searches for games of a single genre
    # will add more specific game tags when we have more things worked out

    image = []  # collect poster images
    details = []  # keep path to details for individual game pages
    title = []  # collect game titles
    price = []  # collect game prices


    for genrename in genres.keys():
        genre = GENRE_URL + genrename #create the api call to games in this genre
        response = requests.get(genre)
        response_json = response.json() 
        appid = list(response_json)[:5] #grabs the first 5 results of the json response
      
        for i in range(len(appid)): #work gets done for each genre call
            current_game = {}
            details_path = DETAILS_URL + str(appid[i])
            current_game["details"] = details_path
            # adds the current game details path to the details list
            poster_path = IMAGE_URL + str(appid[i]) + "/header.jpg"
            current_game["image"] = poster_path
            current_game["title"] = str(response_json[appid[i]]["name"])
            current_game["price"] = int(response_json[appid[i]]["price"])
            games.append(current_game)
            #if price == 0:  # For better formatting than "$0"
                #price[i] = "Free to Play"
            games = [dict(tupleized) for tupleized in set(tuple(game.items()) for game in games)]
    return games
