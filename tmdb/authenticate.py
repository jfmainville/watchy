import http.client
import json
import os
from json import JSONEncoder


def authenticate(tmdb_api_url, tmdb_username, tmdb_password, tmdb_api_key, tmdb_account_id):
    # Send a GET request to receive the request token
    api_connection = http.client.HTTPSConnection(tmdb_api_url)
    headers = {
        "Content-Type": "application/json"
    }
    api_connection.request(
        "GET", "/3/authentication/token/new?api_key=" + tmdb_api_key)
    request_token_response = api_connection.getresponse()
    request_token_data = request_token_response.read()
    request_token = json.loads(request_token_data)['request_token']

    # Send a POST request to validate the request token with the username and password
    validate_with_login_payload = JSONEncoder().encode({
        "username": tmdb_username,
        "password": tmdb_password,
        "request_token": request_token
    })
    api_connection.request("POST", "/3/authentication/token/validate_with_login?api_key=" + tmdb_api_key,
                           validate_with_login_payload, headers=headers)
    tmdb_validate_login_response = api_connection.getresponse()
    tmdb_validate_login_response.read()

    # Send a POST request to get the session id
    request_token_payload = JSONEncoder().encode({
        "request_token": request_token
    })
    api_connection.request(
        "POST", "/3/authentication/session/new?api_key=" + tmdb_api_key, body=request_token_payload, headers=headers)
    tmdb_session_id_response = api_connection.getresponse()
    tmdb_session_id_data = tmdb_session_id_response.read()
    tmdb_session_id = json.loads(tmdb_session_id_data)['session_id']
    return tmdb_session_id
