import http
import json
import ssl


def eztv_extract_tv_show_episodes(tmdb_show_id):
    # Extract the TV show episod#es from the EZTV API
    eztv_url = "eztv.io"
    connection = http.client.HTTPSConnection(
        eztv_url, context=ssl._create_unverified_context())
    connection.request(
        "GET", "/api/get-torrents?imdb_id=" + tmdb_show_id)
    response = connection.getresponse()
    response_data = response.read()
    eztv_shows = json.loads(response_data)
    return eztv_shows["torrents"]
