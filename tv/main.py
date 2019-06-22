import os
import json
from authenticate import authenticate
from watchlist import extract_watchlist_series, extract_show_details
from folder import create_tv_show_folder, get_tv_show_folder_episodes


# Local root folder for the TV shows
tv_shows_directory = "/app/watchy/tv/samples"

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
shows = extract_watchlist_series(
    tmdb_api_url=tmdb_api_url, tmdb_account_id=tmdb_account_id, tmdb_session_id=tmdb_session_id, tmdb_api_key=tmdb_api_key)

for show in shows:
    show_details = extract_show_details(tmdb_api_url=tmdb_api_url,
                                        tmdb_api_key=tmdb_api_key, show=show)
    show_name = show["name"]
    show_season = str(
        show_details["last_episode_to_air"]["season_number"]).zfill(2)
    # Create the local TV show directory if it doesn't already exists
    create_tv_show_folder(
        tv_shows_directory=tv_shows_directory, show_name=show_name)
