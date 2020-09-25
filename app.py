#! /usr/bin/python

# standard library
import os
import json

# requires install
import requests

# API key
NASA_KEY = os.environ["NASA_KEY"]

# APOD - astronomy picture of the day
def get_apod():
    """
    Call the astronomy pic of the day endpoint and return the JSON
    """
    url = f"https://api.nasa.gov/planetary/apod?api_key={ NASA_KEY }"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            response_json = json.loads(response.text)
            json_string = json.dumps(
                response_json,
                indent=4,
                sort_keys=True,
            )
            print(json_string)
            return json_string
        else:
            return f"Error on call, response { response.status_code }"
    except Exception as e:
        return f"Error: { str(e) }"


def get_landsat_imagery(lat=40.647040, lon=-73.937414):
    """
    Call the landsat imagery endpoint and return the result
    """
    url = f"https://api.nasa.gov/planetary/earth/imagery?lon={ lon }&lat={ lat }&api_key={ NASA_KEY }"
    try:
        response = requests.get(url)
        if response.ok:
            print(response.content)
        else:
            return f"Error on call, response code { response.status_code }"
    except Exception as e:
        return f"Error: { str(e) }"


if __name__ == "__main__":
    # get_apod()
    # get_landsat_imagery()
    pass
