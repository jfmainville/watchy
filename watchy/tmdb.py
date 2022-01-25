import requests
import logging

logger = logging.getLogger(__name__)


def tmdb_authenticate(tmdb_api_url, tmdb_username, tmdb_password, tmdb_api_key):
    # Complete the authentication process for the defined user account
    request_token = None
    tmdb_validate_login_response = None
    tmdb_session_id = None

    headers = {
        "Content-Type": "application/json"
    }

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

    # Validate the request token with the username and password of the user account
    if request_token:
        validate_login_payload = {
            "username": tmdb_username,
            "password": tmdb_password,
            "request_token": request_token
        }
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
            # Get the session ID for the user account
            request_token_payload = {
                "request_token": request_token
            }
            try:
                tmdb_session_id_data = requests.post(tmdb_api_url +
                                                     "/3/authentication/session/new?api_key=" + tmdb_api_key,
                                                     params=request_token_payload,
                                                     headers=headers)
                tmdb_session_id = tmdb_session_id_data.json()['session_id']
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


def tmdb_remove_session(tmdb_api_url, tmdb_session_id, tmdb_api_key):
    # Remove the TMDB session ID once the data extraction is completed
    headers = {
        "Content-Type": "application/json"
    }

    request_session_id = {
        "session_id": tmdb_session_id
    }

    try:
        requests.delete(tmdb_api_url +
                        "/3/authentication/session?api_key=" + tmdb_api_key,
                        params=request_session_id, headers=headers)
    except requests.exceptions.ConnectionError as error:
        logger.error("requests connection error: %s", error)
    except requests.exceptions.Timeout as error:
        logger.error("requests connection timeout: %s", error)
    except requests.exceptions.HTTPError as error:
        logger.error("requests HTTP error: %s", error)


def tmdb_extract_watchlist(tmdb_api_url, tmdb_account_id, tmdb_session_id, tmdb_api_key, tmdb_watchlist_content_type):
    # Extract the list of content in the watchlist
    watchlist_content = None
    try:
        watchlist_content_request = requests.get(tmdb_api_url +
                                                 "/3/account/" + tmdb_account_id + "/watchlist/" + tmdb_watchlist_content_type + "?api_key=" +
                                                 tmdb_api_key + "&language=en-US&session_id=" + tmdb_session_id + "&sort_by=created_at.desc&page=1")
        watchlist_content = watchlist_content_request.json()
    except requests.exceptions.ConnectionError as error:
        logger.error("requests connection error: %s", error)
    except requests.exceptions.Timeout as error:
        logger.error("requests connection timeout: %s", error)
    except requests.exceptions.HTTPError as error:
        logger.error("requests HTTP error: %s", error)

    watchlist_content_listdict = []

    if watchlist_content:
        if watchlist_content["total_pages"] > 1:
            for watchlist_page_number in range(1, watchlist_content["total_pages"] + 1):
                try:
                    watchlist_content_request = requests.get(tmdb_api_url +
                                                             "/3/account/" + tmdb_account_id + "/watchlist/" + tmdb_watchlist_content_type + "?api_key=" +
                                                             tmdb_api_key + "&language=en-US&session_id=" + tmdb_session_id + "&sort_by=created_at.desc" + "&page=" + str(
                        watchlist_page_number))
                    watchlist_content = watchlist_content_request.json()
                except requests.exceptions.ConnectionError as error:
                    logger.error("requests connection error: %s", error)
                except requests.exceptions.Timeout as error:
                    logger.error("requests connection timeout: %s", error)
                except requests.exceptions.HTTPError as error:
                    logger.error("requests HTTP error: %s", error)

                # Append the JSON data to the listdict to avoid multiple indexes
                for json_data in watchlist_content["results"]:
                    watchlist_content_listdict.append(json_data)
        else:
            # Append the JSON data to the listdict to avoid multiple indexes
            for json_data in watchlist_content["results"]:
                watchlist_content_listdict.append(json_data)

        return watchlist_content_listdict
    else:
        logger.info("no content in the watchlist")
        return None


