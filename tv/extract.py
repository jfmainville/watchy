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
from tmdb.authenticate import authenticate


# Execute the authenticate function to extract the user information
tmdb_authenticate = authenticate(os.environ.get('TMDB_USERNAME'),
                                 os.environ.get('TMDB_PASSWORD'),
                                 os.environ.get('TMDB_API_KEY'),
                                 os.environ.get('TMDB_ACCOUNT_ID')
                                 )


# Send a GET request to get the list of series in the watchlist
def extract_watchlist_series():
    request_token_payload = JSONEncoder().encode(
        {"request_token": tmdb_authenticate["request_token"]})
    tmdb_authenticate["connection"].request("GET",
                                            "/3/account/" + tmdb_authenticate["account_id"] + "/watchlist/tv?api_key=" + tmdb_authenticate["api_key"] + "&language=en-US&session_id=" + tmdb_authenticate["session_id"] + "&sort_by=created_at.asc")
    watchlist_response = tmdb_authenticate["connection"].getresponse()
    watchlist_data = watchlist_response.read()
    watchlist_series = json.loads(watchlist_data)
    return watchlist_series["results"]
