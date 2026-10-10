# Methodology

## 1. Research Design

This study proposes a comparative and controlled multi-source Earth-observation framework for evaluating the reliability of satellite-based environmental hazard monitoring.

The research focuses on three environmental monitoring problems:

1. Flood monitoring
2. Forest-disturbance monitoring
3. Wildfire monitoring

The methodology does not assume that combining multiple observations will automatically improve performance. Instead, the study will experimentally evaluate whether complementary satellite and environmental observations can reduce false positives and false negatives compared with single-source baselines.

Each hazard will first be investigated independently. The findings will then be analyzed across the three hazards to identify common and hazard-specific failure patterns.

---

## 2. Overall Research Workflow

The proposed research workflow consists of the following stages:

**Hazard Definition → Event Selection → Data Collection → Quality Control → Preprocessing → Single-Source Baseline → Failure Analysis → Incremental Information Addition → Comparative Evaluation → Robustness Testing → Cross-Hazard Analysis**

This workflow is designed to separate the contribution of individual information sources and avoid attributing improvements to multi-source integration without experimental evidence.

---

## 3. Historical Event and Study-Area Selection

Historical environmental events will be selected for each hazard based on the availability of suitable satellite observations and reference information.

For each selected event, the study will document:

- Geographic location
- Event date or monitoring period
- Hazard type
- Available satellite observations
- Environmental conditions
- Reference or ground-truth information
- Data quality and observation availability

Where possible, multiple events and geographic regions will be considered so that the evaluation is not dependent on a single environmental event.

---

## 4. Data Collection

The study will collect complementary Earth-observation and environmental information appropriate to each hazard.

### 4.1 Flood Monitoring

Potential data sources include:

- Sentinel-1 Synthetic Aperture Radar (SAR)
- Sentinel-2 optical imagery
- Satellite-derived rainfall information
- Digital Elevation Model (DEM) and terrain information
- Reference flood-extent information

### 4.2 Forest-Disturbance Monitoring

Potential data sources include:

- Sentinel-2 multispectral imagery
- Sentinel-1 SAR
- Landsat time-series observations
- Vegetation indices
- Temporal change information
- Reference disturbance information

### 4.3 Wildfire Monitoring

Potential data sources include:

- VIIRS active-fire observations
- MODIS active-fire observations
- Sentinel-2 optical imagery
- Thermal or active-fire information
- Environmental contextual information
- Reference fire or burned-area information

The final datasets will be selected after evaluating their spatial resolution, temporal availability, coverage, quality and suitability for the selected events.

---

## 5. Data Quality Control

Before analysis, the collected observations will undergo quality screening.

The quality-control stage will examine:

- Missing observations
- Cloud contamination
- Invalid pixels
- Sensor-specific quality flags
- Acquisition gaps
- Spatial mismatches
- Temporal mismatches
- Incomplete observations

Observations that do not satisfy the predefined quality requirements will either be excluded or explicitly flagged.

This step is important because missing or poor-quality observations can themselves contribute to monitoring failures.

---

## 6. Spatial and Temporal Preprocessing

Because the datasets originate from different sensors and environmental products, they will be spatially and temporally standardized before comparison.

The preprocessing stage may include:

- Coordinate-system standardization
- Spatial resampling where appropriate
- Common-area extraction
- Temporal alignment
- Cloud and invalid-pixel masking
- Normalization or scaling of numerical features
- Generation of relevant spectral, radar, temporal or environmental features

Differences in spatial and temporal resolution will be documented rather than assuming that observations from different sensors provide equivalent information.

---

## 7. Establishment of Single-Source Baselines

A single-source baseline will first be established for each hazard.

Example baseline configurations include:

- **Flood:** Sentinel-1-based flood mapping
- **Forest disturbance:** Sentinel-2 or Landsat-based disturbance detection
- **Wildfire:** VIIRS/MODIS active-fire detection

The baseline will establish the performance that can be achieved using the primary observation source before additional information is introduced.

This provides a reference against which multi-source configurations can be evaluated.

---

## 8. Baseline Failure Analysis

After establishing the baseline, the predictions will be compared with the available reference data to identify failure cases.

Two major error categories will be investigated:

### False Positive

The system identifies a hazard where the reference information indicates that the hazard is absent.

### False Negative

The system fails to identify a hazard where the reference information indicates that the hazard is present.

The study will examine the environmental and observational conditions associated with these errors.

Examples may include:

- Cloud-affected optical observations
- Ambiguous radar responses
- Non-fire thermal anomalies
- Missing satellite observations
- Complex terrain
- Urban surfaces
- Different vegetation conditions

The specific failure categories will be determined from the experimental data rather than assumed in advance.

---

## 9. Incremental Addition of Complementary Information

Additional satellite or environmental information will be introduced incrementally.

