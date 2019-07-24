import os
import json
from authenticate import authenticate
from watchlist import tmdb_extract_watchlist_series, tmdb_extract_show_details
from folder import create_tv_show_folder, get_tv_show_folder_episodes
from eztv import eztv_extract_tv_show_episodes


# Local root folder for the TV shows
tv_shows_directory = "/app/watchy/tv/samples"
tv_shows_download_directory = "/app/watch/downloads/tv"

# TMDB API informations
tmdb_api_url = "api.themoviedb.org"
tmdb_username = os.environ.get('TMDB_USERNAME')
tmdb_password = os.environ.get('TMDB_PASSWORD')
tmdb_api_key = os.environ.get('TMDB_API_KEY')
tmdb_account_id = os.environ.get('TMDB_ACCOUNT_ID')

# Extract all the shows from the TMDB API
tmdb_session_id = authenticate(tmdb_api_url=tmdb_api_url, tmdb_username=tmdb_username,
                               tmdb_password=tmdb_password, tmdb_api_key=tmdb_api_key, tmdb_account_id=tmdb_account_id)

# Extract the shows details from the TMDB API
tmdb_shows = tmdb_extract_watchlist_series(
    tmdb_api_url=tmdb_api_url, tmdb_account_id=tmdb_account_id, tmdb_session_id=tmdb_session_id, tmdb_api_key=tmdb_api_key)

for tmdb_show in tmdb_shows:
    tmdb_show_details = tmdb_extract_show_details(tmdb_api_url=tmdb_api_url,
                                                  tmdb_api_key=tmdb_api_key, tmdb_show=tmdb_show)
    tmdb_show_id = (
        tmdb_show_details["external_ids"]["imdb_id"]).replace("tt", "")
    tmdb_show_name = tmdb_show["name"]
    tmdb_show_season = str(
        tmdb_show_details["last_episode_to_air"]["season_number"]).zfill(2)
    # Create the local TV show directory if it doesn't already exists
    create_tv_show_folder(
        tv_shows_directory=tv_shows_directory, show_name=tmdb_show_name)
    # List all the TV show episodes that were already downloaded
    tv_show_directory_episodes = get_tv_show_folder_episodes(
        tv_shows_directory=tv_shows_directory, show_name=tmdb_show_name)
    # Extract the list of the TV show episodes available on EZTV
    eztv_shows = eztv_extract_tv_show_episodes(tmdb_show_id=tmdb_show_id)
    eztv_show_dictionary = []
    for eztv_show in eztv_shows:
        eztv_show_title = eztv_show["title"]
        eztv_show_timestamp = eztv_show["date_released_unix"]
        eztv_show_seeds = eztv_show["seeds"]
        eztv_show_magnet = eztv_show["magnet_url"]

        # EZTV dictionnary creation
        tmdb_show_name_length = len(tmdb_show_name) + 7
        eztv_show_full_name = eztv_show_title[0:tmdb_show_name_length]
        eztv_show_dictionary.append({
            "name": eztv_show_full_name.title(),
            "seeds": eztv_show_seeds,
            "magnet": eztv_show_magnet,
            "timestamp": eztv_show_timestamp
        })
    for eztv_show_dictionary_item in eztv_show_dictionary:
        eztv_show_title = eztv_show_dictionary_item["name"]
        while eztv_show_title not in tv_show_directory_episodes:
            print(eztv_show_dictionary)
            break
