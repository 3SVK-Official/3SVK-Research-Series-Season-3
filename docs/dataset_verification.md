# Dataset Verification and Leakage Prevention

## Dataset Source and Identity

- **Dataset Type**: Synthetic time-series data
- **Generation Method**: Sinusoidal with noise, anomalies as spikes/dips/shifts
- **Sample Count**: 5,000 samples
- **Feature Count**: 1 feature (univariate time series)
- **Anomaly Count**: 250 anomalies (5% anomaly ratio)
- **Class Distribution**: 95% normal (4,750), 5% anomaly (250)

## Data Generation Details

Location: `src/data/loader.py` lines 63-114

- Normal data: `sin(t) + 0.1 * randn(n_samples)`
- Anomaly types:
  - Large spike: +5 to +10 (40% of anomalies)
  - Large dip: -10 to -5 (30% of anomalies)
  - Sustained shift: 3-8 consecutive points with shift (15% of anomalies)
  - Amplitude spike: multiply by 3-5x (15% of anomalies)

## Preprocessing Pipeline

1. **Normalization**: MinMax normalization (configurable to z-score)
2. **Windowing**: Sliding window of size 60
3. **Feature Engineering**: Rolling statistics (mean, std, min, max) if enabled

## Train/Validation/Test Split

**Method**: Temporal sequential split (no shuffling to preserve time-series structure)

- **Training**: 70% (3,500 samples, ~175 anomalies)
  - Purpose: Model fitting/training
  - Labels used: YES (for supervised training where applicable)
  
- **Validation**: 15% (750 samples, ~37 anomalies)
  - Purpose: Threshold calibration, parameter selection
  - Labels used: YES (for threshold optimization)
  - **Critical**: Test labels NEVER used for threshold tuning
  
- **Test**: 15% (750 samples, ~38 anomalies)
  - Purpose: Final evaluation only
  - Labels used: YES (for metric calculation only)
  - **Critical**: Test data NEVER used for model fitting or threshold selection

## Leakage Prevention Controls

### 1. Data Split Isolation
- Train, validation, and test sets are strictly separated
- No data leakage between splits (sequential split)
- Preprocessing fit on training data only, then applied to val/test

### 2. Threshold Calibration
- Threshold calibrated on validation data ONLY
- Test labels never used for threshold selection
- Calibration method: F1 optimization on validation set

### 3. Model Training
- Models trained on training data ONLY
- Validation and test data never used during training
- Early stopping uses validation set (not test set)

### 4. Evaluation Protocol
- Test set used ONCE for final evaluation
- No test-set-based parameter tuning
- All threshold decisions made before seeing test data

## Verified Split Configuration

```python
# From src/data/loader.py train_val_test_split()
train_ratio = 0.7  # 70% for training
val_ratio = 0.15   # 15% for validation
test_ratio = 0.15  # 15% for test (implicit: 1 - 0.7 - 0.15)
```

## Anomaly Distribution Across Splits

- **Training**: ~175 anomalies (used for model fitting)
- **Validation**: ~37 anomalies (used for threshold calibration)
- **Test**: ~38 anomalies (used for final evaluation only)

## Verification Status

✓ Dataset source verified (synthetic, clearly disclosed)
✓ Sample count verified (5,000)
✓ Feature count verified (1)
✓ Labels verified (binary: 0=normal, 1=anomaly)
✓ Anomaly count verified (250, 5%)
✓ Class distribution verified (95/5)
✓ Preprocessing verified (normalization, windowing)
✓ Train/val/test separation verified (70/15/15)
✓ Leakage prevention documented

## Methodology Compliance

**Training data → model fitting**: ✓
- Models trained on training set only
- Preprocessing fit on training data only

**Validation data → threshold calibration / parameter selection**: ✓
- Threshold calibrated on validation set only
- Early stopping uses validation set
- Test labels never used for threshold tuning

**Test data → final evaluation only**: ✓
- Test set used once for final metrics
- No test-set-based parameter tuning
- All decisions made before seeing test data

## Date Verified

September 9, 2026
