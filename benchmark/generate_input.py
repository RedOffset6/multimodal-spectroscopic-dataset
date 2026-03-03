import pandas as pd
import ast
import matplotlib.pyplot as plt
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors
from rdkit import RDLogger
import numpy as np
import re
import os
RDLogger.DisableLog('rdApp.*')

def read_data(path):
    df = pd.read_parquet(path)

    #  Keep only 1H + 13C
    df = df[df["NMR_type"].isin(["1H NMR", "13C NMR"])]

    #Keep only molecules having BOTH spectra
    both_counts = (
        df.groupby("SMILES")["NMR_type"]
          .nunique()
    )

    both_smiles = both_counts[both_counts == 2].index

    df_both = df[df["SMILES"].isin(both_smiles)]

    # Pivot → ONE ROW PER SMILES
    df_wide = df_both.pivot_table(
        index="SMILES",
        columns="NMR_type",
        values=[
            "NMR_processed",
            "NMR_shift_text",
            "NMR_solvent"
        ],
        aggfunc="first"
    )

    # Flatten MultiIndex columns
    df_wide.columns = [
        f"{val}_{nmr.replace(' NMR','')}"
        for val, nmr in df_wide.columns
    ]

    df_wide = df_wide.reset_index()
    df_wide["NMR_processed_13C"] = df_wide["NMR_processed_13C"].apply(ast.literal_eval)


    return df_wide

def count_cs(x):
    try:
        mol = Chem.MolFromSmiles(x)

        num_carbons = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')

        return num_carbons
    except:
        return np.nan


def plot_carbon_shifts(df):
    df["NMR_13C_count"] = df["NMR_processed_13C"].apply(len)
    df["c_atom_count"] = df["SMILES"].apply(count_cs)

    success_fraction = (df["NMR_13C_count"] <= df["c_atom_count"]).mean()
    print(f"in {success_fraction*100}% of the molecules teh number of carbon atoms and shifts matched")
    print(df["c_atom_count"])
    print("NMR_13C_count")



    plt.scatter(df["c_atom_count"], df["NMR_13C_count"], alpha = 0.01, s=10)
    plt.plot([0,60], [0,60], color ="red")
    plt.xlim(0,60)
    plt.ylim(0,60)
    plt.title("Carbon Shifts in NMREXP")
    plt.xlabel("C Atom Count")
    plt.ylabel("Number of C shifts")

    # print(df[["NMR_13C_count"]])
    # print(df[["c_atom_count"]])
    plt.savefig("carbon_shifts.png")

SMILES_TOKENIZER = re.compile(
    r"(\[[^\]]+]|Br|Cl|Si|Se|Na|Li|Ca|Mg|Al|"
    r"@@?|=|#|-|\+|\\|\/|\(|\)|\.|"
    r"\d+|[A-Za-z])"
)

def smiles_to_formula(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    formula = rdMolDescriptors.CalcMolFormula(mol)

    tokens = SMILES_TOKENIZER.findall(formula)
    return " ".join(tokens)

# tokenises the smiles
def tokenise_smiles(smiles):
    tokens = SMILES_TOKENIZER.findall(smiles)
    return " ".join(tokens)


def flatten_spectrum(spectrum):
    flat_list = []
    for item in spectrum:
        if isinstance(item, list):  # if item is a sublist
            flat_list.extend(item)   # add all elements of sublist
        else:
            flat_list.append(item)   # add the item itself
    return flat_list

def tokenise_carbon_shifts(carbon_list):
    carbon_shifts = [sublist[0] for sublist in carbon_list]
    carbon_shifts = flatten_spectrum(carbon_shifts)
    # checks that the list is flat

    carbon_shifts.sort(reverse=True)

    # Convert each number to string, then join with space

    carbon_string = " ".join(str(round(x, 1)) for x in carbon_shifts)
    carbon_string = f"13CNMR {carbon_string}"
    return carbon_string

def tokenise_proton_shifts(proton_list):
    # tries to turn the strings into tuples
    try:
        proton_list = ast.literal_eval(proton_list)
    except Exception as e:
        print("Failed to parse proton_list:", e)
        return np.nan

    proton_list = sorted(proton_list, key=lambda x: (x[3]+x[4]), reverse= True)

    proton_string = "HNMR "
    for peak in proton_list:
        # calculates shift
        shift = (peak[3]+peak[4])/2
 
        # unpacks the coupling value
        
        if len(peak[1]) == 0 or (peak[1] is None):
            coupling = ""
        elif len(peak[1]) == 1:
            coupling = f"{peak[1][0]} "
        elif len(peak[1]) == 2:
            coupling = f"{peak[1][0]} {peak[1][1]} "
        else:
            coupling = ""

        # builds the proton string 
        proton_string = f"{proton_string}{round(shift, 2)} {peak[0]} {coupling}{peak[2]} | "

    return proton_string




    
def create_input_strings(df):
    # creates a coloumn which contains tokenised molecular formulae
    df["molecular_formula"] = df["SMILES"].apply(smiles_to_formula)

    df["tokenised_carbons"] = df["NMR_processed_13C"].apply(tokenise_carbon_shifts)

    df["tokenised_proton"] = df["NMR_processed_1H"].apply(tokenise_proton_shifts)

    df["tokenised_smiles"] = df["SMILES"].apply(tokenise_smiles)

    return df

def split_data(df):
    # shuffle the dataframe
    df_shuffled = df.sample(frac=1, random_state=42)

    # compute split indices
    n = len(df_shuffled)
    train_end = int(0.9 * n)
    val_end = int(0.95 * n)

    # split
    df_train = df_shuffled.iloc[:train_end]
    df_val = df_shuffled.iloc[train_end:val_end]
    df_test = df_shuffled.iloc[val_end:]

    return df_train, df_val, df_test

def write_files(df, folder_name):
    os.makedirs(folder_name, exist_ok=True)

    df["src"] = df["molecular_formula"] + " " + df["tokenised_proton"] + " " + df["tokenised_carbons"]

    df_train, df_val, df_test = split_data(df)

    # writes the src files
    df_train["src"].to_csv(f"{folder_name}/src-train.txt", index=False, header=False)
    df_val["src"].to_csv(f"{folder_name}/src-val.txt", index =False, header = False)
    df_test["src"].to_csv(f"{folder_name}/src-test.txt", index=False, header=False)

    df_train["tokenised_smiles"].to_csv(f"{folder_name}/tgt-train.txt", index=False, header=False)
    df_val["tokenised_smiles"].to_csv(f"{folder_name}/tgt-val.txt", index =False, header = False)
    df_test["tokenised_smiles"].to_csv(f"{folder_name}/tgt-test.txt", index=False, header=False)



def main():
    path = '../../nmrexp/NMRexp_10to24_1_1004.parquet'

    # reads data
    df = read_data(path)

    # creates the input strings
    df = create_input_strings(df)

    # writes the src and tgt .txt files
    write_files(df, "../expt_train/data")

main()