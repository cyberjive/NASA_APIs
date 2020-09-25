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
    response = requests.get(url)
    if response.ok:
        response_json = json.loads(response.text)
        json_string = json.dumps(
            response_json,
            indent=4,
            sort_keys=True,
        )
        print(json_string)
        return json_string
    else:
        return f"Error on call, response code: { response.status_code }"

if __name__ == "__main__":
    get_apod()
