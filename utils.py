import json
from log_decorator import LogDecorator
import pandas as pd
from pandas import DataFrame
#TODO fix csv construction on dataframe build/write


@LogDecorator()
def build_data_frame(data: dict):
    """
    Construct a new data frame from the provided
    dictionary
    """
    try:
        data = json.loads(data)
        df = pd.json_normalize(data)
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
        df_to_write.to_csv(r"NASA_APIs.csv", index=True)
        print(f"{ df_to_write.shape } written to disk.")
        return None
    except Exception as e:
        print(f"{ str(e) }")
