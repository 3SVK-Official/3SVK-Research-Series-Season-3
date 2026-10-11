# WF01 — Wildfire Active-Fire Data Inspection

## 1. Experiment Overview

| Field            | Details                                                         |
| ---------------- | --------------------------------------------------------------- |
| Experiment ID    | WF01                                                            |
| Experiment name  | Wildfire Active-Fire Data Inspection                            |
| Track            | Wildfire Monitoring                                             |
| Notebook         | `notebooks/wildfire/WF01_data_inspection.ipynb`                 |
| Dataset          | NASA FIRMS MODIS Collection 6.1 Global 24-hour active-fire CSV  |
| Experiment type  | Data inspection and quality assessment                          |
| Execution status | Notebook cells executed; output verification should be reviewed |

## 2. Objective

The objective of WF01 is to inspect satellite-derived active-fire observations before developing a wildfire-monitoring baseline.

The experiment establishes an initial understanding of the dataset's structure, temporal attributes, geographic coordinates, fire-related measurements, data quality, and limitations.

This experiment does not train a machine-learning model or claim to predict future wildfires. It provides the initial data-quality foundation for subsequent wildfire experiments.

## 3. Research Questions

The experiment investigates the following questions:

1. What attributes and data types are available in the active-fire dataset?
2. Are the geographic coordinates valid, and how many records contain missing or invalid coordinates?
3. Are acquisition dates and times available and parseable?
4. How are observations distributed across confidence values and day/night categories, where those fields are available?
5. What values and distributions are present in the fire-related measurements?
6. How are detections distributed across broad geographic regions?
7. What limitations must be addressed before developing a baseline or evaluating a model?

## 4. Dataset and Source

The notebook uses the NASA Fire Information for Resource Management System (FIRMS) MODIS Collection 6.1 global 24-hour CSV.

**Dataset source URL:**

https://firms.modaps.eosdis.nasa.gov/data/active_fire/modis-c6.1/csv/MODIS_C6_1_Global_24h.csv

The downloaded file is saved as:

`MODIS_C6_1_Global_24h.csv`

The notebook records the retrieval timestamp in UTC so the dataset snapshot can be distinguished from later downloads.

### Important temporal limitation

This is a rolling 24-hour snapshot, not a fixed historical archive. Its records change as new satellite observations become available and older observations leave the time window.

For reproducibility, the downloaded CSV should be retained with its retrieval timestamp. Historical modelling will require a suitable historical dataset or archived observations.

## 5. Methodology

### 5.1 Environment setup

The notebook creates separate directories for downloaded data and experiment outputs:

* `/content/wildfire_monitoring/data`
* `/content/wildfire_monitoring/results`

It imports the Python libraries required for data processing, descriptive statistics, and visualization.

### 5.2 Dataset loading and structural inspection

The CSV is loaded into a Pandas DataFrame.

The notebook examines:

* Number of rows and columns.
* Available column names.
* First few observations.
* Data types.
* Missing values.
* Number of unique values per column.
* Exact duplicate rows.

These checks help identify schema problems and potential data-quality issues before further analysis.

### 5.3 Coordinate validation

Latitude and longitude are converted to numeric values where possible.

A coordinate record is treated as valid when:

* Latitude lies between −90 and 90 degrees.
* Longitude lies between −180 and 180 degrees.

Records with missing or invalid coordinates are counted separately. Valid coordinates are used for geographic visualization and regional summaries.

### 5.4 Acquisition timestamp inspection

The notebook examines the `acq_date` and `acq_time` fields and attempts to construct acquisition timestamps.

It reports the number of valid and invalid timestamps and, when valid timestamps exist, the earliest and latest recorded observation times.

Daily detection counts are generated from valid timestamps.

Acquisition times are not automatically interpreted as local time; the notebook's parsed timestamps represent the date and time fields provided by the dataset.

### 5.5 Confidence and day/night analysis

Where available, confidence values are summarized and visualized.

The `daynight` field is normalized for case and whitespace before category counts are generated.

If a required field is unavailable, its analysis is skipped rather than replaced with fabricated values.

Confidence values must be interpreted according to the documentation for the specific product. They should not be assumed to represent the same quantity across different satellite products.

### 5.6 Fire-related measurements

The notebook inspects available fields such as:

* `bright_ti4`
* `bright_ti5`
* `brightness`, if present
* `frp`
* `confidence`
* `scan`
* `track`

Only fields present in the downloaded CSV are analyzed.

Descriptive statistics are generated to summarize the distributions and identify missing or negative values for further investigation.

Brightness temperature and fire radiative power represent different measurements and should not be treated as interchangeable indicators of fire severity.

### 5.7 Geographic distribution

Records with valid coordinates are assigned to broad northern/southern and eastern/western geographic groups.

The notebook counts detections in each quadrant and calculates their percentage of valid-coordinate records.

A longitude–latitude scatter plot is generated to visualize the geographic distribution of sampled detections.

These geographic groups are exploratory bins, not administrative boundaries. Detection counts do not represent the number of unique fire events or the area burned.

## 6. Results

The notebook generates numerical summaries and figures from the downloaded snapshot.

**The exact numerical results should be taken from the saved notebook outputs.** They are not reproduced here because the output values have not yet been recorded in this report.

### 6.1 Dataset structure and quality

Source artifacts:

* `WF01_data_quality.csv`
* `WF01_inspected_data.csv`

Record the following values from the notebook:

