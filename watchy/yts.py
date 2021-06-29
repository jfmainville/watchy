import requests


def yts_extract_movie_torrent(yts_url, movie_imdb_id):
    # Send a GET request to extract the movie torrent data for each movie in the watchlist
    yts_movie_request = requests.get(yts_url +
                                     "/api/v2/list_movies.json?sort=seeds&limit=5&query_term=" + str(movie_imdb_id))
    yts_movie = yts_movie_request.json()

    seeds = yts_movie["data"]["movies"][0]["torrents"][0]["seeds"]
    magnet_link = "magnet:?xt=urn:btih:" + yts_movie["data"]["movies"][0]["torrents"][0][
        "hash"] + "&dn=Url+Encoded+Movie+Name&tr=udp://open.demonii.com:1337/announce&tr=udp://tracker.openbittorrent.com:80&tr=udp://tracker.coppersurfer.tk:6969"

    return seeds, magnet_link
