import os
import re
import time
import unidecode
from datetime import date
from tmdb import tmdb_authenticate, tmdb_extract_watchlist, tmdb_extract_movie_release_dates, tmdb_extract_show_details
from folder import create_content_folders, get_folder_content, move_content_file
from leet import leet_extract_movies
from eztv import eztv_extract_tv_show_episodes
from magnet import download_magnet_link
from dotenv import load_dotenv, find_dotenv
import argparse

in_docker = os.environ.get('IN_DOCKER')

if not in_docker:
    load_dotenv(find_dotenv())

# Movies main directory
movies_directory = os.environ.get('MOVIE_DIRECTORY')
# Movies download directory
movies_download_directory = os.environ.get('MOVIE_DOWNLOAD_DIRECTORY')

# TV shows main directory
tv_shows_directory = os.environ.get('TV_SHOW_DIRECTORY')
# TV shows download directory
tv_shows_download_directory = os.environ.get('TV_SHOW_DOWNLOAD_DIRECTORY')

# TMDB API information
eztv_url = os.environ.get('EZTV_URL')
leet_url = os.environ.get('LEET_URL')
tmdb_api_url = os.environ.get('TMDB_API_URL')
tmdb_username = os.environ.get('TMDB_USERNAME')
tmdb_password = os.environ.get('TMDB_PASSWORD')
tmdb_api_key = os.environ.get('TMDB_API_KEY')
tmdb_account_id = os.environ.get('TMDB_ACCOUNT_ID')

# Parser to determine which function to execute
parser = argparse.ArgumentParser(description='type selector')
parser.add_argument("--movie", "-m", dest="movie", action="store_true", help="execute the movie related function")
parser.add_argument("--tv", "-t", dest="tv", action="store_true", help='execute the TV show related function')

args = parser.parse_args()

# Extract all the movies from the TMDB API
tmdb_session_id = tmdb_authenticate(tmdb_api_url=tmdb_api_url, tmdb_username=tmdb_username,
                                    tmdb_password=tmdb_password, tmdb_api_key=tmdb_api_key)


def movie():
    # Extract the movies details from the TMDB API
    tmdb_watchlist_movies = tmdb_extract_watchlist(
        tmdb_api_url=tmdb_api_url, tmdb_account_id=tmdb_account_id, tmdb_session_id=tmdb_session_id,
        tmdb_api_key=tmdb_api_key, tmdb_watchlist_content_type="movies")

    for tmdb_watchlist_movie in tmdb_watchlist_movies:
        tmdb_movie_release_dates = tmdb_extract_movie_release_dates(tmdb_api_url=tmdb_api_url,
                                                                    tmdb_api_key=tmdb_api_key,
                                                                    tmdb_watchlist_movie=tmdb_watchlist_movie)
        tmdb_movie_title = unidecode.unidecode(tmdb_watchlist_movie["title"])
        tmdb_movie_release_year = (
            tmdb_watchlist_movie["release_date"]).split("-")[0]
        tmdb_movie_dvd_release_date = []
        for tmdb_movie_release_date in tmdb_movie_release_dates["results"]:
            for release_dates in tmdb_movie_release_date["release_dates"]:
                # Check that the release date is set
                if release_dates["type"] == 4 or release_dates["type"] == 5:
                    tmdb_movie_dvd_release_date.append(
                        release_dates["release_date"].split("T")[0])
        # Create the local movies directory if it doesn't already exists
        create_content_folders(
            content_folder=movies_directory, content_download_folder=movies_download_directory, content_title=None)
        # List all the movies that were already downloaded
        local_movies = get_folder_content(content_folder=movies_directory, content_title=None)
        if tmdb_movie_dvd_release_date:
            # Convert the DVD release date to a time format
            tmdb_movie_dvd_release_date_convert = time.strptime(
                str(tmdb_movie_dvd_release_date[0]), "%Y-%m-%d")
        else:
            tmdb_movie_dvd_release_date_convert = time.strptime(
                str(date.today()), "%Y-%m-%d")
        today = time.strptime(str(date.today()), "%Y-%m-%d")
        # Check if the DVD release date is earlier than today
        if tmdb_movie_dvd_release_date_convert < today:
            # Extract the 1337x amount of seeds and magnet link for each movie
            seeds, magnet_link = leet_extract_movies(movie_title=tmdb_movie_title,
                                                     movie_release_year=tmdb_movie_release_year, leet_url=leet_url)
            if seeds and magnet_link:
                # Movie dictionary that contains the required movie information to download it
                download_movie = {}
                tmdb_movie_title_full = (tmdb_movie_title.replace(
                    ":", " -")) + " (" + tmdb_movie_release_year + ")"
                while tmdb_movie_title_full not in local_movies:
                    # Add the movies that needs to be downloaded to the list
                    download_movie.update({
                        "title": tmdb_movie_title_full,
                        "seeds": int(seeds),
                        "magnet": magnet_link
                    })
                    break
                if download_movie != {}:
                    # Download the movie magnet using the aria2 application
                    return_code = download_magnet_link(download_entry=download_movie,
                                                       download_directory=movies_download_directory)
                    # Move the movie download file to the movies directory
                    move_content_file(download_file=download_movie, content_download_folder=movies_download_directory,
                                      content_folder=movies_directory, content_title=None, return_code=return_code)


