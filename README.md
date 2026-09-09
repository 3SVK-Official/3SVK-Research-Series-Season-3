# 3SVK-Research-Series-Season-3 
Official research archive, documentation, and proceedings for the National Research & Innovation Challenge Season 3 by 3SVK.

---

## 🔒 Intellectual Property, Copyright & Legal Notice
© 2026 3SVK Official. All rights reserved.

The research tracks, problem statements, documentation, frameworks, and structural designs published in this repository are the exclusive intellectual property of 3SVK, protected under the Indian Copyright Act, 1957, and international copyright treaties.

Permitted Use: Registered participants may use the provided templates and resources strictly for the purpose of competing in the National Research & Innovation Challenge Season 3.
Legal Prohibition: In accordance with the Copyright Act of India, any unauthorized reproduction, redistribution, adaptation, commercial exploitation, or plagiarism of these works without explicit written consent from 3SVK constitutes an infringement under Section 51 and is punishable under Section 63 and other applicable provisions of Indian law.

---

## 📚 Official Citation
If you use, reference, or build upon this research series, please cite it via our permanent Zenodo DOI:
> 3SVK Official. (2026). 3SVK Research Series Season 3: Official Archive & Proceedings. Zenodo. https://doi.org/10.5281/zenodo.22008262

---

## Adaptive Edge-AI Framework for Real-Time Anomaly Detection

A resource-aware adaptive framework for real-time anomaly detection at the edge, dynamically balancing detection accuracy with computational constraints.

## Research Objective

This project investigates whether an adaptive, resource-aware edge-AI framework can detect anomalies in real time while reducing inference latency, network/data-transfer overhead, and computational resource consumption compared with a conventional centralized detection architecture without materially degrading detection performance.

## Problem Addressed

Traditional centralized anomaly detection systems incur high latency and network overhead, while static edge-based approaches lack flexibility to adapt to varying resource conditions. Existing edge-based systems typically employ fixed model complexity, leading to either over-provisioning (complex models exceeding available resources) or under-provisioning (simple models failing to detect subtle anomalies).

## Implemented Approach

The framework implements a utility-based adaptive controller that:
- Dynamically selects between three detection models of varying complexity based on real-time CPU, memory, and network conditions
- Optimizes transmission decisions to balance local processing with cloud offloading when beneficial
- Employs a mathematically defined utility function that explicitly considers CPU, memory, latency, detection confidence, transmission costs, and model complexity
- Uses validation-based threshold calibration to prevent test-set leakage

## Adaptive Controller

The adaptive controller maintains a state vector:
```
s = (cpu_util, mem_util, net_latency, bandwidth, data_difficulty, anomaly_confidence)
```

At each decision point, the controller selects a model mode `m ∈ {LIGHT, STANDARD, HEAVY}` and transmission decision `t ∈ {LOCAL_ONLY, TRANSMIT}` by maximizing:
```
U(m, t) = w_cpu * (1 - cpu_cost(m)) + 
          w_mem * (1 - mem_cost(m)) + 
          w_lat * (1 - latency_cost(m, t)) + 
          w_conf * confidence(m) - 
          w_trans * trans_cost(t) - 
          w_comp * complexity_cost(m)
```

Subject to feasibility constraints:
```
cpu_util + cpu_overhead(m) ≤ cpu_threshold
mem_util + mem_overhead(m) ≤ mem_threshold
if t = TRANSMIT: net_latency ≤ latency_max
```

## Dataset

The framework uses synthetic time-series data with:
- 5,000 samples
- 5% anomaly rate
- Train/Val/Test split: 70/15/15
- Window size: 60 samples
- Normal samples: sinusoidal pattern with Gaussian noise
- Anomaly patterns: spikes, dips, sustained shifts, amplitude changes

## Detection Models

Three models of increasing complexity are implemented:

- **LIGHT**: Statistical Z-score based anomaly detector (fast, low memory)
- **STANDARD**: Autoencoder with reconstruction error (balanced)
- **HEAVY**: LSTM Autoencoder for temporal patterns (high accuracy, high computational cost)

## Leakage Prevention

To prevent test-set leakage, all three systems (Centralized, Static Edge, Adaptive Edge) use validation-based threshold calibration with F1 optimization on the validation set before evaluating on the test set.

## Validation-Based Threshold Calibration

