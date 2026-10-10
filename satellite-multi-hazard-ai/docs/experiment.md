# Experimental Objectives

## Experiments

### 1. Experimental Objective

The experiments are designed to evaluate whether combining complementary satellite and environmental observations can improve environmental hazard monitoring compared with relying on a single data source.

The experiments will focus on three hazards:

1. Flood monitoring
2. Forest-disturbance monitoring
3. Wildfire monitoring

The evaluation will focus particularly on false positives, false negatives, detection performance, robustness to missing observations, and consistency across different environmental conditions.

---

### 2. Experiment 1 — Single-Source Baseline

The first experiment establishes a baseline using a single primary observation source for each hazard.

#### Flood

Sentinel-1 SAR will be used as the primary source for flood detection.

#### Forest Disturbance

Sentinel-2 optical imagery or Landsat time-series observations will be used as the primary source for detecting vegetation or land-cover changes.

#### Wildfire

VIIRS or MODIS active-fire observations will be used as the primary source for wildfire detection.

The baseline results will be recorded before introducing additional information.

#### Baseline Metrics

The following metrics will be considered:

- Precision
- Recall
- F1-score
- Intersection over Union (IoU)
- False-positive rate
- False-negative rate
- Detection delay, where applicable

---

### 3. Experiment 2 — Incremental Addition of Complementary Information

The second experiment evaluates whether additional observations improve the baseline results.

Instead of combining all available data at once, complementary information will be added incrementally.

#### Flood Experiment

The following configurations will be compared:

- **F1:** Sentinel-1 SAR
- **F2:** Sentinel-1 SAR + rainfall
- **F3:** Sentinel-1 SAR + terrain information
- **F4:** Sentinel-1 SAR + rainfall + terrain

The performance of each configuration will be compared with the previous configuration.

#### Forest-Disturbance Experiment

The following information will be evaluated:

- Optical imagery
- Optical imagery + SAR
- Optical imagery + temporal change information
- Optical imagery + SAR + temporal information

The objective is to determine whether SAR and temporal observations provide useful information when optical observations alone are insufficient.

#### Wildfire Experiment

The following configurations will be evaluated:

- Active-fire observations only
- Active-fire + optical imagery
- Active-fire + environmental context
- Active-fire + optical imagery + environmental context

The objective is to determine whether additional observations reduce missed detections or false alarms.

---

### 4. Experiment 3 — Failure-Case Analysis

The third experiment focuses on understanding where the single-source baseline fails.

Two major failure categories will be investigated:

#### False Positives

A false positive occurs when the monitoring system identifies a hazard where the reference data do not indicate the target event.

Examples include:

- Water-like surfaces incorrectly identified as flood areas
- Normal vegetation changes incorrectly identified as forest disturbance
- Thermal anomalies incorrectly interpreted as wildfire

#### False Negatives

A false negative occurs when an actual hazard event is present in the reference data but is not detected by the monitoring system.

Examples include:

- Flooded areas missed by the baseline
- Small or gradual forest disturbances not detected
- Fires missed because of observation limitations

For each failure case, the available complementary observations will be examined to determine whether they provide additional information that could explain or reduce the failure.

---

### 5. Experiment 4 — Missing-Data Robustness

This experiment evaluates how the monitoring workflow behaves when one of the expected information sources is unavailable.

The following scenarios will be considered:

- All planned data sources available
- Optical imagery unavailable
- Environmental information unavailable
- One complementary satellite source unavailable

The results will be compared to determine whether the workflow can continue to provide useful monitoring information under incomplete observation conditions.

This experiment is particularly relevant for situations involving cloud cover, observation gaps, delayed data availability, or other data-quality limitations.

---

### 6. Experiment 5 — Condition-Based Evaluation

The performance of the monitoring workflow will be evaluated under different environmental and observation conditions.

#### Flood

The analysis may consider:

