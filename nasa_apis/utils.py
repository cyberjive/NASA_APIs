# TODO fix csv construction on dataframe build/write
import json
from .log_decorator import LogDecorator
import pandas as pd
from pandas import DataFrame


@LogDecorator()
def build_data_frame(data: str) -> pd.DataFrame:
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
        return None


@LogDecorator()
def write_to_disk(df_to_write: pd.DataFrame) -> pd.DataFrame:
    """
    Write the provided data frame to csv
    simulating a DB
    """
    try:
        df_to_write.to_csv(r"NASA_APIs.csv", mode="a", index=True)
        print(f"{ df_to_write } with { df_to_write.columns } written to disk.")
        return df_to_write
    except Exception as e:
        print(f"{ str(e) }")
        return None
