# Python 3.14.6 Compatibility Documentation

## Python Version
- **Target Version**: Python 3.14.6
- **Status**: Verified and tested

## Dependencies

### Core Dependencies

| Package | Version | Purpose | Compatibility Status |
|---------|---------|---------|---------------------|
| numpy | >=1.26.0 | Numerical computing, array operations | ✅ Compatible |
| pandas | >=2.2.0 | Data manipulation, rolling features | ✅ Compatible |
| torch | >=2.4.0 | Deep learning models (Autoencoder, LSTM) | ✅ Compatible |

### Visualization

| Package | Version | Purpose | Compatibility Status |
|---------|---------|---------|---------------------|
| matplotlib | >=3.9.0 | Plotting and figure generation | ✅ Compatible |
| seaborn | >=0.13.0 | Statistical visualization | ✅ Compatible |

### Configuration

| Package | Version | Purpose | Compatibility Status |
|---------|---------|---------|---------------------|
| pyyaml | >=6.0 | Configuration file parsing | ✅ Compatible |

### System Monitoring

| Package | Version | Purpose | Compatibility Status |
|---------|---------|---------|---------------------|
| psutil | >=6.0.0 | CPU and memory monitoring | ✅ Compatible |

### Testing

| Package | Version | Purpose | Compatibility Status |
|---------|---------|---------|---------------------|
| pytest | >=8.3.0 | Unit testing framework | ✅ Compatible |
| pytest-cov | >=5.0.0 | Code coverage for tests | ✅ Compatible |

### Type Checking (Optional)

| Package | Version | Purpose | Compatibility Status |
|---------|---------|---------|---------------------|
| mypy | >=1.11.0 | Static type checking | ✅ Compatible |

## Removed Dependencies

The following dependencies were removed as they are not used in the codebase:

- **scipy**: Not used (numpy provides sufficient numerical operations)
- **scikit-learn**: Not used (metrics implemented manually to avoid dependency)
- **torchvision**: Not used (only torch is needed for models)
- **tqdm**: Not used (no progress bars in current implementation)
- **jupyter**: Optional (not required for core functionality)
- **notebook**: Optional (not required for core functionality)
- **memory-profiler**: Not used (psutil provides sufficient monitoring)
- **requests**: Not used (no external API calls)

## Installation

```bash
python -m pip install -r requirements.txt
```

## Verification

To verify Python 3.14.6 compatibility:

1. Check Python version:
```bash
python --version
```

2. Install dependencies:
```bash
python -m pip install -r requirements.txt
```

3. Run tests:
```bash
python -m pytest tests/ -v
```

4. Run experiments:
```bash
python experiments/verify_results.py
```

## Notes

- All dependencies are compatible with Python 3.14.6
- The codebase avoids sklearn dependency by implementing metrics manually
- PyTorch is used for deep learning models (Autoencoder, LSTM Autoencoder)
- psutil is used for system resource monitoring
- The implementation is designed to work with minimal external dependencies
