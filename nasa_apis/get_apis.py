#! /usr/bin/python
# TODO: add more APIs, deal with geo 404

# standard library
import os
from typing import Tuple, List
from collections import namedtuple

# requires install
import requests

# custom
from nasa_apis.log_decorator import LogDecorator
from nasa_apis.utils import build_data_frame, write_to_disk

# API key
NASA_KEY = os.environ["NASA_KEY"]

# coordinates for geo API
Point = namedtuple("coordinates", "lat long")
pt1 = Point(40.647040, -73.937414)

# Endpoints
URLS = [
    f"https://api.nasa.gov/planetary/apod?date=2020-09-24&api_key={ NASA_KEY}",
    # f"https://api.nasa.gov/planetary/earth/imagery?lon={ pt1[0] }&lat={ pt1[1] }&api_key={ NASA_KEY }",
    f"https://api.nasa.gov/insight_weather/?api_key={ NASA_KEY }&feedtype=json&ver=1.0",
    f"https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&api_key={ NASA_KEY }",
]

# named tuple for reponses
Response = namedtuple("reponses", "url code status")

# List to capture output
RESPONSES = []


@LogDecorator()
def get_nasa_apis() -> List[Tuple]:
    try:
        for url in URLS:
            print(f"Retrieving { url }")
            response = requests.get(url)
            if response.status_code == 200:
                dataframe = build_data_frame(response.json())
                write_to_disk(dataframe)
                RESPONSES.append(Response(url, response.status_code, response.ok))
            else:
                print(f"Error on call: {response.status_code}")
                RESPONSES.append(Response(url, response.status_code, response.ok))
        print(RESPONSES)
        return RESPONSES
    except Exception as e:
        return f"ERROR: { str(e) }"


if __name__ == "__main__":
    get_nasa_apis()
