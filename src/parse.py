import pandas as pd


def parse_csv(filename: str) -> pd.DataFrame:
    df = pd.read_csv(filename)

    return df
