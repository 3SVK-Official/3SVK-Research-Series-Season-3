# WF02 — FIRMS Detection Reliability: Event-Level Evaluation

## 1. Experiment Overview

**Experiment ID:** WF02
**Track:** Wildfire Monitoring
**Experiment type:** Historical satellite-detection analysis
**Data source:** NASA Fire Information for Resource Management System (FIRMS)
**Notebook:** `notebooks/wildfire/WF02_firms_detection_reliability.ipynb`
**Status:** Preliminary event-level evaluation

### Objective

To investigate whether NASA FIRMS active-fire detections are spatially and temporally associated with independently documented historical fire events.

The experiment establishes a reproducible workflow for querying historical satellite observations, inspecting their attributes, and comparing detections with documented event locations and dates.

## 2. Research Questions

1. Does FIRMS return satellite observations around the documented fire events?
2. Do any returned detections fall within the predefined spatial and temporal matching criteria?
3. What information do detection attributes, including brightness, confidence, and fire radiative power (FRP), provide for further investigation?
4. What limitations must be addressed before measuring detection reliability?

## 3. Data Sources

### 3.1 FIRMS observations

Historical active-fire observations were requested through the NASA FIRMS API using available satellite products.

The notebook records returned observations, acquisition dates, coordinates, available detection attributes, and API request statuses.

### 3.2 Independent event references

Historical fire-event references are maintained in:

`data/event_references/historical_fire_events.csv`

The reference table contains event identifiers, event names, dates, approximate coordinates, source URLs, and verification status.

These references provide the basis for the event-level comparison. A reference point is not equivalent to a verified fire perimeter.

## 4. Methodology

### Step 1 — Event reference validation

The event-reference table was checked for required fields, valid dates, coordinate ranges, and source information.

### Step 2 — Historical data retrieval

FIRMS product availability was inspected before requesting observations. Requests were restricted to the event-specific date windows and geographic bounding boxes.

### Step 3 — Data quality assessment

Returned records were inspected for valid coordinates and acquisition dates. Request statuses were recorded to help distinguish empty responses from API failures.

### Step 4 — Spatial and temporal comparison

Candidate associations were identified using the following exploratory criteria:

| Parameter                    | Setting |
| ---------------------------- | ------- |
| Spatial matching radius      | 30 km   |
| Date buffer before the event | 2 days  |
| Date buffer after the event  | 2 days  |

A returned detection meeting both criteria was classified as a **candidate spatiotemporal match**, not a confirmed true positive.

### Step 5 — Attribute and visualization analysis

The notebook examined available detection attributes and generated event-level tables, daily detection summaries, and spatial visualizations.

## 5. Observations and Results

The numerical findings must be taken from the generated notebook outputs rather than estimated.

| Observation                                                | Source artifact                                  |
| ---------------------------------------------------------- | ------------------------------------------------ |
| Number of documented events examined                       | `WF02_event_coverage.csv`                        |
| Returned detection rows for each event                     | `WF02_event_coverage.csv`                        |
| Candidate spatiotemporal match rows                        | `WF02_event_spatiotemporal_matches.csv`          |
| Closest returned detection distance to the reference point | `WF02_event_spatiotemporal_matches.csv`          |
| Successful and failed API requests                         | `WF02_request_log.csv`                           |
| Available confidence values                                | `WF02_confidence_value_counts.csv`, if generated |
| Numeric detection-attribute summaries                      | `WF02_detection_attribute_summary.csv`           |
| Spatial distribution of detections                         | `WF02_spatial_matches_<event_id>.png`            |
| Final event-level evaluation                               | `WF02_event_evaluation.md`                       |

**Interpretation:** Candidate matches indicate spatial and temporal proximity to the documented event under the selected criteria. They do not independently establish that each detection belongs to the event.

An empty result also requires investigation: it may reflect product availability, query parameters, sensor coverage, acquisition timing, or a genuine absence of returned detections.

## 6. Research Findings

This experiment establishes a preliminary workflow for examining historical FIRMS observations around documented fire events.

The analysis distinguishes three important outcomes:

* **Returned detection:** A record returned by a FIRMS query.
* **Candidate match:** A returned detection meeting the specified spatial and temporal criteria.
* **Verified detection:** A detection independently confirmed against suitable reference evidence.

Only the first two categories are assessed by the current proximity-based workflow. Independent verification is required to establish the third.

Consequently, this experiment does not yet establish a validated FIRMS detection rate, precision, recall, or false-alarm rate.

## 7. Limitations

1. A small number of historical events cannot establish reliability across different regions, seasons, and environmental conditions.
2. Approximate event coordinates and circular buffers do not represent the actual fire perimeter.
3. A nearby satellite detection may correspond to another fire or thermal anomaly.
4. The absence of a returned record does not automatically indicate a missed fire.
5. Cloud and smoke conditions, satellite overpass timing, sensor resolution, and product availability can affect observations.
6. Brightness, confidence, and FRP are detection attributes, not independent ground-truth labels.
7. Quantitative evaluation requires suitable independent reference perimeters or verified detection-level labels.

## 8. Generated Artifacts

The experiment is designed to produce the following files:

* `results/WF02_query_windows.csv`
* `results/WF02_request_log.csv`
* `results/WF02_event_coverage.csv`
* `results/WF02_event_spatiotemporal_matches.csv`
* `results/WF02_detection_attribute_summary.csv`
* `results/WF02_event_evaluation.md`
* `results/WF02_conclusion.md`
* `results/WF02_final_verification.csv`
* Event-specific spatial-match figures
* `data/WF02_historical_firms_detections.csv`

Only files confirmed to exist in the completed notebook run should be included in the final repository.

## 9. Conclusion

WF02 provides a preliminary, reproducible method for retrieving and examining NASA FIRMS historical active-fire observations around independently documented fire events.

The spatial and temporal comparison helps identify candidate associations for further review. However, proximity alone cannot confirm detections, identify false alarms, or establish missed fires.

The experiment should therefore be treated as an initial event-level investigation rather than a completed statistical reliability assessment. Further evaluation requires independent reference evidence and a clearly defined event-level validation procedure.

## 10. Next Experiment

Proceed to **WF03 — NBR/dNBR Burned-Area Baseline**.

The next experiment will investigate pre-fire and post-fire spectral changes using satellite imagery. Burned-area mapping and active-fire detection will remain separate tasks because they measure different aspects of a fire event.
