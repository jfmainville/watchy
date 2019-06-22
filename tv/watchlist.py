import json
import http.client
import os


# Send a GET request to get the list of series in the watchlist
def extract_watchlist_series(tmdb_api_url, tmdb_account_id, tmdb_session_id, tmdb_api_key):
    api_connection = http.client.HTTPSConnection(tmdb_api_url)
    api_connection.request("GET", "/3/account/" + tmdb_account_id + "/watchlist/tv?api_key=" +
                           tmdb_api_key + "&language=en-US&session_id=" + tmdb_session_id + "&sort_by=created_at.asc")
    watchlist_response = api_connection.getresponse()
    watchlist_data = watchlist_response.read()
    watchlist_series = json.loads(watchlist_data)
    return watchlist_series["results"]


def extract_show_details(tmdb_api_url, tmdb_api_key, show):
    api_connection = http.client.HTTPSConnection(tmdb_api_url)
    api_connection.request("GET",
                           "/3/tv/" + str(show["id"]) + "?api_key=" + tmdb_api_key + "&language=en-US")
    show_details_response = api_connection.getresponse()
    show_details_data = show_details_response.read()
    show_details = json.loads(show_details_data)
    return show_details
