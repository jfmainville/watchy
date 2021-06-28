import json
import http.client


def yts_extract_movie_torrent(movie_imdb_id, yts_url):
    # Send a GET request to extract the movie torrent data for each movie in the watchlist
    api_connection = http.client.HTTPSConnection(yts_url)
    api_connection.request("GET",
                           "/api/v2/list_movies.json?sort=seeds&limit=5&query_term=" + str(movie_imdb_id))
    yts_movie_response = api_connection.getresponse()
    yts_movie_response_data = yts_movie_response.read()
    yts_movie = json.loads(yts_movie_response_data)

    seeds = yts_movie["data"]["movies"][0]["torrents"][0]["seeds"]
    magnet_link = "magnet:?xt=urn:btih:" + yts_movie["data"]["movies"][0]["torrents"][0][
        "hash"] + "&dn=Url+Encoded+Movie+Name&tr=udp://open.demonii.com:1337/announce&tr=udp://tracker.openbittorrent.com:80&tr=udp://tracker.coppersurfer.tk:6969"

    return seeds, magnet_link
