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


def tmdb_api_connection(username, password, api_key, account_id):
    # Send a GET request to receive the request token
    connection_api = http.client.HTTPSConnection("api.themoviedb.org")
    connection_api.request(
        "GET", "/3/authentication/token/new?api_key=" + api_key)
    request_token_response = connection_api.getresponse()
    request_token_data = request_token_response.read()
    request_token = json.loads(request_token_data)['request_token']

    # Send a POST request to validate the request token with the username and password
    validate_with_login_payload = JSONEncoder().encode({
        "username": username,
        "password": password,
        "request_token": request_token
    })
    connection_api.request("POST", "/3/authentication/token/validate_with_login?api_key=" + api_key,
                           validate_with_login_payload, headers={'Content-type': 'application/json'})
    validate_with_login_response = connection_api.getresponse()
    validate_with_login_data = validate_with_login_response.read().decode()

    # Send a POST request to get the session id
    request_token_payload = JSONEncoder().encode(
        {"request_token": request_token})
    connection_api.request("POST", "/3/authentication/session/new?api_key=" + api_key, request_token_payload,
                           headers={'Content-type': 'application/json'})
    session_id_response = connection_api.getresponse()
    session_id_data = session_id_response.read()
    session_id = json.loads(session_id_data)['session_id']
    return {
        "connection": connection_api,
        "account_id": account_id,
        "request_token": request_token,
        "api_key": api_key,
        "session_id": session_id
    }
