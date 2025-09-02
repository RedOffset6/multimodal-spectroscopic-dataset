import pandas as pd
import json
from pathlib import Path
import numpy as np

def main():
    # point this to your saved parquet file
    parquet_path = Path("data_imp_2d/aligned_chunk_0.parquet")
    
    print(f"Reading {parquet_path}")
    df = pd.read_parquet(parquet_path, engine="pyarrow")  # or fastparquet if you prefer
    print(df.head())

    # print("\n=== DataFrame Info ===")
    # print(df.info())
    # print("\nColumns:", df.columns.tolist())
    # print(f"Total molecules: {len(df)}\n")

    # # Show the first few rows of new columns
    # print("=== First few cosy/hsqc/hmbc entries ===")
    # print(df[["smiles", "cosy", "hsqc", "hmbc"]].head())

    # # If you want to inspect JSON -> DataFrame
    # if "imp_atoms_df" in df.columns:
    #     atoms_json = df.loc[0, "imp_atoms_df"]
    #     atoms_df = pd.read_json(atoms_json)
    #     print("\n=== Atoms DF (row 0) ===")
    #     print(atoms_df.head())

    # if "imp_pairs_df" in df.columns:
    #     pairs_json = df.loc[0, "imp_pairs_df"]
    #     pairs_df = pd.read_json(pairs_json)
    #     print("\n=== Pairs DF (row 0) ===")
    #     print(pairs_df.head())
    print(df.iloc[0])
    count_arrays = df["cosy"].apply(lambda x: isinstance(x, np.ndarray)).sum()
    print("Rows where cosy is a list:", count_arrays)

if __name__ == "__main__":
    main()