# Dataset Documentation

## Synthetic Time-Series Anomaly Dataset

### Overview
Custom synthetic dataset generated for edge anomaly detection research. The dataset simulates streaming time-series data with various anomaly patterns.

### Generation Method
- **Base signal**: Sinusoidal wave with Gaussian noise
- **Normal data**: `sin(t) + 0.1 * N(0,1)`
- **Anomaly ratio**: 5% (configurable)

### Anomaly Patterns
Four types of anomalies are injected:
1. **Large spikes**: Add 5-10 to signal (40% of anomalies)
2. **Large dips**: Subtract 5-10 from signal (30% of anomalies)
3. **Sustained shifts**: Add/subtract 3-6 for 3-8 consecutive samples (15% of anomalies)
4. **Amplitude spikes**: Multiply signal by 3-5x (15% of anomalies)

### Dataset Characteristics
- **Total samples**: 5000 (configurable)
- **Number of anomalies**: ~250 (5% of total)
- **Features**: 1 (univariate time-series)
- **Window size**: 60 samples
- **Normalization**: Min-max scaling [0, 1]

### Train/Validation/Test Split
- **Train**: 70% (3500 samples)
- **Validation**: 15% (750 samples) - used for threshold calibration
- **Test**: 15% (750 samples) - used for final evaluation only

### Label Adjustment
After windowing (window_size=60), labels are adjusted to align with window boundaries:
- Original test labels: 750 samples
- Windowed test labels: 691 samples (loss of 59 samples due to windowing)
- Test anomalies after windowing: ~24-48 samples (varies by random seed)

### Detectability
Anomalies are partially detectable:
- Simple statistical methods achieve F1 ~0.11-0.13
- Autoencoder achieves F1 ~0.16 with proper threshold calibration
- High recall (>0.9) but low precision (~0.09) due to window-based signal dilution

### Advantages
- Fully reproducible with fixed random seed
- No external dependencies
- Known ground truth
- Configurable size and anomaly ratio
- Multiple anomaly types for robustness

### Limitations
- Synthetic nature may not reflect real-world patterns
- Window-based detection dilutes single-point anomalies
- Class imbalance (5% anomalies) requires careful threshold selection
- Not representative of specific real-world domains (e.g., IoT, industrial)

### Usage
```python
from src.data.loader import DataLoader
import yaml

config = yaml.safe_load(open('configs/default_config.yaml'))
loader = DataLoader(config)
data, labels = loader.load_dataset('synthetic', n_samples=5000, anomaly_ratio=0.05)
```

### Reproducibility
Set random seed in config:
```yaml
experiments:
  random_seed: 42
```

### Future Improvements
- Consider adding multivariate patterns
- Add seasonal/cyclical components
- Include context-dependent anomalies
- Evaluate on real-world datasets (NAB, KDD, etc.)
