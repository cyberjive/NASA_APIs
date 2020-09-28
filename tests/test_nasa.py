import pandas as pd
import pytest
import requests

from nasa_apis.utils import build_data_frame, write_to_disk
from nasa_apis.get_apis import get_nasa_apis

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
    def mock_request_get(*args, **kwargs):
        return MockResponse(200)

    monkeypatch.setattr(requests, "get", mock_request_get)


@pytest.fixture
def mock_failure_response_code(monkeypatch):
    def mock_request_get(*args, **kwargs):
        return MockResponse(404)

    monkeypatch.setattr(requests, "get", mock_request_get)


# mock dataframe argument
mock_df_arg = '{"date":"2020-09-24","explanation":"One of our Solar System\'s most tantalizing worlds, icy Saturnian moon Enceladus appears in these detailed hemisphere views from the Cassini spacecraft. In false color, the five panels present 13 years of infrared image data from Cassini\'s Visual and Infrared Mapping Spectrometer and Imaging Science Subsystem. \
        Fresh ice is colored red, and the most dramatic features look like long gashes in the 500 kilometer diameter moon\'s south polar region. They correspond to the location of tiger stripes, surface fractures that likely connect to an ocean beneath the Enceladus ice shell. \
        The fractures are the source of the moon\'s icy plumes that continuously spew into space. \
        The plumes were discovered by by Cassini in 2005. Now, reddish hues in the northern half of the leading hemisphere view also indicate a recent resurfacing of other regions of the geologically active moon, a world that may hold conditions suitable for life.   Experts Debate: How will humanity first discover extraterrestrial life?",\
        "hdurl":"https://apod.nasa.gov/apod/image/2009/PIA24023_fig1.jpg","media_type":"image","service_version":"v1","title":"Enceladus in Infrared","url":"https://apod.nasa.gov/apod/image/2009/PIA24023_fig1_1050.jpg"}\n'

# utils tests
def test_build_df_return_success():
    df = build_data_frame(mock_df_arg)
    assert df is not None
    assert isinstance(df, pd.DataFrame)


def test_build_df_return_failure():
    df = build_data_frame("invalid_arg")
    assert df is None


def test_write_to_disk_success():
    df = build_data_frame(mock_df_arg)
    disk_out = write_to_disk(df)
    assert disk_out is not None
    assert isinstance(disk_out, pd.DataFrame)


def test_write_to_disk_failure():
    df = build_data_frame("invalid_arg")
    disk_out = write_to_disk(df)
    assert disk_out is None
