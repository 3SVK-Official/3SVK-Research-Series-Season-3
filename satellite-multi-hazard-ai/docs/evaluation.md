# Evaluation

## 1. Evaluation Objective

The evaluation is designed to determine whether combining complementary satellite and environmental observations improves environmental hazard monitoring compared with single-source approaches.

The evaluation will focus on:

- Detection accuracy
- False positives
- False negatives
- Spatial agreement with reference data
- Detection delay
- Robustness to missing observations
- Performance under different environmental conditions
- Consistency across different events and geographic regions

The evaluation will be performed separately for flood, forest-disturbance, and wildfire monitoring before conducting a cross-hazard analysis.

---

## 2. Reference Data

The experimental outputs will be compared against suitable reference or validation data for each hazard.

Reference information may include:

- Official or authoritative hazard datasets
- Historical event records
- Reference flood extents
- Burned-area or active-fire reference data
- Forest-disturbance reference information
- Manually validated samples where appropriate

The quality and limitations of the reference data will be documented because evaluation results depend on the reliability of the reference information.

---

## 3. Classification-Based Evaluation

For detection tasks, the results will be analyzed using four basic categories:

### True Positive (TP)

The system detects a hazard and the reference data confirm the hazard.

### True Negative (TN)

The system does not detect a hazard and the reference data also indicate no hazard.

### False Positive (FP)

The system detects a hazard but the reference data do not confirm it.

### False Negative (FN)

The reference data indicate a hazard, but the system fails to detect it.

These categories will be used to analyze the types of errors produced by different monitoring configurations.

---

## 4. Precision

Precision measures how many of the detected hazard observations are actually relevant.

\[
Precision = \frac{TP}{TP + FP}
\]

Higher precision indicates fewer false-positive detections.

---

## 5. Recall

Recall measures how many of the reference hazard observations are successfully detected.

\[
Recall = \frac{TP}{TP + FN}
\]

Higher recall indicates fewer missed hazard observations.

---

## 6. F1-Score

F1-score combines precision and recall into a single measure.

\[
F1 = 2 \times \frac{Precision \times Recall}{Precision + Recall}
\]

F1-score will be used to compare the overall detection performance of different experimental configurations.

---

## 7. Intersection over Union

For spatial hazard mapping, Intersection over Union (IoU) will be used to measure the overlap between the detected hazard area and the reference hazard area.

\[
IoU = \frac{Intersection}{Union}
\]

Higher IoU indicates greater spatial agreement between the detected and reference hazard areas.

IoU will be particularly useful for flood and burned-area mapping where spatial extent is important.

---

## 8. False-Positive Rate

The false-positive rate will be calculated as:

\[
FPR = \frac{FP}{FP + TN}
\]

This metric will help determine whether adding complementary information reduces incorrect hazard detections.

---

## 9. False-Negative Rate

The false-negative rate will be calculated as:

\[
FNR = \frac{FN}{FN + TP}
\]

This metric will help determine whether complementary information reduces missed hazard observations.

---

## 10. Detection Delay

For hazards where temporal information is available, detection delay will be evaluated.

\[
Detection\ Delay = Detection\ Time - Reference\ Event\ Time
\]

Lower detection delay indicates that the event was identified closer to the reference event time.

Detection delay will be considered particularly relevant for wildfire and rapidly developing flood events.

---

## 11. Baseline vs Multi-Source Comparison

The primary comparison will be between the single-source baseline and the corresponding multi-source configuration.

For each hazard, the following will be compared:

| Metric | Single-Source Baseline | Multi-Source Configuration | Change |
|---|---|---|---|
| Precision | — | — | — |
| Recall | — | — | — |
| F1-score | — | — | — |
| IoU | — | — | — |
| False-positive rate | — | — | — |
| False-negative rate | — | — | — |
| Detection delay | — | — | — |

The change in each metric will be documented rather than assuming that the multi-source configuration will always perform better.

---

## 12. Condition-Based Evaluation

Performance will also be evaluated under different environmental and observation conditions.

### Flood

Evaluation conditions may include:

- Different rainfall levels
- Different terrain characteristics
- Urban and non-urban areas
- Different flood events

### Forest Disturbance

Evaluation conditions may include:

- Different vegetation conditions
- Different disturbance types
- Cloud-affected observations
- Different temporal observation gaps

### Wildfire

Evaluation conditions may include:

- Different geographic environments
- Different thermal anomaly conditions
- Active-fire observations
- Post-fire observations
- Different observation conditions

This analysis will identify situations where complementary information is particularly useful or where limitations remain.

---

## 13. Robustness Evaluation

The workflow will be tested under incomplete data conditions.

Examples include:

- Optical imagery unavailable
- One satellite source unavailable
- Environmental contextual information unavailable
- Reduced temporal observations

Performance under these conditions will be compared with the full-data configuration.

The purpose is to determine whether the monitoring workflow remains useful when some observations are missing.

---

## 14. Geographic and Event-Level Evaluation

The evaluation will not depend on a single event or geographic location where sufficient data are available.

Results will be compared across:

- Different historical events
- Different geographic regions
- Different environmental conditions

The consistency of performance changes will be documented.

This helps determine whether observed improvements are specific to one event or remain observable across multiple cases.

---

## 15. Error Analysis

Quantitative metrics will be supplemented with qualitative analysis of representative errors.

### False-Positive Analysis

Examples of false positives will be examined to identify possible causes such as:

- Similar spectral or radar characteristics
- Temporary environmental changes
- Thermal anomalies unrelated to wildfire
- Water-like or vegetation-like surfaces
- Data-quality issues

### False-Negative Analysis

Examples of false negatives will be examined to identify possible causes such as:

- Cloud cover
- Observation gaps
- Small-scale events
- Weak signal characteristics
- Temporal mismatch
- Insufficient complementary information

---

## 16. Statistical Comparison

Where the number of independent samples or events is sufficient, the results from different configurations will be compared across repeated observations or events.

The analysis will focus on whether observed differences are consistent across cases rather than relying on a single example.

If the available sample size is limited, the study will explicitly report this limitation and treat the results as exploratory rather than making broad generalizations.

---

## 17. Cross-Hazard Evaluation

After evaluating each hazard independently, the results will be compared across flood, forest disturbance, and wildfire monitoring.

The comparison will examine:

- Which failure types are common across hazards
- Which complementary observations are useful for each hazard
- Whether multi-source information reduces false positives
- Whether multi-source information reduces false negatives
- Whether improvements remain consistent across events
- How missing observations affect each hazard

The objective is to identify both common principles and hazard-specific limitations.

---

## 18. Evaluation Decision Criteria

The evaluation will classify experimental observations based on the evidence obtained:

### Measurable Improvement

The additional information produces an observable improvement in one or more evaluation metrics or reduces a documented failure type.

### Limited Improvement

The additional information produces only a small or inconsistent change across evaluated cases.

### No Measurable Improvement

The additional information does not produce a meaningful change in the evaluated results.

### Remaining Limitation

The additional information does not resolve a particular failure case, or the limitation is caused by factors outside the available observations.

These categories describe experimental findings and are not predetermined outcomes.

---

## 19. Final Evaluation Output

The final evaluation will provide:

1. Single-source baseline results.
2. Multi-source experimental results.
3. Metric-level comparisons.
4. False-positive and false-negative analysis.
5. Condition-based results.
6. Missing-data robustness results.
7. Geographic and event-level validation.
8. Cross-hazard observations.
9. Remaining limitations.
10. Reproducibility information.

The final conclusion will be based on the experimental evidence rather than assuming that multi-source monitoring is superior in every situation.
