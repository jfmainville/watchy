import requests
import logging

logger = logging.getLogger(__name__)


def eztv_extract_tv_show_episodes(eztv_url, tmdb_show_id):
    # Extract the TV show episodes from the EZTV API
    eztv_shows = None
    try:
        eztv_shows_request = requests.get(eztv_url + "/api/get-torrents?imdb_id=" + tmdb_show_id)
        eztv_shows = eztv_shows_request.json()
    except requests.exceptions.ConnectionError as error:
        logger.error("requests connection error: %s", error)
    except requests.exceptions.Timeout as error:
        logger.error("requests connection timeout: %s", error)
    except requests.exceptions.HTTPError as error:
        logger.error("requests HTTP error: %s", error)

    if eztv_shows:
        return eztv_shows["torrents"]
    else:
        logger.error(
            "error while extracting the TV show episodes list from the EZTV REST API")
        return eztv_shows
