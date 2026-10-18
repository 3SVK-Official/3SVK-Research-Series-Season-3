from scipy.io import loadmat
from pathlib import Path
import numpy as np

# Data folder ka path
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

# File load
file_path = DATA_DIR / "100.mat"
data = loadmat(file_path)

# Vibration signal
signal = data["X100_DE_time"].flatten()

# RMS calculate
rms = np.sqrt(np.mean(signal ** 2))

# Standard deviation
std = np.std(signal)

# Mean
mean = np.mean(signal)

# Peak value
peak = np.max(np.abs(signal))

print("Signal features:")
print("Mean:", mean)
print("RMS:", rms)
print("Standard Deviation:", std)
print("Peak:", peak)
from scipy.io import loadmat
from pathlib import Path
import numpy as np

# data folder ka path
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

# 100.mat file
file_path = DATA_DIR / "100.mat"

# file load karo
data = loadmat(file_path)

# drive-end vibration signal
signal = data["X100_DE_time"].flatten()

# ek window mein 1000 samples
WINDOW_SIZE = 1000

print("Total samples:", len(signal))
print("Window size:", WINDOW_SIZE)

# signal ko 1000-1000 samples ke pieces mein todna
for start in range(0, len(signal) - WINDOW_SIZE + 1, WINDOW_SIZE):

    window = signal[start:start + WINDOW_SIZE]

    # har window ke features
    rms = np.sqrt(np.mean(window ** 2))
    std = np.std(window)
    peak = np.max(np.abs(window))

    print(
        f"Window {start // WINDOW_SIZE + 1}: "
        f"RMS={rms:.6f}, "
        f"STD={std:.6f}, "
        f"Peak={peak:.6f}"
    )

    # abhi sirf first 5 windows
    if start >= 4000:
        break