def tmdb_extract_movie_imdb_id(tmdb_api_url, tmdb_api_key, tmdb_watchlist_movie):
    # Extract the IMDB ID for each movie in the watchlist
    movie_imdb_id = None
    try:
        movie_imdb_id_request = requests.get(tmdb_api_url +
                                             "/3/movie/" + str(tmdb_watchlist_movie["id"]) + "?api_key=" + tmdb_api_key)
        movie_imdb_id = movie_imdb_id_request.json()
    except requests.exceptions.ConnectionError as error:
        logger.error("requests connection error: %s", error)
    except requests.exceptions.Timeout as error:
        logger.error("requests connection timeout: %s", error)
    except requests.exceptions.HTTPError as error:
        logger.error("requests HTTP error: %s", error)

    if movie_imdb_id:
        return movie_imdb_id["imdb_id"]
    else:
        logger.error("unable to extract the IMDB ID for the %s movie", tmdb_watchlist_movie["title"])
        return movie_imdb_id


def tmdb_extract_movie_release_dates(tmdb_api_url, tmdb_api_key, tmdb_watchlist_movie):
    # Extract the details for each movie in the watchlist
    movie_release_dates = None
    try:
        movie_release_dates_request = requests.get(tmdb_api_url +
                                                   "/3/movie/" + str(
            tmdb_watchlist_movie["id"]) + "/release_dates?api_key=" + tmdb_api_key)
        movie_release_dates = movie_release_dates_request.json()
    except requests.exceptions.ConnectionError as error:
        logger.error("requests connection error: %s", error)
    except requests.exceptions.Timeout as error:
        logger.error("requests connection timeout: %s", error)
    except requests.exceptions.HTTPError as error:
        logger.error("requests HTTP error: %s", error)

    if movie_release_dates:
        return movie_release_dates
    else:
        logger.warning("unable to extract the release date for the %s movie", tmdb_watchlist_movie["title"])
        return movie_release_dates


def tmdb_extract_show_details(tmdb_api_url, tmdb_api_key, tmdb_show):
    # Extract the details for each TV show in the watchlist
    show_details = None
    try:
        tmdb_show_id = str(tmdb_show["id"])
        show_details_request = requests.get(tmdb_api_url +
                                            "/3/tv/" + tmdb_show_id + "?api_key=" + tmdb_api_key + "&language=en-US&append_to_response=external_ids")
        show_details = show_details_request.json()
    except requests.exceptions.ConnectionError as error:
        logger.error("requests connection error: %s", error)
    except requests.exceptions.Timeout as error:
        logger.error("requests connection timeout: %s", error)
    except requests.exceptions.HTTPError as error:
        logger.error("requests HTTP error: %s", error)
    if show_details:
        return show_details
    else:
        logger.warning("unable to extract the details for the %s TV show",
                       tmdb_show["name"])
        return show_details


def tmdb_remove_watchlist_movie(tmdb_api_url, tmdb_account_id, tmdb_session_id, tmdb_api_key, tmdb_watchlist_movie):
    # Remove the movie from the watchlist

    try:
        tmdb_movie_id = str(tmdb_watchlist_movie["id"])
        tmdb_movie_data = {
            "media_type": "movie",
            "media_id": tmdb_movie_id,
            "watchlist": False
        }
        movie_watchlist_status = requests.post(
            tmdb_api_url + "/3/account/" + tmdb_account_id + "/watchlist?api_key=" + tmdb_api_key + "&session_id=" + tmdb_session_id,
            json=tmdb_movie_data)
        print(movie_watchlist_status)
    except requests.exceptions.ConnectionError as error:
        logger.error("requests connection error: %s", error)
    except requests.exceptions.Timeout as error:
        logger.error("requests connection timeout: %s", error)
    except requests.exceptions.HTTPError as error:
        logger.error("requests HTTP error: %s", error)
    if movie_watchlist_status.status_code == 200:
        logger.info("successfully removed the movie %s from the watchlist",
                    tmdb_watchlist_movie["title"])
    else:
        logger.error("failed to remove the movie %s from the watchlist",
                     tmdb_watchlist_movie["title"])