def tv_show():
    # Extract the shows details from the TMDB API
    tmdb_shows = tmdb_extract_watchlist(
        tmdb_api_url=tmdb_api_url, tmdb_account_id=tmdb_account_id, tmdb_session_id=tmdb_session_id,
        tmdb_api_key=tmdb_api_key, tmdb_watchlist_content_type="tv")

    for tmdb_show in tmdb_shows:
        tmdb_show_details = tmdb_extract_show_details(tmdb_api_url=tmdb_api_url,
                                                      tmdb_api_key=tmdb_api_key, tmdb_show=tmdb_show)
        tmdb_show_id = (
            tmdb_show_details["external_ids"]["imdb_id"]).replace("tt", "")
        tmdb_show_name = re.sub('[^a-zA-Z0-9 \n]', '', unidecode.unidecode(tmdb_show["name"]))
        # Create the local TV show directory if it doesn't already exists
        create_content_folders(
            content_folder=tv_shows_directory, content_download_folder=tv_shows_download_directory,
            content_title=tmdb_show_name)
        # List all the TV show episodes that were already downloaded
        tv_show_directory_episodes = get_folder_content(
            content_folder=tv_shows_directory, content_title=tmdb_show_name)
        # Extract the list of the TV show episodes available on EZTV
        eztv_shows = eztv_extract_tv_show_episodes(tmdb_show_id=tmdb_show_id, eztv_url=eztv_url)
        eztv_show_listdict = []
        for eztv_show in eztv_shows:
            eztv_show_title = eztv_show["title"]
            eztv_show_timestamp = eztv_show["date_released_unix"]
            eztv_show_seeds = eztv_show["seeds"]
            eztv_show_magnet = eztv_show["magnet_url"]

            # EZTV dictionary creation
            tmdb_show_name_length = len(tmdb_show_name) + 7
            eztv_show_full_name = (
                eztv_show_title[0:tmdb_show_name_length]).title()
            if tmdb_show_name.lower() in eztv_show_full_name.lower():
                eztv_show_listdict.append({
                    "name": eztv_show_full_name,
                    "seeds": eztv_show_seeds,
                    "magnet": eztv_show_magnet,
                    "timestamp": eztv_show_timestamp
                })
        # Refactor the eztv_show_listdict list dictionary to only show unique values
        filtered_eztv_show_listdict = list(
            {value['name']: value for value in eztv_show_listdict}.values())
        # TV show  list that contains all the files that needs to be downloaded
        download_tv_shows = []
        for filtered_eztv_show_dictionary_item in filtered_eztv_show_listdict:
            eztv_show_title = filtered_eztv_show_dictionary_item["name"]
            while eztv_show_title not in tv_show_directory_episodes:
                # Add the TV show episodes that needs to be downloaded to the list
                download_tv_shows.append({
                    "title": filtered_eztv_show_dictionary_item["name"],
                    "seeds": filtered_eztv_show_dictionary_item["seeds"],
                    "magnet": filtered_eztv_show_dictionary_item["magnet"]
                })
                break
        for download_tv_show in download_tv_shows:
            # Download the TV show magnet using the aria2 application
            return_code = download_magnet_link(download_entry=download_tv_show,
                                               download_directory=tv_shows_download_directory)
            # Move the TV show download file to the TV shows directory
            move_content_file(download_file=download_tv_show,
                              content_download_folder=tv_shows_download_directory,
                              content_folder=tv_shows_directory, content_title=tmdb_show_name,
                              return_code=return_code)


if args.movie:
    # Execute the movie function
    movie()
elif args.tv:
    # Execute the TV show function
    tv_show()
