import pandas as pd


def parse_csv(filename: str) -> pd.DataFrame:
    df = pd.read_csv(filename)

    return df


def save_csv(data: list, filename: str) -> None:
    df = pd.DataFrame(data)

    df.to_csv(filename, index=False)