| Metric                                      | Observed result                   |
| ------------------------------------------- | --------------------------------- |
| Total records                               | To be copied from notebook output |
| Number of columns                           | To be copied from notebook output |
| Exact duplicate rows                        | To be copied from notebook output |
| Records with valid coordinates              | To be copied from notebook output |
| Records with invalid or missing coordinates | To be copied from notebook output |
| Valid acquisition timestamps                | To be copied from notebook output |
| Invalid or missing timestamps               | To be copied from notebook output |

### 6.2 Temporal distribution

Source artifact: `WF01_daily_detection_counts.csv`

The daily counts summarize records by acquisition date when valid timestamps are available.

The observed date range and detection counts should be interpreted within the limits of the rolling 24-hour snapshot. They do not establish a seasonal trend or long-term wildfire pattern.

### 6.3 Confidence and day/night distributions

Source artifacts:

* `WF01_confidence_distribution.png`, when generated.
* `WF01_daynight_counts.csv`, when applicable.
* `WF01_daynight_distribution.png`, when applicable.

These outputs help describe the available detection attributes. They do not independently establish whether a detection is a confirmed wildfire.

### 6.4 Fire-related measurement summary

Source artifact: `WF01_numeric_attribute_summary.csv`

The summary provides descriptive statistics for the recognized numeric fields present in the dataset.

The results should be inspected for missing values, unusual ranges, and measurement-specific interpretation before any thresholds or modelling features are selected.

### 6.5 Geographic distribution

Source artifacts:

* `WF01_geographic_summary.csv`
* `WF01_geographic_summary.png`

The regional summary and scatter plot describe the locations of observations with valid coordinates in the downloaded snapshot.

The visualization is an exploratory longitude–latitude plot, not a projected geographic map or a map of fire perimeters.

## 7. Generated Artifacts

The notebook is designed to generate the following outputs:

| Artifact                                 | Purpose                                                      |
| ---------------------------------------- | ------------------------------------------------------------ |
| `WF01_data_quality.csv`                  | Missing-value, data-type, and uniqueness summary             |
| `WF01_inspected_data.csv`                | Inspected copy of the downloaded dataset                     |
| `WF01_daily_detection_counts.csv`        | Daily counts based on valid acquisition timestamps           |
| `WF01_daynight_counts.csv`               | Counts by day/night category, when available                 |
| `WF01_daynight_distribution.png`         | Day/night distribution visualization, when applicable        |
| `WF01_numeric_attribute_summary.csv`     | Descriptive statistics for available numeric fields          |
| `WF01_confidence_distribution.png`       | Confidence distribution, when usable confidence values exist |
| `WF01_geographic_summary.csv`            | Counts by broad geographic quadrant                          |
| `WF01_geographic_summary.png`            | Visualization of broad geographic counts                     |
| `WF01_global_detection_distribution.png` | Geographic scatter plot of detections                        |
| `WF01_summary.md`                        | Automatically generated summary of the inspection            |
| `WF01_output_verification.csv`           | Verification of expected output files                        |

Optional outputs depend on the fields and valid observations present in the downloaded snapshot.

The existence and non-zero size of expected files should be confirmed using `WF01_output_verification.csv` and the notebook's final completion check.

## 8. Limitations

1. **Thermal anomalies are not definitive wildfire confirmations.** Active-fire products identify satellite-observed thermal anomalies; additional evidence may be needed to determine their cause.
2. **Snapshot limitation.** The global 24-hour CSV is not sufficient by itself for historical training or long-term trend analysis.
3. **Detection counts are not unique-fire counts.** A fire may generate multiple detections, and a detection may not correspond to a confirmed wildfire.
4. **No burned-area measurement.** Point detections alone do not establish the affected area or fire perimeter.
5. **Observation constraints.** Satellite coverage, spatial resolution, observation timing, cloud conditions for relevant sensors, and other factors can influence detection.
6. **Confidence interpretation.** Confidence and other attributes must be interpreted according to the relevant product documentation.
7. **Geographic visualization.** Broad geographic bins and scatter plots are exploratory and do not replace spatial analysis using appropriate geographic boundaries.
8. **No independent ground-truth validation.** This experiment does not compare detections against independently verified wildfire events.
9. **No trained model.** WF01 reports no predictive accuracy, precision, recall, F1-score, or early-warning performance.

## 9. Reproducibility

To reproduce the experiment:

1. Open `notebooks/wildfire/WF01_data_inspection.ipynb`.
2. Run the cells in sequence.
3. Record the source URL and retrieval timestamp.
4. Inspect the dataset quality and coordinate checks.
5. Review the temporal, numeric, and geographic summaries.
6. Confirm which optional outputs were generated.
7. Verify the final output checklist.
8. Update this report with numerical findings taken directly from the notebook outputs.
9. Commit the notebook and report to the repository.

Because the dataset is a rolling snapshot, a later download may produce different counts and distributions.

## 10. Conclusion

WF01 establishes the initial data-inspection workflow for the project's wildfire-monitoring track. It examines the structure, quality, timing, geographic distribution, and available fire-related attributes of NASA FIRMS MODIS active-fire observations.

The experiment provides a foundation for selecting a suitable historical dataset and designing a baseline for subsequent research.

No claim is made that the inspected detections represent confirmed wildfires, that they predict future fires, or that a monitoring model has achieved a particular level of accuracy.

**Completion status:** Notebook cells executed. Final experiment completion should be confirmed by reviewing the actual output-verification table, generated artifacts, and saved summary.
