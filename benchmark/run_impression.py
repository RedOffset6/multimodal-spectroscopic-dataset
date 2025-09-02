import pandas as pd
from pathlib import Path
import glob
import sys

from IMPRESSION import IMPRESSION

def main():
    #converts the data type to a Path
    analytical_data = Path("../data")

    #loops through the parquet files
    for parquet_file in analytical_data.glob("*.parquet"):
        imp = IMPRESSION(model_path='trained_model.torch')

        print(f"working on {parquet_file.stem}")

        data = pd.read_parquet(parquet_file)
        print(data.iloc[0])
        break
if __name__ == '__main__':
    main()