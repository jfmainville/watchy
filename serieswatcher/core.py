import os
import json
from json import JSONEncoder
from eztv_extract import eztv_extract
from tmdb_extract_watchlist import extract_watchlist_series
from tmdb_api_connection import tmdb_api_connection

# Execute the tmdb_api_connection function to extract the user information
api_connection = tmdb_api_connection(os.environ.get('TMDB_USERNAME'),
                                     os.environ.get('TMDB_PASSWORD'),
                                     os.environ.get('TMDB_API_KEY'),
                                     os.environ.get('TMDB_ACCOUNT_ID')
                                     )

shows = extract_watchlist_series()

for show in shows:
    api_connection["connection"].request("GET",
                                         "/3/tv/" + str(show["id"]) + "?api_key=" + api_connection["api_key"] + "&language=en-US")
    show_details_response = api_connection["connection"].getresponse()
    show_details_data = show_details_response.read()
    show_details = json.loads(show_details_data)
    show_name = show["name"]
    show_season = str(
        show_details["last_episode_to_air"]["season_number"]).zfill(2)
    episodes = eztv_extract(show_name, show_season)
