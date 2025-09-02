import pandas as pd
from pathlib import Path
import glob
import sys
import numpy as np
import matplotlib.pyplot as plt
import pyarrow
import time


def plot_peaks(peaks, title, xlabel, ylabel, filename):
    """
    Generic function to plot and save NMR peak lists.
    peaks: list of [x, y] coordinates
    """
    # Convert list of np.float64 or floats into arrays
    peaks = np.array(peaks, dtype=float)

    plt.figure(figsize=(6,6))
    plt.scatter(peaks[:,0], peaks[:,1], c="red", marker="o", s=40, edgecolors="black")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    # # Set square aspect for typical NMR look
    # plt.gca().set_aspect('equal', adjustable='box')

    # In NMR, chemical shift axes run *right to left*, so reverse them
    plt.gca().invert_xaxis()
    plt.gca().invert_yaxis()

    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()
    print(f"Saved {title} plot to {filename}")


def build_2d_experiments(atoms_df, pairs_df):
    #print(len(atoms_df))
    #print(atoms_df)
    #atoms_df.to_csv("atoms.csv", index=False)
    #print(atoms_df)
    #loops through pairs
    #pairs_df.to_csv("pairs.csv", index=False)

    #if atom index 0 == atom index 1 then both atoms in the pair are the same atom and should be ignored
    #by removing indeces where atom 0 > atom 1 each pair will only be considered once (index 0 and index 1 will be compared but index 1 and 0 will not)



    pairs_df = pairs_df[pairs_df["atom_index_0"] <= pairs_df["atom_index_1"]]

    pairs_df.to_csv("pairs_no_dupliacates.csv", index=False)
    
    cosy_list = []
    hsqc_list = []
    hmbc_list = []

    #iterates through the rows in the pair dataframe
    for index, row in pairs_df.iterrows():
        #finds the atom indeces
        atom_index_0 = row["atom_index_0"]
        atom_index_1 = row["atom_index_1"]
        
        #finds atom type for each of the two atoms in the pair
        atom_type_0 = atoms_df.iloc[atom_index_0]["typeint"]
        atom_type_1 = atoms_df.iloc[atom_index_1]["typeint"]


        ################
        #     COSY     #     (currently does not include the cross peaks)
        ################

        #checks to see if both atoms are Hydrogen and the scalar coupling is greater than 2Hz (e.g could show up in a cosy experiment)
        if (atom_type_0 == 1) and (atom_type_1 == 1) and (abs(row["predicted_coupling"]) >= 2):
            shift0 = atoms_df.iloc[atom_index_0]["predicted_shift"]
            shift1 = atoms_df.iloc[atom_index_1]["predicted_shift"]
            
            # #creates a string for the cosy peak
            cosy_peak = [round(shift0, 2), round(shift1, 2)]

            cosy_list.append(cosy_peak)

        #adding in the cross peaks between an atom and its self (The diagonal)
        #the 2 Hz filter is removed because impression outputs a coupling of zero Hz between an atom and itself
        if (atom_index_0 == atom_index_1) and (atom_type_0 == 1):
            shift0 = atoms_df.iloc[atom_index_0]["predicted_shift"]
            shift1 = atoms_df.iloc[atom_index_1]["predicted_shift"]
            
            #creates the peak string
            cosy_peak = [round(shift0, 2), round(shift1, 2)]

            cosy_list.append(cosy_peak)



        ################
        #     HSQC     #
        ################

        #checks to see if both atoms are Hydrogen and the scalar coupling is greater than 2Hz (e.g could show up in
        = 100):
            shift0 = atoms_df.iloc[atom_index_0]["predicted_shift"]
            shift1 = atoms_df.iloc[atom_index_1]["predicted_shift"]
            
            # #creates a string for the HSQC rounding the carbon shift to 1dp
            if atom_type_0 == 6:
                hsqc_peak = [round(shift1, 2), round(shift0, 1)]
            else:
                hsqc_peak = [round(shift0, 2), round(shift1, 1)]
            hsqc_list.append(hsqc_peak)


        ################
        #     HMBC     #
        ################

        #checks to see if both atoms are Hydrogen and the scalar coupling is greater than 2Hz (e.g could show up in an HMBC experiment)
        if (((atom_type_0 == 1) and (atom_type_1 == 6)) or ((atom_type_0 == 6) and (atom_type_1 == 1))) and ((abs(row["predicted_coupling"]) >= 2)and (abs(row["predicted_coupling"]) < 50)):
            shift0 = atoms_df.iloc[atom_index_0]["predicted_shift"]
            shift1 = atoms_df.iloc[atom_index_1]["predicted_shift"]
            
            # #creates a string for the cosy peak
            if atom_type_0 == 6:            
                hmbc_peak = [round(shift1, 2), round(shift0, 1)]
            else:
                hmbc_peak = [round(shift0, 2), round(shift1, 1)]
            
            hmbc_list.append(hmbc_peak)

    # print("COSY PEAKS")
    # print(cosy_list)

    # print("HSQC PEAKS")
    # print(hsqc_list)

    # print("HMBC PEAKS")
    # print(hmbc_list)

    # plot_peaks(cosy_list, "COSY Spectrum", "1H Shift (ppm)", "1H Shift (ppm)", "cosy.png")
    # plot_peaks(hsqc_list, "HSQC Spectrum",  "1H Shift (ppm)","13C Shift (ppm)", "hsqc.png")
    # plot_peaks(hmbc_list, "HMBC Spectrum",  "1H Shift (ppm)", "13C Shift (ppm)", "hmbc.png")
    return cosy_list, hsqc_list, hmbc_list



