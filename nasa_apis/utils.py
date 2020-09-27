import json
from nasa_apis.log_decorator import LogDecorator
import pandas as pd
from pandas import DataFrame

# TODO fix csv construction on dataframe build/write


@LogDecorator()
def build_data_frame(data: dict) -> pd.DataFrame:
    """
    Construct a new data frame from the provided
    dictionary
    """
    try:
        data = json.loads(data)
        df = pd.json_normalize(data)
        breakpoint()
        return df
    except Exception as e:
        print(f"{ str(e) }")


@LogDecorator()
def write_to_disk(df_to_write: pd.DataFrame):
    """
    Write the provided data frame to csv
    simulating a DB
    """
    try:
        df = df_to_write.to_csv(r"NASA_APIs.csv", mode="a", index=True)
        breakpoint()
        print(f"{ df.shape } written to disk.")
        return df.shape
    except Exception as e:
        print(f"{ str(e) }")
