# EdgeSense-Bearing

## Lightweight Cloud-Edge AI for Real-Time Bearing Fault Diagnosis

### Abstract

Industrial motors are widely used in manufacturing and automation systems, where bearing faults can lead to vibration abnormalities and unexpected equipment downtime. This project presents a lightweight machine-learning pipeline for bearing fault diagnosis using vibration signals.

The proposed system processes vibration data in fixed-size windows and extracts statistical features including mean, root mean square (RMS), standard deviation, and peak amplitude. Multiple machine-learning models are evaluated for classification of normal and faulty bearing conditions.

The project also investigates a software-based edge-cloud data-flow approach. Instead of continuously transmitting raw vibration windows, compact extracted features can be generated at the edge and transmitted for classification. The study measures classification performance, inference latency, process memory, and theoretical payload reduction.

All reported experimental values are generated from the implemented code and stored in the project results directory.

---

## 1. Introduction

Bearing condition monitoring is an important part of predictive maintenance for rotating machinery. Changes in bearing condition can affect vibration signals, making vibration analysis useful for fault diagnosis.

Traditional monitoring systems may transmit large amounts of sensor data to a centralized processing system. Processing selected information closer to the data source can reduce the amount of information that needs to be transferred.

This project explores a lightweight machine-learning based approach for bearing fault classification using vibration measurements from the Case Western Reserve University (CWRU) Bearing Data Center dataset.

The work focuses on four initial bearing-condition classes:

1. Normal
2. Inner Race Fault
3. Ball Fault
4. Outer Race Fault

---

## 2. Problem Statement

Continuous vibration monitoring can generate a large volume of sensor data. Sending complete high-frequency vibration signals to a centralized system can increase data-transfer requirements.

The research problem investigated in this project is:

> Can compact vibration features extracted locally be used for bearing fault classification while reducing the amount of data required for transmission compared with transmitting the complete vibration window?

---

## 3. Objectives

The objectives of this study are:

- To load and process bearing vibration signals.
- To divide continuous vibration signals into fixed-size windows.
- To extract statistical vibration features.
- To train machine-learning classification models.
- To compare different classification approaches.
- To measure classification performance using accuracy, precision, recall and F1-score.
- To measure inference latency and process memory.
- To compare raw-signal and compact-feature payload sizes.
- To evaluate a software-based edge-cloud data-flow approach.

---

## 4. Dataset

The experiments use the Case Western Reserve University Bearing Data Center dataset.

The dataset provides vibration measurements obtained from bearing experiments under normal and faulty operating conditions. The project uses the drive-end vibration signal for the primary processing pipeline.

The downloaded MATLAB files contain vibration time-series variables and RPM information.

---

## 5. Proposed Methodology

The overall processing pipeline is:

```text
CWRU Vibration Data
        |
        v
Signal Loading
        |
        v
Fixed-Size Windowing
        |
        v
Feature Extraction
        |
        v
Machine Learning
        |
        v
Fault Classification
```text
CWRU Vibration Data
        |
        v
Signal Loading
        |
        v
Fixed-Size Windowing
        |
        v
Feature Extraction
        |
        v
Machine Learning
        |
        v
Fault Classification
```
## 6. Signal Processing

The drive-end vibration signal is extracted from each MATLAB data file.

The continuous vibration signal is divided into fixed-size windows of 1000 samples.

For each window, four statistical features are calculated:

- Mean
- Root Mean Square (RMS)
- Standard Deviation
- Peak Amplitude

The extracted features are then used as inputs to the machine-learning models.

### 6.1 Root Mean Square

RMS represents the overall magnitude of the vibration signal.

\[
RMS = \sqrt{\frac{1}{N}\sum_{i=1}^{N}x_i^2}
\]

### 6.2 Standard Deviation

Standard deviation measures the variation of vibration values around their mean.

### 6.3 Peak Amplitude

Peak amplitude represents the maximum absolute vibration value within a window.

---

## 7. Machine Learning Models

Four machine-learning classification models are compared:

1. Logistic Regression
2. Decision Tree
3. K-Nearest Neighbors (KNN)
4. Random Forest

All models use the same extracted features and the same train/test grouping.

---

## 8. Evaluation Metrics

The classification models are evaluated using:

- Accuracy
- Precision
- Recall
- F1-score
- Confusion Matrix

The system-level evaluation includes:

- Inference latency
- Process RSS memory
- Raw vibration payload size
- Feature payload size
- Theoretical payload reduction

---

## 9. Edge-Cloud Experiment

Two processing approaches are evaluated.

### 9.1 Cloud-style Processing

```text
Raw Vibration Window
        |
        v
Data Transmission
        |
        v
Feature Extraction
        |
        v
Machine Learning
        |
        v
Prediction
```

### 9.2 Edge-style Processing

```text
Raw Vibration Window
        |
        v
Feature Extraction at Edge
        |
        v
Compact Feature Payload
        |
        v
Data Transmission
        |
        v
Machine Learning
        |
        v
