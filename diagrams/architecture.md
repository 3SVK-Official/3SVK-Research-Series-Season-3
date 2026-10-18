# System Architecture Design

## Overview

The Adaptive Edge-AI Framework for Real-Time Anomaly Detection implements a resource-aware decision system that dynamically balances local processing and data transmission based on real-time resource constraints and data characteristics.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Data Source                                │
│                    (IoT Sensors / Telemetry)                     │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Data Ingestion                               │
│              - Buffer management                                 │
│              - Stream processing                                  │
│              - Data validation                                    │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Edge Preprocessing                             │
│              - Normalization                                     │
│              - Feature extraction                                │
│              - Windowing (sliding window)                        │
│              - Dimensionality reduction (optional)               │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│           Adaptive Resource/Context Controller                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  State Monitoring:                                      │   │
│  │  - CPU utilization (%)                                 │   │
│  │  - Memory usage (%)                                    │   │
│  │  - Network latency (ms)                                │   │
│  │  - Bandwidth available (Mbps)                          │   │
│  │  - Data difficulty score                              │   │
│  │  - Anomaly confidence (from previous detection)        │   │
│  └─────────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Decision Variables:                                    │   │
│  │  - Processing mode: {LIGHT, STANDARD, HEAVY}           │   │
│  │  - Transmission flag: {LOCAL_ONLY, TRANSMIT}           │   │
│  │  - Model complexity: {LOW, MEDIUM, HIGH}               │   │
│  └─────────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Adaptation Policy:                                     │   │
│  │  Utility = w₁·(1 - CPU_norm) + w₂·(1 - MEM_norm)       │   │
│  │           + w₃·(1 - LAT_norm) + w₄·CONFIDENCE          │   │
│  │  Decision = argmax(Utility) over feasible actions       │   │
│  └─────────────────────────────────────────────────────────┘   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                 Anomaly Detection Engine                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Model Variants (selected by controller):              │   │
│  │  - LIGHT: Z-score detector (fast, low memory)          │   │
│  │  - STANDARD: Autoencoder (balanced)                    │   │
│  │  - HEAVY: LSTM-Autoencoder (high accuracy)             │   │
│  └─────────────────────────────────────────────────────────┘   │
│  Output: anomaly_score ∈ [0, 1], anomaly_label ∈ {0, 1}         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Local Decision                                 │
│              - Threshold comparison                               │
│              - Confidence assessment                             │
│              - Escalation decision                               │
└────────────────────────────┬────────────────────────────────────┘
                             │
              ┌──────────────┴──────────────┐
              ▼                             ▼
┌──────────────────────────┐    ┌──────────────────────────┐
│ Normal / Low Confidence  │    │ Anomaly / High Confidence│
│ → Local handling         │    │ → Response / escalation  │
│ - Log result             │    │ - Alert generation       │
│ - Update statistics      │    │ - Transmit to cloud      │
│ - Continue monitoring    │    │ - Trigger mitigation     │
└──────────────────────────┘    └──────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                  Cloud Coordination (optional)                    │
│              - Global model aggregation                           │
│              - Long-term analytics                                │
│              - Model updates                                      │
│              - Historical pattern analysis                        │
└─────────────────────────────────────────────────────────────────┘
```

## Component Specifications

### 1. Data Ingestion Module

**Responsibilities:**
- Accept streaming data from sensors
- Implement bounded buffer (FIFO queue)
- Validate data integrity
- Handle missing values

**Parameters:**
- Buffer size: configurable (default: 1000 samples)
- Sampling rate: data-dependent
- Validation rules: schema-based

**Complexity:** O(1) per sample insertion

### 2. Edge Preprocessing Module

**Responsibilities:**
- Normalize features to [0, 1] or z-score
- Extract temporal features (rolling statistics)
- Apply sliding window (configurable window size)
- Optional PCA for dimensionality reduction

**Parameters:**
- Window size: w (default: 60 samples)
- Normalization: min-max or z-score
- Feature engineering: rolling mean, std, min, max

**Complexity:** O(w) per sample for window operations

### 3. Adaptive Resource/Context Controller

**Mathematical Formulation:**

**State Space S:**
```
S = {
  cpu_util ∈ [0, 100],           # CPU utilization percentage
  mem_util ∈ [0, 100],          # Memory utilization percentage
  net_latency ∈ [0, ∞),         # Network latency in ms
  bandwidth ∈ [0, ∞),           # Available bandwidth in Mbps
  data_difficulty ∈ [0, 1],     # Estimated difficulty of current data
  anomaly_confidence ∈ [0, 1]   # Confidence from previous detection
}
```

**Decision Space A:**
```
A = {
  (mode, transmit, complexity) where
  mode ∈ {LIGHT, STANDARD, HEAVY}
  transmit ∈ {LOCAL_ONLY, TRANSMIT}
  complexity ∈ {LOW, MEDIUM, HIGH}
}
```

**Utility Function U(s, a):**
```
U(s, a) = w₁·(1 - cpu_util/100) 
        + w₂·(1 - mem_util/100)
        + w₃·(1 - min(net_latency, L_max)/L_max)
        + w₄·anomaly_confidence
        - w₅·transmit_cost(a.transmit)
        - w₆·complexity_cost(a.complexity)
