import os
import json
from tmdb import tmdb_authenticate, tmdb_extract_watchlist_movies, tmdb_extract_movie_release_dates
from folder import create_movie_folders, get_local_movies, move_local_movie
# from leet import leet_extract_movies
# from magnet import download_magnet_link


# Movies main directory
movies_directory = "/app/watchy/movie/samples"
# Movies download directory
movies_download_directory = "/app/watchy/downloads/movie"

# TMDB API informations
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
    for tmdb_movie_release_date in tmdb_movie_release_dates["results"]:
        for release_dates in tmdb_movie_release_date["release_dates"]:
            # Check that the rel
            if release_dates["type"] == 4 and tmdb_movie_release_date["iso_3166_1"] == "BR":
                tmdb_movie_dvd_release_date = (
                    release_dates["release_date"]).split("T")[0]
    # Create the local movies directory if it doesn't already exists
    create_movie_folders(
        movies_directory=movies_directory, movies_download_directory=movies_download_directory, movie_title=tmdb_movie_title)
    # List all the movies that were already downloaded
    local_movies = get_local_movies(
        movies_directory=movies_directory, movie_title=tmdb_movie_title)
#    # Movie dictionnary list that contains all the files that needs to be downloaded
#    download_movies=[]
#    for filtered_movie_dictionary_item in filtered_movie_listdict:
#        movie_title=filtered_movie_dictionary_item["name"]
#        while movie_title not in movies_directory:
#            # Add the movies that needs to be downloaded to the list
#            download_movies.append({
#                "title": filtered_movie_dictionary_item["title"],
#                "seeds": filtered_movie_dictionary_item["seeds"],
#                "magnet": filtered_movie_dictionary_item["magnet"]
#            })
#            break
#    for download_movie in download_movies:
#        # Download the movie magnet using the aria2 application
#        returncode=download_magnet_link(download_movie = download_movie,
#                                          movies_download_directory = movies_download_directory)
#        # Move the movie download file to the movies directory
#        move_local_movie(download_movie=download_movie, movies_download_directory=movies_download_directory,
#                              movies_directory=movies_directory, movie_title=tmdb_movie_title, returncode=returncode)