- Different rainfall conditions
- Different terrain characteristics
- Urban and non-urban areas
- Different flood events

#### Forest Disturbance

The analysis may consider:

- Different vegetation conditions
- Different disturbance types
- Cloud-free and cloud-affected observations
- Different observation gaps

#### Wildfire

The analysis may consider:

- Different observation conditions
- Different thermal anomaly contexts
- Different geographic environments
- Active-fire and post-fire observations

The purpose is to determine whether the observed improvement remains consistent under different conditions.

---

### 7. Experiment 6 — Geographic and Event-Level Validation

The workflow will be evaluated using multiple historical events or geographic regions where suitable reference information is available.

Where possible, some events or regions will be used for workflow development, while independent events or regions will be used for evaluation.

This reduces the possibility that the results are specific to a single event or geographic location.

The following will be compared:

- Performance across different events
- Performance across different geographic regions
- False-positive patterns
- False-negative patterns
- Consistency of improvements from complementary information

---

### 8. Experiment 7 — Cross-Hazard Analysis

The final experiment compares the results obtained from flood, forest-disturbance, and wildfire monitoring.

The analysis will investigate:

- Common failure patterns
- Hazard-specific failure patterns
- Contribution of complementary observations
- Changes in false positives and false negatives
- Effects of missing observations
- Conditions where multi-source information provides measurable improvement
- Conditions where additional information provides little or no measurable benefit

The purpose is not to assume that the same data-fusion strategy will work equally well for every hazard.

---

### 9. Evaluation Metrics

The experiments will use quantitative evaluation metrics wherever suitable.

#### Precision

Measures the proportion of detected events or pixels that are actually relevant.

#### Recall

Measures the proportion of reference events or pixels that are successfully detected.

#### F1-Score

Provides a combined measure of precision and recall.

#### Intersection over Union (IoU)

Measures the spatial overlap between the detected hazard area and the reference hazard area.

#### False-Positive Rate

Measures the proportion of incorrect detections.

#### False-Negative Rate

Measures the proportion of actual hazard observations that were missed.

#### Detection Delay

Measures the time difference between the reference event occurrence and its detection, where suitable temporal information is available.

---

### 10. Experimental Comparison

The results will be organized so that each additional information source can be compared with the corresponding baseline.

| Experiment | Baseline | Additional Information | Main Evaluation |
|---|---|---|---|
| E1 | Single source | None | Baseline performance |
| E2 | Single source | Complementary observations | Performance improvement |
| E3 | Single source | Failure-case analysis | FP/FN reduction |
| E4 | Multi-source | Remove one source | Robustness |
| E5 | Multi-source | Different conditions | Condition-based performance |
| E6 | Multi-source | Different events/regions | Generalization |
| E7 | All hazards | Cross-hazard comparison | Common and hazard-specific patterns |

---

### 11. Experimental Decision Framework

The experimental analysis will follow the sequence:

**Single-Source Baseline → Identify Failure Cases → Add Complementary Information → Re-evaluate → Compare FP/FN → Condition-Based Analysis → Geographic/Event Validation → Missing-Data Testing → Cross-Hazard Analysis**

An additional data source will be considered useful only when the experimental results show a measurable improvement or provide useful information for reducing specific failure cases.

The study will therefore distinguish between:

- Information that improves detection
- Information that reduces false positives
- Information that reduces false negatives
- Information that improves robustness
- Information that provides little measurable improvement

---

### 12. Expected Experimental Output

The experiments will produce:

1. Baseline performance results for each hazard.
2. Comparative results after adding complementary information.
3. False-positive and false-negative examples.
4. Condition-specific performance observations.
5. Missing-data robustness results.
6. Event-level and geographic validation results.
7. Cross-hazard comparison findings.
8. A final assessment of where multi-source monitoring provides measurable benefits and where limitations remain.

The final results will be documented together with the datasets, preprocessing steps, experimental configurations, evaluation metrics, and limitations to support reproducibility.