```

Where:
- w₁, w₂, w₃, w₄, w₅, w₆ are configurable weights (sum to 1)
- L_max is maximum acceptable latency threshold
- transmit_cost(LOCAL_ONLY) = 0, transmit_cost(TRANSMIT) = 1
- complexity_cost(LOW) = 0, complexity_cost(MEDIUM) = 0.5, complexity_cost(HIGH) = 1

**Decision Policy:**
```
a* = argmax U(s, a) subject to:
  cpu_util + complexity_cpu(a.complexity) ≤ CPU_threshold
  mem_util + complexity_mem(a.complexity) ≤ MEM_threshold
  if transmit = TRANSMIT: net_latency ≤ L_max
```

**Complexity:** O(|A|) = O(3×2×3) = O(18) = O(1) per decision

**Adaptation Mechanism:**
- State updated every sample (or every N samples for efficiency)
- Decision made based on current state
- Weights can be tuned offline or adapted online

### 4. Anomaly Detection Engine

**Model Variants:**

**LIGHT Mode - Statistical Z-score Detector:**
- Fast training and inference
- Low memory footprint
- Computes Z-scores for anomaly detection
- Complexity: O(n) training, O(1) inference per sample
- Note: Implemented in `src/models/isolation_forest.py` but uses Z-score method

**STANDARD Mode - Autoencoder:**
- Neural network with bottleneck
- Reconstruction error as anomaly score
- Balanced accuracy and efficiency
- Complexity: O(n·d·h) training, O(d·h) inference (d=input dim, h=hidden dim)
- Implemented in `src/models/autoencoder.py`

**HEAVY Mode - LSTM-Autoencoder:**
- Temporal modeling capability
- Higher accuracy for sequential data
- Higher computational cost
- Complexity: O(n·t·d·h²) training, O(t·d·h) inference (t=sequence length)
- Implemented in `src/models/lstm_autoencoder.py`

**Model Selection:**
- LIGHT: When CPU > 90% or memory > 90% (resource constraints)
- STANDARD: Default mode, balanced resource usage
- HEAVY: When CPU < 40% and memory < 40% (abundant resources)
- Note: Under current resource conditions, controller primarily selects STANDARD mode

### 5. Local Decision Module

**Decision Logic:**
```
if anomaly_score > threshold_high:
    label = ANOMALY
    action = ESCALATE
elif anomaly_score > threshold_low:
    label = UNCERTAIN
    action = TRANSMIT_FOR_VERIFICATION
else:
    label = NORMAL
    action = LOCAL_LOG
