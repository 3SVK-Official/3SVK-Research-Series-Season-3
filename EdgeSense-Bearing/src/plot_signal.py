from scipy.io import loadmat
from pathlib import Path
import matplotlib.pyplot as plt

# Project ke data folder ka path
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

# 100.mat file
file_path = DATA_DIR / "100.mat"

# MATLAB file load karo
data = loadmat(file_path)

# Drive-end vibration signal nikalo
signal = data["X100_DE_time"].flatten()

# RPM nikalo
rpm = data["X100RPM"].flatten()[0]

print("RPM:", rpm)
print("Total vibration samples:", len(signal))

# Pehle 2000 samples graph mein dikhayenge
samples_to_plot = 2000

plt.figure(figsize=(12, 5))
plt.plot(signal[:samples_to_plot])

plt.title("CWRU Bearing Vibration Signal - 100.mat")
plt.xlabel("Sample Number")
plt.ylabel("Vibration Amplitude")
plt.grid(True)

plt.show()