#
#Non Parallel version of main 
#

# def main():
#     print("HELLO")
#     #converts the data type to a Path
#     analytical_data = Path("../../alberts/multimodal-spectroscopic-dataset/data")

#     # print("HELLO2")
#     imp = IMPRESSION(model_path='utils/model/PAPER_DT456E_15IQR_CLEANED_OPT_checkpoint.torch')


#     #loops through the parquet files
#     for parquet_file in analytical_data.glob("*.parquet"):
#         print(f"working on {parquet_file.stem}")
#         start = time.time()
#         data = pd.read_parquet(parquet_file)

#         # add coloumns for the impression outputs
#         for col in ["cosy", "hsqc", "hmbc", "imp_atoms_df", "imp_pairs_df"]:
#             if col not in data.columns:
#                 data[col] = None
        
        
#         for index, molecule in data.iterrows():
#             print(molecule["smiles"])
#             #Run impression and return the atoms, and pairs dataframes datastructure

#             start_imp = time.time()
#             atoms_df, pairs_df = imp.predict_from_files([molecule["smiles"]])
#             end_imp = time.time()
#             print(f"time spent on impression call: {end_imp - start_imp:.2f} seconds")

#             #generate mock versions of the 2d experiments
#             cosy_list, hsqc_list, hmbc_list = build_2d_experiments(atoms_df, pairs_df)
            
#             data.at[index, "cosy"] = cosy_list
#             data.at[index, "hsqc"] = hsqc_list
#             data.at[index, "hmbc"] = hmbc_list
#             data.at[index, "imp_atoms_df"] = atoms_df.to_json(orient="records")
#             data.at[index, "imp_pairs_df"] = pairs_df.to_json(orient="records")
#             break
#         end = time.time()
#         print(f"Total time: {end - start:.2f} seconds")
#         # Save as new parquet
#         output_path = Path("../../alberts/multimodal-spectroscopic-dataset/data_imp")
#         save_path = output_path / f"{parquet_file.stem}_imp.parquet"
#         data.to_parquet(save_path, engine="pyarrow", index=False)
#         break

def process_file(file_path, file_number):
    start = time.time()
    print("A new thread says Hi")
    print("beginning to read parquet")
    data = pd.read_parquet(file_path)

    # add coloumns for the 2d experiment outputs
    for col in ["cosy", "hsqc", "hmbc" ]:
        if col not in data.columns:
            data[col] = None
    
    atoms_df = pd.read_csv(f"data_imp/parquet_{file_number}/atoms.csv")
    pairs_df = pd.read_csv(f"data_imp/parquet_{file_number}/pairs.csv")

    #print(pairs_df.head())
    #print(atoms_df.head())
    
    print("Beginning iteration")
    for index, molecule in data.iterrows():
        #start_loop = time.time()

        
        smile_string = molecule["smiles"]

        print("RETURNING THE ATOMS DF FOR MY MOLECULE")
        atoms = atoms_df[atoms_df["molecule_name"]==smile_string]
        pairs = pairs_df[pairs_df["molecule_name"]==smile_string]

        cosy_list, hsqc_list, hmbc_list = build_2d_experiments(atoms, pairs)

        #saves the new data
        data.at[index, "cosy"] = cosy_list
        data.at[index, "hsqc"] = hsqc_list
        data.at[index, "hmbc"] = hmbc_list

        #end_loop = time.time()

        #print(f"\n\n2D STRUCTURE GEN CALL TIMING\n\ntime spent on impression call: {end_loop - start_loop:.2f} seconds\n\n")


    save_path = f"data_imp_2d/aligned_chunk_{file_number}.parquet"
    data.to_parquet(save_path, engine="pyarrow", index=False)
        #Run impression and return the atoms, and pairs dataframes datastructure
        
    #     print("Beginning impression call")
    #     start_imp = time.time()
    #     atoms_df, pairs_df = imp.predict_from_files([molecule["smiles"]])
    #     end_imp = time.time()
    #     print(f"\n\nIMPRESSION CALL TIMING\n\ntime spent on impression call: {end_imp - start_imp:.2f} seconds\n\n")
 
    #     print(f"PRINTING ATOMS DF\n\n\n\ {atoms_df}")

    #     print(f"PRINTING PAIRS DF\n\n\n\ {pairs_df}")

    #     # #generate mock versions of the 2d experiments
    #     # cosy_list, hsqc_list, hmbc_list = build_2d_experiments(atoms_df, pairs_df)
        
    #     # data.at[index, "cosy"] = cosy_list
    #     # data.at[index, "hsqc"] = hsqc_list
    #     # data.at[index, "hmbc"] = hmbc_list
    #     # data.at[index, "imp_atoms_df"] = atoms_df.to_json(orient="records")
    #     # data.at[index, "imp_pairs_df"] = pairs_df.to_json(orient="records")
    #     break
    # end = time.time()
    # print(f"Total time: {end - start:.2f} seconds")
    # # Save as new parquet
    # output_path = Path("../../alberts/multimodal-spectroscopic-dataset/data_imp")
    # save_path = output_path / f"aligned_chunk_{file_number}.parquet"
    # data.to_parquet(save_path, engine="pyarrow", index=False)


def main():
    start = time.time()
    file_number = int(sys.argv[1])

    print(f"processing parquet file {file_number}")
    file_path = Path(f"data_new/aligned_chunk_{file_number}.parquet")

    process_file(file_path, file_number)
    end = time.time()
    print(f"\n\nMAIN TIMING\n\ntime spent running main: {end - start:.2f} seconds\n\n")

if __name__ == '__main__':
    main()