```

**Parameters:**
- threshold_high: configurable (default: 0.8)
- threshold_low: configurable (default: 0.5)

### 6. Cloud Coordination (Optional)

**Responsibilities:**
- Receive escalated anomalies
- Aggregate global statistics
- Periodic model updates
- Long-term pattern analysis

**Implementation:**
- Implemented in `src/cloud/coordinator.py`
- Simulates centralized processing with HEAVY model (LSTM Autoencoder)
- Used for Baseline A (Centralized Detection)
- Includes simulated network latency (50ms) for transmission

**Note:** For this research, cloud coordination is simulated. The focus is on edge adaptation.

## Data Flow

### Normal Flow (No Anomaly)
1. Data arrives from sensor
2. Preprocessing normalizes and windows data
3. Controller selects LIGHT/STANDARD mode
4. Detection engine processes locally
5. Anomaly score < threshold
6. Result logged locally
7. No transmission

### Anomaly Flow (High Confidence)
1. Data arrives from sensor
2. Preprocessing normalizes and windows data
3. Controller selects appropriate mode
4. Detection engine processes locally
5. Anomaly score > threshold_high
6. Alert generated
7. Data transmitted to cloud (if enabled)
8. Mitigation triggered

### Uncertain Flow (Medium Confidence)
1. Data arrives from sensor
2. Preprocessing normalizes and windows data
3. Controller selects mode
4. Detection engine processes locally
5. threshold_low < anomaly_score < threshold_high
6. Data transmitted for verification
7. Cloud provides final decision

## Computational Complexity Analysis

### Per-Sample Complexity

**Data Ingestion:** O(1)
**Preprocessing:** O(w) where w = window size
**Controller Decision:** O(1)
**Detection:**
- LIGHT (Isolation Forest): O(log n)
- STANDARD (Autoencoder): O(d·h)
- HEAVY (LSTM-Autoencoder): O(t·d·h)
**Decision:** O(1)

**Total per-sample:** O(w) + O(detection) ≈ O(w + d·h) for STANDARD mode

### Memory Complexity

**Buffer:** O(buffer_size)
**Window:** O(w·d)
**Model:**
- LIGHT: O(n_estimators × max_features)
- STANDARD: O(d·h + h·d')
- HEAVY: O(t·d·h²)

**Total:** O(buffer_size + w·d + model_size)

## Failure Modes and Edge Cases

### Resource Exhaustion
- **Detection:** CPU > 95% or memory > 95%
- **Handling:** Force LIGHT mode, skip samples if necessary, log warning

### Network Unavailability
- **Detection:** net_latency > L_max or bandwidth = 0
- **Handling:** Force LOCAL_ONLY mode, buffer data for later transmission

### Model Failure
- **Detection:** Detection engine returns error or invalid score
- **Handling:** Fall back to statistical baseline (z-score), log error

### Data Quality Issues
- **Detection:** Missing values, outliers, invalid ranges
- **Handling:** Impute missing values, flag outliers, use robust preprocessing

## Configuration Parameters

### Controller Weights
- w_cpu: weight for CPU utilization (default: 0.3)
- w_mem: weight for memory utilization (default: 0.2)
- w_lat: weight for latency (default: 0.2)
- w_conf: weight for anomaly confidence (default: 0.2)
- w_transmit: cost for transmission (default: 0.05)
- w_complexity: cost for model complexity (default: 0.05)

### Thresholds
- CPU_threshold: 80%
- MEM_threshold: 80%
- L_max: 100ms (maximum acceptable latency)
- threshold_high: 0.8
- threshold_low: 0.5

### Buffer and Window
- buffer_size: 1000 samples
- window_size: 60 samples
- sampling_rate: data-dependent

## Baseline Architectures

### Baseline A: Centralized Detection
- All data transmitted to cloud
- No local processing
- Single model in cloud (HEAVY mode - LSTM Autoencoder)
- No adaptation
- Implemented in `experiments/baseline_centralized/run.py`
- Uses CloudCoordinator from `src/cloud/coordinator.py`
- Includes simulated network latency (50ms)

### Baseline B: Static Edge Detection
- All data processed locally
- Fixed model (STANDARD mode - Autoencoder)
- No adaptation
- Transmits only anomaly events (30,720 bytes)
- Implemented in `experiments/baseline_static_edge/run.py`
- Uses EdgeProcessor with adaptive=False

### Proposed: Adaptive Edge Framework
- Dynamic local/transmission decision
- Adaptive model selection (LIGHT/STANDARD/HEAVY)
- Resource-aware processing with utility function
- Transmits only anomaly events (30,720 bytes)
- Implemented in `experiments/proposed/run.py`
- Uses EdgeProcessor with adaptive=True
- Uses AdaptiveController from `src/adaptive/controller.py`
- Under current resource constraints, primarily selects STANDARD mode
