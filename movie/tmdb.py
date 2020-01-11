import json
import http.client
import os
from json import JSONEncoder


def tmdb_authenticate(tmdb_api_url, tmdb_username, tmdb_password, tmdb_api_key, tmdb_account_id):
    # Send a GET request to receive the request token
    api_connection = http.client.HTTPSConnection(tmdb_api_url)
    headers = {
        "Content-Type": "application/json"
    }
    api_connection.request(
        "GET", "/3/authentication/token/new?api_key=" + tmdb_api_key)
    request_token_response = api_connection.getresponse()
    request_token_data = request_token_response.read()
    request_token = json.loads(request_token_data)['request_token']

    # Send a POST request to validate the request token with the username and password
    validate_with_login_payload = JSONEncoder().encode({
        "username": tmdb_username,
        "password": tmdb_password,
        "request_token": request_token
    })
    api_connection.request("POST", "/3/authentication/token/validate_with_login?api_key=" + tmdb_api_key,
                           validate_with_login_payload, headers=headers)
    tmdb_validate_login_response = api_connection.getresponse()
    tmdb_validate_login_response.read()

    # Send a POST request to get the session id
    request_token_payload = JSONEncoder().encode({
        "request_token": request_token
    })
    api_connection.request(
        "POST", "/3/authentication/session/new?api_key=" + tmdb_api_key, body=request_token_payload, headers=headers)
    tmdb_session_id_response = api_connection.getresponse()
    tmdb_session_id_data = tmdb_session_id_response.read()
    tmdb_session_id = json.loads(tmdb_session_id_data)['session_id']
    return tmdb_session_id


def tmdb_extract_watchlist_movies(tmdb_api_url, tmdb_account_id, tmdb_session_id, tmdb_api_key):
    # Send a GET request to get the list of series in the watchlist
    api_connection = http.client.HTTPSConnection(tmdb_api_url)
    api_connection.request("GET", "/3/account/" + tmdb_account_id + "/watchlist/movies?api_key=" +
                           tmdb_api_key + "&language=en-US&session_id=" + tmdb_session_id + "&sort_by=created_at.asc")
    watchlist_response = api_connection.getresponse()
    watchlist_data = watchlist_response.read()
    watchlist_series = json.loads(watchlist_data)
    return watchlist_series["results"]


def tmdb_extract_movie_release_dates(tmdb_api_url, tmdb_api_key, tmdb_watchlist_movie):
    # Send a GET request to extract the details for each movie in the watchlist
    api_connection = http.client.HTTPSConnection(tmdb_api_url)
    api_connection.request("GET",
                           "/3/movie/" + str(tmdb_watchlist_movie["id"]) + "/release_dates?api_key=" + tmdb_api_key)
    movie_release_dates_response = api_connection.getresponse()
    movie_release_dates_data = movie_release_dates_response.read()
    movie_release_dates = json.loads(movie_release_dates_data)
    return movie_release_dates