The `ThresholdCalibrator` class implements multiple calibration methods:
- `f1_optimize`: Maximize F1 score on validation data (used in experiments)
- `percentile`: Use fixed percentile (e.g., 95th)
- `precision_constrained`: Maximize recall subject to precision constraint
- `recall_constrained`: Maximize precision subject to recall constraint

This ensures fair comparison between systems and prevents overfitting to the test set.

## Project Structure

```
3svk/
├── configs/                 # Configuration files
│   └── default_config.yaml
├── diagrams/                # Architecture diagrams
│   └── architecture.md
├── experiments/             # Experiment scripts
│   ├── baseline_centralized/
│   ├── baseline_static_edge/
│   ├── proposed/
│   ├── ablation/
│   ├── verify_results.py
│   └── generate_figures.py
├── figures/                 # Generated figures and tables
├── references/              # Literature review and research gap
│   ├── literature_review.md
│   └── research_gap.md
├── results/                 # Experiment results (JSON)
├── src/                     # Source code
│   ├── adaptive/           # Adaptive controller
│   ├── cloud/              # Cloud coordinator
│   ├── data/               # Data loading and streaming
│   ├── edge/               # Edge processor
│   ├── evaluation/         # Metrics and monitoring
│   ├── models/             # Detection models
│   └── preprocessing/      # Data preprocessing
├── tests/                  # Unit tests
├── requirements.txt         # Python dependencies
├── research-paper.md       # Complete research paper
└── README.md              # This file
```

## Installation

### Prerequisites

- Python 3.14.6
- pip

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd 3svk
```

2. Install dependencies:
```bash
python -m pip install -r requirements.txt
```

## Usage

### Running Experiments

#### Run All Experiments
```bash
python experiments/verify_results.py
```

This will:
- Run baseline centralized experiment
- Run baseline static edge experiment
- Run proposed adaptive edge experiment
- Save results to `results/` directory

#### Run Individual Experiments
```bash
# Baseline A: Centralized Detection
python experiments/baseline_centralized/run.py

# Baseline B: Static Edge Detection
python experiments/baseline_static_edge/run.py

# Proposed: Adaptive Edge Framework
python experiments/proposed/run.py

# Ablation Study
python experiments/ablation/run.py
```

#### Generate Figures and Tables
```bash
python experiments/generate_figures.py
```

This will generate:
- Benchmark comparison table
- Performance comparison plots
- Summary report

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_data.py -v
python -m pytest tests/test_preprocessing.py -v
python -m pytest tests/test_adaptive.py -v
```

## Configuration

Edit `configs/default_config.yaml` to customize:

- **Data**: Dataset parameters, window size, anomaly ratio
- **Preprocessing**: Normalization method, feature engineering
- **Models**: Model architectures and hyperparameters
- **Controller**: Utility function weights and thresholds
- **Evaluation**: Metrics to compute
- **Experiments**: Random seed, sample sizes

## Architecture

### Components

1. **Data Ingestion** (`src/data/`)
   - `DataLoader`: Loads and splits datasets
   - `DataStream`: Simulates streaming data with buffering

2. **Preprocessing** (`src/preprocessing/`)
   - `Preprocessor`: Normalization and window creation
   - `FeatureEngineer`: Rolling statistics and difference features

3. **Detection Models** (`src/models/`)
   - `IsolationForestModel`: Lightweight statistical detector
   - `AutoencoderModel`: Standard autoencoder
   - `LSTMAutoencoderModel`: Heavy LSTM autoencoder

4. **Adaptive Controller** (`src/adaptive/`)
   - `AdaptiveController`: Resource-aware decision making with utility function

5. **Processing** (`src/edge/`, `src/cloud/`)
   - `EdgeProcessor`: Local processing with adaptive model selection
   - `CloudCoordinator`: Centralized processing simulation

6. **Evaluation** (`src/evaluation/`)
   - `MetricsCalculator`: Detection and system metrics
   - `SystemMonitor`: CPU, memory, and network monitoring

## Three Implemented Systems

### 1. Centralized Detection (Baseline A)
- All data transmitted to cloud for processing
- Uses HEAVY model (LSTM Autoencoder) in cloud
- No local processing
- No adaptation

### 2. Static Edge Detection (Baseline B)
- All data processed locally
- Fixed STANDARD model (Autoencoder)
- No adaptation
- Transmits only anomaly events (30,720 bytes)

