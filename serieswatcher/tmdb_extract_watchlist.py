import http.client
import json
from json import JSONEncoder
from datetime import datetime
from datetime import timedelta
import os
import time
import re
import fnmatch
import glob
from itertools import groupby
import subprocess
from tmdb_api_connection import tmdb_api_connection


# Execute the tmdb_api_connection function to extract the user information
api_connection = tmdb_api_connection(os.environ.get('TMDB_USERNAME'),
                                     os.environ.get('TMDB_PASSWORD'),
                                     os.environ.get('TMDB_API_KEY'),
                                     os.environ.get('TMDB_ACCOUNT_ID')
                                     )


# Send a GET request to get the list of series in the watchlist
def extract_watchlist_series():
    request_token_payload = JSONEncoder().encode(
        {"request_token": api_connection["request_token"]})
    api_connection["connection"].request("GET",
                                         "/3/account/" + api_connection["account_id"] + "/watchlist/tv?api_key=" + api_connection["api_key"] + "&language=en-US&session_id=" + api_connection["session_id"] + "&sort_by=created_at.asc")
    watchlist_response = api_connection["connection"].getresponse()
    watchlist_data = watchlist_response.read()
    watchlist_series = json.loads(watchlist_data)
    return watchlist_series
