import requests
import json
from flask import Flask, jsonify

def get_assets():
    url = "http://127.0.0.1:5000/courses"
    headers = {
            'x-access-token': "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOjEsImV4cCI6MTY1Njk1MTI0Mn0.iVJF6OtdsD_pYkuJN_UKsOsFh0r6N0wVrzSH90-x5Sc",
            'accept': "application/json",
            'content-type': "application/json"
            }
    response = requests.request("GET", url, headers = headers)
    print(response.json())
    

if __name__ == '__main__':
    get_assets()
