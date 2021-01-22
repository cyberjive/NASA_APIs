# TODO See if there's a better way to clear the test
# list than Autouse = True, it slows this down and is
# loaded unnecessarily
from typing import List
import pandas as pd
import pytest
import requests

from nasa_apis.utils import build_data_frame, write_to_disk
from nasa_apis.get_apis import get_nasa_apis, URLS


# Mock class for API response
class MockResponse:
    """
    REST GET response mock
    """

    def __init__(self, status_code):
        self.status_code = status_code

    @property
    def ok(self):
        if self.status_code == 200:
            return True
        else:
            return False

    def json(self):
        if not self.ok:
            # 4.xx response
            return {
                "error": {
                    "code": "API_KEY_INVALID",
                    "message": "An invalid api_key was supplied. Get one at "
                    "https://api.nasa.gov:443",
                }
            }
        else:
            # 200 response
            return {
                "date": "2020-09-24",
                "explanation": "One of our Solar System's most tantalizing worlds, icy "
                "Saturnian moon Enceladus appears in these detailed hemisphere "
                "views from the Cassini spacecraft. In false color, the five "
                "panels present 13 years of infrared image data from Cassini's "
                "Visual and Infrared Mapping Spectrometer and Imaging Science "
                "Subsystem. Fresh ice is colored red, and the most dramatic "
                "features look like long gashes in the 500 kilometer diameter "
                "moon's south polar region. They correspond to the location of "
                "tiger stripes, surface fractures that likely connect to an "
                "ocean beneath the Enceladus ice shell. The fractures are the "
                "source of the moon's icy plumes that continuously spew into "
                "space. The plumes were discovered by by Cassini in 2005. Now, "
                "reddish hues in the northern half of the leading hemisphere "
                "view also indicate a recent resurfacing of other regions of "
                "the geologically active moon, a world that may hold "
                "conditions suitable for life.   Experts Debate: How will "
                "humanity first discover extraterrestrial life?",
                "hdurl": "https://apod.nasa.gov/apod/image/2009/PIA24023_fig1.jpg",
                "media_type": "image",
                "service_version": "v1",
                "title": "Enceladus in Infrared",
                "url": "https://apod.nasa.gov/apod/image/2009/PIA24023_fig1_1050.jpg",
                "status_code": 200,
            }


# pandas fixtures
@pytest.fixture
def mock_success_json_normalize(monkeypatch):
    def mock_json_normalize(*args, **kwargs):
        return pd.DataFrame(
            {
                "date": "2020-09-24",
                "explanation": "big long string",
                "hdurl": "hdurl",
                "media_type": "type of media",
                "service_version": "the version of service",
                "title": "title of the day",
                "url": "url for the pic",
            }
        )

    monkeypatch.setattr(pd, "json_normalize", mock_json_normalize)


# requests fixtures
@pytest.fixture
def mock_success_response_code(monkeypatch):
    def mock_rest_fail(*args, **kwargs):
        return MockResponse(200)

    monkeypatch.setattr(requests, "get", mock_rest_fail)


@pytest.fixture
def mock_failure_response_code(monkeypatch):
    def mock_failure_request_get(*args, **kwargs):
        return MockResponse(404)

    monkeypatch.setattr(requests, "get", mock_failure_request_get)


# nasa output reset fixture
@pytest.fixture(autouse=True)
def clear_api_listing():
    t = get_nasa_apis()
    t.clear()


# mock dataframe argument
mock_df_arg = {
    "date": "2020-09-24",
    "explanation": "One of our Solar System's most tantalizing worlds, icy "
    "Saturnian moon Enceladus appears in these detailed hemisphere "
    "views from the Cassini spacecraft. In false color, the five "
    "panels present 13 years of infrared image data from Cassini's "
    "Visual and Infrared Mapping Spectrometer and Imaging Science "
    "Subsystem. Fresh ice is colored red, and the most dramatic "
    "features look like long gashes in the 500 kilometer diameter "
    "moon's south polar region. They correspond to the location of "
    "tiger stripes, surface fractures that likely connect to an "
    "ocean beneath the Enceladus ice shell. The fractures are the "
    "source of the moon's icy plumes that continuously spew into "
    "space. The plumes were discovered by by Cassini in 2005. Now, "
    "reddish hues in the northern half of the leading hemisphere "
    "view also indicate a recent resurfacing of other regions of "
    "the geologically active moon, a world that may hold "
    "conditions suitable for life.   Experts Debate: How will "
    "humanity first discover extraterrestrial life?",
    "hdurl": "https://apod.nasa.gov/apod/image/2009/PIA24023_fig1.jpg",
    "media_type": "image",
    "service_version": "v1",
    "title": "Enceladus in Infrared",
    "url": "https://apod.nasa.gov/apod/image/2009/PIA24023_fig1_1050.jpg",
}

# utils tests
def test_build_df_return_success():
    df = build_data_frame(mock_df_arg)
    assert df is not None
    assert isinstance(df, pd.DataFrame)


def test_build_df_return_failure():
    df = build_data_frame("invalid_arg")
    assert df is None


def test_write_to_disk_success():
    df = pd.json_normalize(mock_df_arg)
    disk_out = write_to_disk(df)
    assert disk_out is not None
    assert isinstance(disk_out, pd.DataFrame)


def test_write_to_disk_failure():
    df = "Invalid Argument"
    disk_out = write_to_disk(df)
    assert disk_out is None


# API call tests
def test_mock_success_api_call(mock_success_response_code):
    success_test_list = get_nasa_apis()
    assert type(success_test_list) == list
    assert len(success_test_list) == 3
    for item in success_test_list:
        assert 200 in item


def test_mock_failure_api_call(mock_failure_response_code):
    failure_test_list = get_nasa_apis()
    assert type(failure_test_list) == list
    assert len(failure_test_list) == 3
    for item in failure_test_list:
        assert 404 in item


# Data structure tests
def test_urls():
    assert len(URLS) == 3
    assert type(URLS) == list
