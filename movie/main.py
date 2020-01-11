import os
import json
from datetime import date
import time
from tmdb import tmdb_authenticate, tmdb_extract_watchlist_movies, tmdb_extract_movie_release_dates
from folder import create_movie_folders, get_local_movies, move_local_movie
from leet import leet_extract_movies
from magnet import download_magnet_link


# Movies main directory
movies_directory = os.environ.get('MOVIE_DIRECTORY')
# Movies download directory
movies_download_directory = os.environ.get('MOVIE_DOWNLOAD_DIRECTORY')

# TMDB API information
tmdb_api_url = "api.themoviedb.org"
tmdb_username = os.environ.get('TMDB_USERNAME')
tmdb_password = os.environ.get('TMDB_PASSWORD')
tmdb_api_key = os.environ.get('TMDB_API_KEY')
tmdb_account_id = os.environ.get('TMDB_ACCOUNT_ID')

# Extract all the movies from the TMDB API
tmdb_session_id = tmdb_authenticate(tmdb_api_url=tmdb_api_url, tmdb_username=tmdb_username,
                                    tmdb_password=tmdb_password, tmdb_api_key=tmdb_api_key, tmdb_account_id=tmdb_account_id)

# Extract the movies details from the TMDB API
tmdb_watchlist_movies = tmdb_extract_watchlist_movies(
    tmdb_api_url=tmdb_api_url, tmdb_account_id=tmdb_account_id, tmdb_session_id=tmdb_session_id, tmdb_api_key=tmdb_api_key)

for tmdb_watchlist_movie in tmdb_watchlist_movies:
    tmdb_movie_release_dates = tmdb_extract_movie_release_dates(tmdb_api_url=tmdb_api_url,
                                                                tmdb_api_key=tmdb_api_key, tmdb_watchlist_movie=tmdb_watchlist_movie)
    tmdb_movie_title = tmdb_watchlist_movie["title"]
    tmdb_movie_release_year = (
        tmdb_watchlist_movie["release_date"]).split("-")[0]
    tmdb_movie_dvd_release_date = []
    for tmdb_movie_release_date in tmdb_movie_release_dates["results"]:
        for release_dates in tmdb_movie_release_date["release_dates"]:
            # Check that the release date is set
            if release_dates["type"] == 4 and tmdb_movie_release_date["iso_3166_1"] == "BR":
                tmdb_movie_dvd_release_date.append(
                    release_dates["release_date"].split("T")[0])
    # Create the local movies directory if it doesn't already exists
    create_movie_folders(
        movies_directory=movies_directory, movies_download_directory=movies_download_directory, movie_title=tmdb_movie_title)
    # List all the movies that were already downloaded
    local_movies = get_local_movies(
        movies_directory=movies_directory, movie_title=tmdb_movie_title)
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
        seeds, magnet_link = leet_extract_movies(movie_title=tmdb_movie_title)
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
            returncode = download_magnet_link(download_movie=download_movie,
                                              movies_download_directory=movies_download_directory)
            # Move the movie download file to the movies directory
            move_local_movie(download_movie=download_movie, movies_download_directory=movies_download_directory,
                             movies_directory=movies_directory, movie_title=tmdb_movie_title, returncode=returncode)
