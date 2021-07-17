import requests
import logging

logger = logging.getLogger(__name__)


def yts_extract_movie_torrent(yts_url, movie_imdb_id):
    # Extract the movie torrent data for each movie in the watchlist
    yts_movie = None
    try:
        yts_movie_request = requests.get(yts_url +
                                         "/api/v2/list_movies.json?sort=seeds&limit=5&query_term=" + str(movie_imdb_id))
        yts_movie = yts_movie_request.json()
    except requests.exceptions.ConnectionError as error:
        logger.error("requests connection error: %s", error)
    except requests.exceptions.Timeout as error:
        logger.error("requests connection timeout: %s", error)
    except requests.exceptions.HTTPError as error:
        logger.error("requests HTTP error: %s", error)

    torrent_trackers = "&dn=Url+Encoded+Movie+Name&tr=udp://open.demonii.com:1337/announce&tr=udp://tracker.openbittorrent.com:80&tr=udp://tracker.coppersurfer.tk:6969"

    if yts_movie:
        seeds = yts_movie["data"]["movies"][0]["torrents"][0]["seeds"]
        magnet_link = "magnet:?xt=urn:btih:" + yts_movie["data"]["movies"][0]["torrents"][0][
            "hash"] + torrent_trackers
        return seeds, magnet_link
    else:
        logger.error("error while extracting the movie details from the YTS REST API")
        return yts_movie
