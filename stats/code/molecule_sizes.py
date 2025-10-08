import pandas as pd 
import os
import re
import rdkit
import matplotlib.pyplot as plt
import pickle as pkl

path = "../../2d_model/data/tgt-train.txt"

with open(path, "r") as f:
    smiles_list = [re.sub(r'[^A-Za-z]', '', line) for line in f if line.strip()]

# turn list into Series
smiles_series = pd.Series(smiles_list)

# remove both lowercase and uppercase r/l
smiles_series = smiles_series.str.replace(r"[rRlL]", "", regex=True)

#gets the number of heavy atoms
sizes = smiles_series.str.len()


plt.hist(sizes, bins=40, edgecolor="black")
plt.xlabel("Number of Heavy Atoms")
plt.ylabel("Count of molecules")
plt.title("Distribution of molecule sizes in training data")

# Save the figure
plt.savefig("../plots/molecule_size_distribution.png", dpi=300, bbox_inches="tight")

# Open the pickle file in read-binary mode
with open("../data/correct_assignment_sizes.pkl", "rb") as f:
    correct_molecules = pkl.load(f)



plt.hist(
    sizes, 
    bins=40, 
    alpha=0.5, 
    label="training_data", 
    edgecolor="black"
)
plt.hist(
    correct_molecules, 
    bins=40, 
    alpha=0.5, 
    label="corrcetly_assigned_molecules", 
    edgecolor="black"
)

plt.xlabel("Number of Heavy Atoms")
plt.ylabel("Count of Molecules")
plt.title("Distribution of Molecule Sizes")
plt.legend()
#plt.show()

# Save the figure
plt.savefig("../plots/overlay.png", dpi=300, bbox_inches="tight")