Prediction
```

The edge-cloud experiment is implemented as a local software emulation. It does not measure real Internet network latency or physical edge-device performance.

---

## 10. Experimental Results

The experimental outputs are generated automatically by the project scripts.

The main result files are:

```text
results/model_comparison.csv
results/benchmark_results.csv
results/edge_cloud_comparison.csv
results/final_results_summary.csv
```

The classification results are compared across the four machine-learning models.

System-level measurements include prediction latency, process memory and payload size.

The exact numerical values reported in the final version of this section will be taken directly from the generated result files.

---

## 11. Limitations

The current implementation has the following limitations:

- The edge environment is simulated using a local computer.
- No physical sensor or dedicated edge device is used.
- The payload reduction experiment is a theoretical/local comparison.
- Process RSS is used as a system-level memory measurement.
- The study uses a limited subset of the available bearing conditions.

---

## 12. Future Work

Future work may include:

- Deployment on Raspberry Pi or another dedicated edge device.
- Real-time vibration sensor acquisition.
- Real network latency measurement.
- Adaptive sampling based on signal conditions.
- Additional fault severities.
- Additional motor loads and speeds.
- Cloud dashboard integration.
- Lightweight neural-network models.

---

## 13. Conclusion

This project develops a lightweight machine-learning pipeline for bearing fault diagnosis using motor vibration signals.

The workflow combines signal windowing, statistical feature extraction, machine-learning classification and a software-based edge-cloud data-flow experiment.

The study provides a reproducible framework for investigating the trade-off between vibration-data transmission and local feature processing.

The final conclusions are based on the experimentally generated classification and system-level measurements stored in the project results directory.## 6. Signal Processing

The drive-end vibration signal is extracted from each MATLAB data file.

The continuous vibration signal is divided into fixed-size windows of 1000 samples.

For each window, four statistical features are calculated:

- Mean
- Root Mean Square (RMS)
- Standard Deviation
- Peak Amplitude

The extracted features are then used as inputs to the machine-learning models.

### 6.1 Root Mean Square

RMS represents the overall magnitude of the vibration signal.

\[
RMS = \sqrt{\frac{1}{N}\sum_{i=1}^{N}x_i^2}
\]

### 6.2 Standard Deviation

Standard deviation measures the variation of vibration values around their mean.

### 6.3 Peak Amplitude

Peak amplitude represents the maximum absolute vibration value within a window.

---

## 7. Machine Learning Models

Four machine-learning classification models are compared:

1. Logistic Regression
2. Decision Tree
3. K-Nearest Neighbors (KNN)
4. Random Forest

All models use the same extracted features and the same train/test grouping.

---

## 8. Evaluation Metrics

The classification models are evaluated using:

- Accuracy
- Precision
- Recall
- F1-score
- Confusion Matrix

The system-level evaluation includes:

- Inference latency
- Process RSS memory
- Raw vibration payload size
- Feature payload size
- Theoretical payload reduction

---

## 9. Edge-Cloud Experiment

Two processing approaches are evaluated.

### 9.1 Cloud-style Processing

```text
Raw Vibration Window
        |
        v
Data Transmission
        |
        v
Feature Extraction
        |
        v
Machine Learning
        |
        v
Prediction
```

### 9.2 Edge-style Processing

```text
Raw Vibration Window
        |
        v
Feature Extraction at Edge
        |
        v
Compact Feature Payload
        |
        v
Data Transmission
        |
        v
Machine Learning
        |
        v
Prediction
```

The edge-cloud experiment is implemented as a local software emulation. It does not measure real Internet network latency or physical edge-device performance.

---

## 10. Experimental Results

The experimental outputs are generated automatically by the project scripts.

The main result files are:

```text
results/model_comparison.csv
results/benchmark_results.csv
results/edge_cloud_comparison.csv
results/final_results_summary.csv
```

The classification results are compared across the four machine-learning models.

System-level measurements include prediction latency, process memory and payload size.

The exact numerical values reported in the final version of this section will be taken directly from the generated result files.

---

## 11. Limitations

The current implementation has the following limitations:

- The edge environment is simulated using a local computer.
- No physical sensor or dedicated edge device is used.
- The payload reduction experiment is a theoretical/local comparison.
- Process RSS is used as a system-level memory measurement.
- The study uses a limited subset of the available bearing conditions.

---

## 12. Future Work

Future work may include:

- Deployment on Raspberry Pi or another dedicated edge device.
- Real-time vibration sensor acquisition.
- Real network latency measurement.
- Adaptive sampling based on signal conditions.
- Additional fault severities.
- Additional motor loads and speeds.
- Cloud dashboard integration.
- Lightweight neural-network models.

---

## 13. Conclusion

This project develops a lightweight machine-learning pipeline for bearing fault diagnosis using motor vibration signals.

The workflow combines signal windowing, statistical feature extraction, machine-learning classification and a software-based edge-cloud data-flow experiment.

The study provides a reproducible framework for investigating the trade-off between vibration-data transmission and local feature processing.

The final conclusions are based on the experimentally generated classification and system-level measurements stored in the project results directory.