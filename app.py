#! /usr/bin/python
# TODO: write to dataframe/csv

# standard library
import os
import json
from collections import namedtuple
from pprint import pprint

# requires install
import requests

# custom
from log_decorator import LogDecorator

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


@LogDecorator()
def get_nasa_apis():
    for url in URLS:
        print(url)
        response = requests.get(url)
        pprint(response)
        if response.status_code == 200:
            if response.text:
                pprint(response.text)
                continue
            elif response.content:
                pprint(response.content)
                continue
            return response.status_code


if __name__ == "__main__":
    # get_apod()
    # get_landsat_imagery()
    # get_mars_weather()
    get_nasa_apis()
    pass
