from scipy.io import loadmat
from pathlib import Path

# Project ke data folder ka path
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

# Pehli .mat file automatically dhoondho
mat_files = list(DATA_DIR.glob("*.mat"))

if not mat_files:
    print("Data folder mein koi .mat file nahi mili.")
else:
    file_path = mat_files[0]

    print("File mil gayi:")
    print(file_path.name)

    # MATLAB file read karo
    data = loadmat(file_path)

    print("\nFile ke andar available variables:")
    for key in data.keys():
        if not key.startswith("__"):
            print(key)