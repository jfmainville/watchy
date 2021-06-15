import json
import http.client
from json import JSONEncoder


def tmdb_authenticate(tmdb_api_url, tmdb_username, tmdb_password, tmdb_api_key):
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


def tmdb_extract_watchlist(tmdb_api_url, tmdb_account_id, tmdb_session_id, tmdb_api_key, tmdb_watchlist_content_type):
    # Send a GET request to get the list of series in the watchlist
    api_connection = http.client.HTTPSConnection(tmdb_api_url)
    api_connection.request("GET",
                           "/3/account/" + tmdb_account_id + "/watchlist/" + tmdb_watchlist_content_type + "?api_key=" +
                           tmdb_api_key + "&language=en-US&session_id=" + tmdb_session_id + "&sort_by=created_at.desc&page=1")
    watchlist_response = api_connection.getresponse()
    watchlist_data = watchlist_response.read()
    watchlist_content = json.loads(watchlist_data)

    watchlist_content_listdict = []

    if watchlist_content["total_pages"] > 1:
        for watchlist_page_number in range(1, watchlist_content["total_pages"] + 1):
            api_connection.request("GET",
                                   "/3/account/" + tmdb_account_id + "/watchlist/" + tmdb_watchlist_content_type + "?api_key=" +
                                   tmdb_api_key + "&language=en-US&session_id=" + tmdb_session_id + "&sort_by=created_at.desc" + "&page=" + str(
                                       watchlist_page_number))
            watchlist_response = api_connection.getresponse()
            watchlist_data = watchlist_response.read()
            watchlist_content = json.loads(watchlist_data)
            # Append the JSON data to the listdict to avoid multiple indexes
            for json_data in watchlist_content["results"]:
                watchlist_content_listdict.append(json_data)
    else:
        # Append the JSON data to the listdict to avoid multiple indexes
        for json_data in watchlist_content["results"]:
            watchlist_content_listdict.append(json_data)

    return watchlist_content_listdict


def tmdb_extract_movie_imdb_id(tmdb_api_url, tmdb_api_key, tmdb_watchlist_movie):
    # Send a GET request to extract the IMDB ID for each movie in the watchlist
    api_connection = http.client.HTTPSConnection(tmdb_api_url)
    api_connection.request("GET",
                           "/3/movie/" + str(tmdb_watchlist_movie["id"]) + "?api_key=" + tmdb_api_key)
    movie_imdb_id_response = api_connection.getresponse()
    movie_imdb_id_response_data = movie_imdb_id_response.read()
    movie_imdb_id = json.loads(movie_imdb_id_response_data)
    return movie_imdb_id["imdb_id"]


def tmdb_extract_movie_release_dates(tmdb_api_url, tmdb_api_key, tmdb_watchlist_movie):
    # Send a GET request to extract the movie release date for each movie in the watchlist
    api_connection = http.client.HTTPSConnection(tmdb_api_url)
    api_connection.request("GET",
                           "/3/movie/" + str(tmdb_watchlist_movie["id"]) + "/release_dates?api_key=" + tmdb_api_key)
    movie_release_dates_response = api_connection.getresponse()
    movie_release_dates_data = movie_release_dates_response.read()
    movie_release_dates = json.loads(movie_release_dates_data)
    return movie_release_dates


def tmdb_extract_show_details(tmdb_api_url, tmdb_api_key, tmdb_show):
    # Send a GET request to extract the details for each TV show in the watchlist
    api_connection = http.client.HTTPSConnection(tmdb_api_url)
    api_connection.request("GET",
                           "/3/tv/" + str(tmdb_show["id"])
                           + "?api_key=" + tmdb_api_key + "&language=en-US&append_to_response=external_ids")
    show_details_response = api_connection.getresponse()
    show_details_data = show_details_response.read()
    show_details = json.loads(show_details_data)
    return show_details