For example, a flood experiment may follow the sequence:

- **Experiment F1:** Sentinel-1
- **Experiment F2:** Sentinel-1 + rainfall
- **Experiment F3:** Sentinel-1 + terrain
- **Experiment F4:** Sentinel-1 + rainfall + terrain

Similar controlled configurations will be developed for forest disturbance and wildfire monitoring.

This design allows the contribution of individual information sources to be measured rather than evaluating only one final multi-source model.

---

## 10. Comparative Evaluation

Each configuration will be evaluated against the corresponding reference data.

Depending on the monitoring task, the evaluation will consider:

- Precision
- Recall
- F1-score
- Intersection over Union (IoU)
- False-positive rate
- False-negative rate
- Detection delay, where temporal detection is relevant

For spatial mapping tasks, predicted hazard areas will be compared with reference hazard areas to quantify spatial agreement.

Overall accuracy will not be treated as the only measure of performance because a single accuracy value may hide important false-positive and false-negative patterns.

---

## 11. Condition-Based Evaluation

The study will further evaluate performance under different observation and environmental conditions.

### Flood

Performance may be compared across:

- Different rainfall conditions
- Different terrain characteristics
- Urban and non-urban areas
- Different flood events

### Forest Disturbance

Performance may be compared across:

- Cloud-free and cloud-affected periods
- Different observation gaps
- Different disturbance types
- Different vegetation conditions

### Wildfire

Performance may be compared across:

- Different observation conditions
- Different thermal-anomaly contexts
- Different geographic environments
- Active-fire and post-fire monitoring situations

The purpose is to determine not only whether a method performs differently, but also under which conditions complementary information provides measurable benefit.

---

## 12. Geographic and Event-Level Validation

Where sufficient data are available, training and evaluation data will be separated by geographic region or environmental event.

For example:

**Training Events/Regions → Model Development**

**Independent Events/Regions → Evaluation**

This approach will help determine whether the observed performance is specific to the development data or remains applicable to previously unseen events or regions.

The evaluation will document the geographic and temporal separation between development and testing data.

---

## 13. Robustness to Missing Observations

Because satellite observations may be unavailable because of cloud cover, acquisition gaps or other conditions, the study will investigate the effect of missing information.

Controlled experiments may include:

- All selected sources available
- Optical source unavailable
- Environmental context unavailable
- One complementary source unavailable

The resulting performance will be compared with the complete-information configuration.

This experiment will help determine whether the proposed framework can maintain useful monitoring capability when one information source is unavailable.

---

## 14. Cross-Hazard Analysis

After completing the individual hazard experiments, the results will be analyzed across flood, forest disturbance and wildfire monitoring.

The analysis will investigate:

- Common failure patterns
- Hazard-specific failure patterns
- The contribution of complementary observations
- Conditions under which sensor fusion is useful
- Conditions under which additional information provides little or no measurable benefit
- The effect of missing observations
- Differences in reference-data quality and evaluation difficulty

The cross-hazard analysis will not assume that the same sensor combination or methodology will be optimal for all hazards.

---

## 15. Experimental Decision Framework

The results of each experiment will be interpreted using an evidence-based comparison:

**Single-source baseline**

↓

**Identify failure cases**

↓

**Add complementary information**

↓

**Re-evaluate**

↓

**Compare false positives and false negatives**

↓

**Analyze condition-specific performance**

↓

**Test geographic/event robustness**

↓

**Determine whether the additional information provides measurable improvement**

An additional information source will not be considered useful merely because it is theoretically complementary. Its usefulness must be supported by the experimental results.

---

## 16. Reproducibility and Research Documentation

All experiments will be documented in the project repository.

The repository will maintain records of:

- Data sources
- Dataset versions or acquisition periods
- Study areas and events
- Preprocessing procedures
- Feature configurations
- Baseline methods
- Experimental configurations
- Evaluation metrics
- Results
- Failure cases
- Limitations
- Code and configuration files

This documentation will allow the experimental procedure and conclusions to be independently understood and reproduced.

---

## 17. Final Research Evaluation

The final research question will be evaluated as an experimental hypothesis:

> **“Can combining complementary satellite and environmental observations reduce missed detections and false alarms compared with relying on individual observations for flood, forest-disturbance and wildfire monitoring?”**

The study will not assume that multi-source integration will improve all hazards or all conditions.

Instead, the final findings will report:

1. Where the single-source baseline fails.
2. Which complementary information was introduced.
3. Whether the additional information changed performance.
4. Whether false positives or false negatives changed.
5. Under which environmental or observational conditions the change occurred.
6. Whether the result remained consistent across independent events or regions.
7. What limitations remain after the experiments.

This approach allows the research contribution to be derived from experimental evidence rather than from the assumption that multi-sensor integration is inherently superior.
