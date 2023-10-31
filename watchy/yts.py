import logging

import requests

logger = logging.getLogger(__name__)


def yts_extract_movie_torrent(yts_url, movie_imdb_id, movie_title):
    # Extract the movie torrent data for each movie in the watchlist
    yts_movie = None
    try:
        yts_movie_request = requests.get(yts_url +
                                         "/api/v2/list_movies.json?quality=720p&sort=seeds&limit=5&query_term=" +
                                         str(movie_imdb_id))
        yts_movie = yts_movie_request.json()
    except requests.exceptions.ConnectionError as error:
        logger.error("requests connection error: %s", error)
    except requests.exceptions.Timeout as error:
        logger.error("requests connection timeout: %s", error)
    except requests.exceptions.HTTPError as error:
        logger.error("requests HTTP error: %s", error)

    torrent_trackers = "&dn=Url+Encoded+Movie+Name&tr=udp://open.demonii.com:1337/announce&tr=udp://tracker.openbittorrent.com:80&tr=udp://tracker.coppersurfer.tk:6969"

    if yts_movie:
        try:
            seeds = yts_movie["data"]["movies"][0]["torrents"][0]["seeds"]
            magnet_link = "magnet:?xt=urn:btih:" + yts_movie["data"]["movies"][0]["torrents"][0][
                "hash"] + torrent_trackers
            return seeds, magnet_link
        except KeyError:
            logger.warning("the movie %s isn't yet available on the YTS platform", movie_title)
            return None, None
