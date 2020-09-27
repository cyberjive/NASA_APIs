#! /usr/bin/python
# TODO: add more APIs, deal with geo 404

# standard library
import os
import json
from collections import namedtuple
from pprint import pprint

# requires install
import requests

# custom
from .log_decorator import LogDecorator
from .utils import build_data_frame, write_to_disk

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
    try:
        for url in URLS:
            print(f"Retrieving { url }")
            response = requests.get(url)
            if response.status_code == 200:
                if response.text:
                    breakpoint()
                    dataframe = build_data_frame(response.text)
                    write_to_disk(dataframe)
                    print("Writing to disk...")
                    continue
                elif response.content:
                    breakpoint()
                    dataframe = build_data_frame(response.content)
                    write_to_disk(dataframe)
                    print("Writing to disk...")
                return response.status_code
            else:
                breakpoint()
                print(f"Error on call: {response.status_code}")
                return response.status_code
    except Exception as e:
        return f"{ str(e) }"


if __name__ == "__main__":
    get_nasa_apis()
