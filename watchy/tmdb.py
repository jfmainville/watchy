import requests
import logging

logger = logging.getLogger(__name__)


def tmdb_authenticate(tmdb_api_url, tmdb_username, tmdb_password, tmdb_api_key):
    # Send a GET request to receive the request token
    headers = {
        "Content-Type": "application/json"
    }
    request_token = None
    try:
        request_token_data = requests.get(tmdb_api_url +
                                          "/3/authentication/token/new?api_key=" + tmdb_api_key, headers=headers)
        request_token = request_token_data.json()['request_token']
    except requests.exceptions.ConnectionError as error:
        logger.error("requests connection error: %s", error)
    except requests.exceptions.Timeout as error:
        logger.error("requests connection timeout: %s", error)
    except requests.exceptions.HTTPError as error:
        logger.error("requests HTTP error: %s", error)

    # Send a POST request to validate the request token with the username and password
    if request_token:
        validate_login_payload = {
            "username": tmdb_username,
            "password": tmdb_password,
            "request_token": request_token
        }
        tmdb_validate_login_response = None
        try:
            tmdb_validate_login_response = requests.post(
                tmdb_api_url + "/3/authentication/token/validate_with_login?api_key=" + tmdb_api_key,
                params=validate_login_payload, headers=headers)
        except requests.exceptions.ConnectionError as error:
            logger.error("requests connection error: %s", error)
        except requests.exceptions.Timeout as error:
            logger.error("requests connection timeout: %s", error)
        except requests.exceptions.HTTPError as error:
            logger.error("requests HTTP error: %s", error)

        tmdb_session_id = None

        if tmdb_validate_login_response and tmdb_validate_login_response.status_code == 200:
            # Send a POST request to get the session ID
            request_token_payload = {
                "request_token": request_token
            }

            try:
                tmdb_session_id = requests.post(tmdb_api_url +
                                                "/3/authentication/session/new?api_key=" + tmdb_api_key,
                                                params=request_token_payload,
                                                headers=headers)
                tmdb_session_id = tmdb_session_id.json()['session_id']
            except requests.exceptions.ConnectionError as error:
                logger.error("requests connection error: %s", error)
            except requests.exceptions.Timeout as error:
                logger.error("requests connection timeout: %s", error)
            except requests.exceptions.HTTPError as error:
                logger.error("requests HTTP error: %s", error)

    if request_token and tmdb_session_id:
        return tmdb_session_id
    else:
        logger.error("failed to authenticate the user")
        return request_token


def tmdb_extract_watchlist(tmdb_api_url, tmdb_account_id, tmdb_session_id, tmdb_api_key, tmdb_watchlist_content_type):
    # Send a GET request to get the list of series in the watchlist
    watchlist_content_request = requests.get(tmdb_api_url +
                                             "/3/account/" + tmdb_account_id + "/watchlist/" + tmdb_watchlist_content_type + "?api_key=" +
                                             tmdb_api_key + "&language=en-US&session_id=" + tmdb_session_id + "&sort_by=created_at.desc&page=1")
    watchlist_content = watchlist_content_request.json()

    watchlist_content_listdict = []

    if watchlist_content["total_pages"] > 1:
        for watchlist_page_number in range(1, watchlist_content["total_pages"] + 1):
            watchlist_content_request = requests.get(tmdb_api_url +
                                                     "/3/account/" + tmdb_account_id + "/watchlist/" + tmdb_watchlist_content_type + "?api_key=" +
                                                     tmdb_api_key + "&language=en-US&session_id=" + tmdb_session_id + "&sort_by=created_at.desc" + "&page=" + str(
                watchlist_page_number))
            watchlist_content = watchlist_content_request.json()
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
    movie_imdb_id_request = requests.get(tmdb_api_url +
                                         "/3/movie/" + str(tmdb_watchlist_movie["id"]) + "?api_key=" + tmdb_api_key)
    movie_imdb_id = movie_imdb_id_request.json()
    return movie_imdb_id["imdb_id"]


def tmdb_extract_movie_release_dates(tmdb_api_url, tmdb_api_key, tmdb_watchlist_movie):
    # Send a GET request to extract the details for each movie in the watchlist
    movie_release_dates_request = requests.get(tmdb_api_url +
                                               "/3/movie/" + str(
        tmdb_watchlist_movie["id"]) + "/release_dates?api_key=" + tmdb_api_key)
    movie_release_dates = movie_release_dates_request.json()
    return movie_release_dates


def tmdb_extract_show_details(tmdb_api_url, tmdb_api_key, tmdb_show):
    # Send a GET request to extract the details for each TV show in the watchlist
    tmdb_show_id = str(tmdb_show["id"])
    show_details_request = requests.get(tmdb_api_url +
                                        "/3/tv/" + tmdb_show_id + "?api_key=" + tmdb_api_key + "&language=en-US&append_to_response=external_ids")
    show_details = show_details_request.json()
    return show_details