### 3. Adaptive Edge Framework (Proposed)
- Dynamic local/transmission decision
- Adaptive model selection (LIGHT/STANDARD/HEAVY)
- Resource-aware processing with utility function
- Transmits only anomaly events (30,720 bytes)
- Under current resource constraints, controller primarily selects STANDARD mode

## Experimental Methodology

### Detection Metrics
- Accuracy, Precision, Recall, F1-Score
- ROC-AUC, PR-AUC
- False Positive Rate, False Negative Rate

### Latency Measurement
- Centralized: Includes network transmission (uplink + downlink + inference)
- Edge systems: Measure local inference only
- Reported metrics: mean, std, min, max, p50, p95, p99

### CPU Measurement
- Mean CPU utilization percentage
- Standard deviation
- Min/max values

### Memory Measurement
- Mean memory utilization percentage
- Standard deviation
- Min/max values

### Communication Measurement
- Total data transmitted in bytes
- Edge systems transmit only anomaly events
- Centralized transmits all data

## Current Verified Results

Results from `results/final_results.json` (validated on 2026-09-09):

### Detection Performance

| Method | Accuracy | Precision | Recall | F1-Score | ROC-AUC | PR-AUC |
|--------|----------|-----------|--------|----------|---------|--------|
| Centralized | 0.2142 | 0.0797 | 1.0000 | 0.1476 | 0.6190 | 0.0814 |
| Static Edge | 0.8683 | 0.1562 | 0.2128 | 0.1802 | 0.6128 | 0.1123 |
| Adaptive Edge (Ours) | 0.8683 | 0.1562 | 0.2128 | 0.1802 | 0.6128 | 0.1123 |

**Note**: All methods use validation-based threshold calibration (F1 optimization) to prevent test-set leakage. Edge methods achieve better F1 due to improved precision. The adaptive controller makes resource-aware decisions but primarily selects the STANDARD model under current resource constraints.

### System Performance

| Method | Latency (ms) | CPU (%) | Memory (%) | Data (bytes) |
|--------|-------------|---------|------------|--------------|
| Centralized | 101.13 | 59.66 | 77.88 | 331,680 |
| Static Edge | 0.39 | 37.90 | 77.30 | 30,720 |
| Adaptive Edge (Ours) | 0.50 | 47.61 | 79.90 | 30,720 |

**Note**: Centralized latency includes network transmission (uplink + downlink + inference). Edge systems measure local inference only. Edge systems transmit only anomaly events (30,720 bytes), while centralized transmits all data (331,680 bytes).

### Key Improvements

- **Latency**: 99.61% reduction vs Centralized (Static Edge), 99.51% reduction vs Centralized (Adaptive Edge)
  - Note: Latency reduction is due to network elimination (architectural advantage), not algorithmic improvement
- **Data Transmission**: 90.74% reduction vs Centralized (both Edge methods)
  - Note: Data reduction due to local processing (architectural advantage)
- **Detection Performance**: Edge methods achieve 22.0% higher F1 vs Centralized (0.1802 vs 0.1476)

## Documentation

- **Research Paper**: `research-paper.md` - Complete research paper with methodology, results, and discussion
- **Architecture**: `diagrams/architecture.md` - Detailed system architecture
- **Literature Review**: `references/literature_review.md` - Related work and background
- **Research Gap**: `references/research_gap.md` - Problem statement and contribution

## Reproducibility

All experiments use fixed random seeds (configured in `default_config.yaml`) to ensure reproducibility. Results are saved as JSON files in the `results/` directory.

## Python 3.14.6 Compatibility

This project is tested and verified to work with Python 3.14.6. All dependencies are compatible with Python 3.14.6.

## Limitations

1. **Synthetic Data**: Evaluation on synthetic data may not reflect real-world performance
2. **Controller Tuning**: Utility function weights require domain-specific calibration for optimal model switching
3. **Single Run**: Results from single run; multiple runs with statistical reporting recommended for production
4. **Detection Performance**: All methods have low F1 scores (<0.2), indicating challenging detection task or need for model improvement
5. **Adaptive Behavior**: Under current resource constraints, the adaptive controller primarily selects the STANDARD mode, resulting in behavior similar to static edge processing

## License

This project is submitted for the 3SVK Challenge.

## Contact

For questions or issues, please refer to the research paper or contact the authors.
