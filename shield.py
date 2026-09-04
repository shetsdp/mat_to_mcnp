import os
import sys
import numpy as np
import subprocess
import re
import csv
from sys import exit
import shutil
import matplotlib.pyplot as plt

# -------------------------
# Energy grid (log spaced)
# -------------------------
energies = [1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1.0, 10.0]

results = []

print(energies)



# -------------------------
# Read template
# -------------------------
with open("inp", "r") as f:
    template = f.read()

# -------------------------
# Loop over energies
# -------------------------
for E in energies:
    folder = f"runs/E_{E:.0e}"
    os.makedirs(folder, exist_ok=True)

    input_file = os.path.join(folder, "inp")
    output_file = os.path.join(folder, "out")

    # Replace energy
    content = template.replace("{ene}", f"{E:.5e}")

    with open(input_file, "w") as f:
        f.write(content)

    # -------------------------
    # Run MCNP
    # -------------------------
    subprocess.run(
        "mcnp5 i=inp o=out",
        shell=True,
        cwd=folder
        )

    # -------------------------
    # Parse F1 tally
    # -------------------------
    with open(output_file, "r") as f:
        text = f.read()

    match = re.search(r"surface\s+\d+\s+([\d.E+-]+)\s+([\d.E+-]+)", text)

    if match:
        value = float(match.group(1))
        error = float(match.group(2))
    else:
        value, error = None, None

    results.append([E, value, error])


    #sys.exit()

# -------------------------
# Save results
# -------------------------
with open("results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Energy (MeV)", "Transmission", "Rel Error"])
    writer.writerows(results)

# Extract columns
E = [r[0] for r in results]
values = [r[1] for r in results]
errors = [r[2] for r in results]

# Plot with error bars
plt.errorbar(E, values, yerr=errors, fmt='o-', capsize=3)

# Set x-axis to log scale
plt.xscale('log')

# Labels
plt.xlabel('Energy (MeV)')
plt.ylabel('Value')
plt.title('Log-scale X-axis Plot')

plt.grid(True, which="both", ls="--")
plt.show()

print("Done!")

""" if os.path.exists("runs"):
    shutil.rmtree("runs")
    print("Runs folder deleted.")
else:
    print("Runs folder not found.") """