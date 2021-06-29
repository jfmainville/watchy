import requests


def eztv_extract_tv_show_episodes(eztv_url, tmdb_show_id):
    # Extract the TV show episodes from the EZTV API
    eztv_shows_request = requests.get(eztv_url + "/api/get-torrents?imdb_id=" + tmdb_show_id)
    eztv_shows = eztv_shows_request.json()
    return eztv_shows["torrents"]
