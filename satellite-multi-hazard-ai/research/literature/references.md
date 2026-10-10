# Research References

This file contains the primary scientific papers, official satellite
documentation and authoritative data-system documentation consulted
during the development of the Satellite-Based Multi-Hazard Intelligence
System.

The references are organized by research topic.

---

# 1. Earth Observation and Satellite Missions

## 1.1 Sentinel-1

European Space Agency (ESA).

"Sentinel-1."

Copernicus Sentinel-1 is a radar Earth-observation mission. The mission
provides all-weather, day-and-night radar imagery of Earth's surface.

Official source:

https://www.esa.int/Applications/Observing_the_Earth/Copernicus/Sentinel-1

Additional ESA mission information:

https://www.esa.int/Applications/Observing_the_Earth/Copernicus/Sentinel-1/Introducing_Sentinel-1_mission

Relevance to this project:

- Synthetic Aperture Radar (SAR)
- Flood monitoring
- Forest monitoring
- Disaster response
- Observation under many weather and illumination conditions

---

## 1.2 Sentinel-2

European Space Agency (ESA).

"Sentinel-2."

The Sentinel-2 mission provides multispectral optical observations
using 13 spectral bands.

The Sentinel-2 instrument provides observations at 10 m, 20 m and
60 m spatial resolutions depending on the spectral band.

Official source:

https://www.esa.int/Applications/Observing_the_Earth/Copernicus/Sentinel-2

ESA facts and figures:

https://www.esa.int/Applications/Observing_the_Earth/Copernicus/Sentinel-2/Facts_and_figures

Relevance to this project:

- Vegetation monitoring
- Forest disturbance
- Land-cover change
- Water monitoring
- Burned-area assessment
- Complementary information to SAR

---

# 2. Flood Monitoring

## 2.1 Copernicus Global Flood Monitoring

Copernicus Emergency Management Service (CEMS).

"Global Flood Monitoring."

The Copernicus Global Flood Monitoring component provides
near-real-time flood monitoring using incoming Sentinel-1 SAR
observations.

The system applies automated flood-mapping approaches and combines
multiple flood-mapping algorithm outputs.

Official documentation:

https://emergency.copernicus.eu/

Copernicus Data Space documentation:

https://dataspace.copernicus.eu/

Relevance to this project:

- Operational flood-monitoring baseline
- Sentinel-1 SAR
- Automated flood mapping
- Near-real-time monitoring
- Reference for investigating flood-detection limitations

---

## 2.2 Flood Remote Sensing and Machine Learning Review

A 2026 systematic review examined artificial intelligence and
multi-sensor Earth observation for flood forecasting and mapping.

The review considered combinations of Earth-observation and
environmental information and discussed challenges involving
datasets, spatial scales, flood types and validation.

This source is relevant to the project's investigation of whether
complementary observations can provide useful contextual information.

Source:

https://www.sciencedirect.com/

Note:

The exact paper record and DOI will be added after the team verifies
the final bibliographic metadata before using it as an experimental
reference.

---

# 3. Forest Disturbance

## 3.1 Near Real-Time Forest Disturbance Using Multi-Sensor Fusion

Tang, X., Bratley, K. H., Cho, K., Bullock, E. L., Olofsson, P.,
& Woodcock, C. E. (2023).

"Near real-time monitoring of tropical forest disturbance by fusion
of Landsat, Sentinel-2, and Sentinel-1 data."

Remote Sensing of Environment, 294, 113626.

DOI:

10.1016/j.rse.2023.113626

Source:

https://www.sciencedirect.com/science/article/pii/S0034425723001773

Key relevance:

The study developed a Fusion Near Real-Time (FNRT) approach combining
Landsat, Sentinel-2 and Sentinel-1 observations.

The study reported that the three-source fusion approach achieved
higher detection rates and shorter detection lag than individual
data sources in the selected Amazon study sites.

Reported results included approximately:

- 69.8% of disturbances detected within 30 days.
- 84.6% detected within 60 days.
- Peak producer's accuracy of approximately 91.6% at around a
  100-day lag in the reported experiment.

The study also reported that Sentinel-1 was particularly useful in
situations such as wet seasons or persistently cloudy regions.

Important research implication:

Optical-radar fusion is already an established research direction.
Therefore, this project must not claim that simply combining
Sentinel-1 and Sentinel-2 is novel.

---

## 3.2 Forest Disturbance Mapping Review

Rodríguez Paulino, E., Schlerf, M., Röder, A., Stoffels, J.,
& Udelhoven, T. (2024).

"Forest disturbance characterization in the era of earth observation
big data: A mapping review."

International Journal of Applied Earth Observation and
Geoinformation, 128, 103755.

DOI:

10.1016/j.jag.2024.103755

Source:

https://www.sciencedirect.com/science/article/pii/S1569843224001092

Key findings:

The review examined 104 publications on forest disturbance
characterization.

The study found that:

- Spectral-temporal information was widely used.
- SWIR-derived disturbance information was frequently used.
- Random Forest was among the most frequently used classification
  algorithms.
- Results depended substantially on change-detection methods,
  predictors and classifiers.
- Fewer than 10% of reviewed studies made their datasets accessible.

Research implication:

Reproducibility and transparent documentation are important
considerations for our project.

---

# 4. Wildfire Monitoring

## 4.1 NASA Fire Information for Resource Management System

NASA.

"Fire Information for Resource Management System (FIRMS)."

FIRMS provides satellite-derived active-fire and thermal-anomaly
information.

The system provides products derived from sensors including MODIS
and VIIRS.

Official source:

https://firms.modaps.eosdis.nasa.gov/

Relevance:

- Active-fire detection
- Thermal-anomaly monitoring
- Large-area fire monitoring
- Wildfire research baseline

---

## 4.2 Wildfire Satellite Remote Sensing Review

Chuvieco, E., Aguado, I., Salas, J., García, M., Yebra, M.,
& Oliva, P. (2020).

"Satellite Remote Sensing Contributions to Wildland Fire Science
and Management."

Current Forestry Reports, 6, 81–96.

DOI:

10.1007/s40725-020-00116-5

Source:

https://doi.org/10.1007/s40725-020-00116-5

Repository record:

https://openresearch-repository.anu.edu.au/items/5612aaae-20b7-4a90-ad6c-13ed2d0eedd5

The review considers satellite remote sensing for:

- Pre-fire assessment
- Active-fire detection
- Post-fire effects
- Fire prevention
- Fire detection
- Post-fire assessment

The review also discusses increasing use of multiple sensors,
including optical and radar observations.

The authors identify sensor integration, uncertainty
characterization and statistical validation as important challenges.

Research implication:

Our wildfire track should distinguish:

1. Fire-risk assessment
2. Active-fire detection
3. Post-fire burned-area assessment

These should not automatically be treated as the same prediction
problem.

---

# 5. Official Data and Supporting Sources

## 5.1 NASA Earth Observation Data

NASA Earthdata provides access to Earth-observation datasets and
information relevant to environmental monitoring.

Official source:

https://www.earthdata.nasa.gov/

Potential relevance:

- Satellite imagery
- Fire products
- Precipitation
- Environmental datasets

---

## 5.2 NASA GPM IMERG

NASA Global Precipitation Measurement (GPM) mission provides
precipitation observations and derived products.

IMERG combines precipitation observations from multiple sources to
produce precipitation estimates.

Official source:

https://gpm.nasa.gov/data-access/downloads/gpm

Relevance:

Rainfall can be investigated as contextual information for flood
analysis.

The project will not assume that rainfall automatically improves
flood detection. This must be tested experimentally.

---

# 6. Forest Monitoring Data

## 6.1 Global Forest Watch

Global Forest Watch provides information and monitoring tools for
forests and forest disturbances.

Official source:

https://www.globalforestwatch.org/

Relevant information includes forest-change and disturbance
monitoring products.

Research implication:

Global Forest Watch demonstrates that operational forest monitoring
already uses multiple data sources.

Therefore, the project must identify a specific measurable limitation
rather than claiming that multi-source forest monitoring is itself
new.

---

# 7. Research Methodology References

## 7.1 Reproducibility

The project will document:

- Data sources
- Data acquisition periods
- Preprocessing
- Experimental configurations
- Training and testing data
- Evaluation metrics
- Results
- Limitations

This documentation is especially important because the forest
disturbance mapping review identified limited accessibility of
datasets in much of the reviewed literature.

---

# 8. Reference Classification

The sources in this repository are classified into four groups.

## Group A — Official Satellite Documentation

Examples:

- ESA Sentinel-1
- ESA Sentinel-2
- NASA Earthdata
- NASA FIRMS
- NASA GPM

Purpose:

To establish authoritative information about satellite missions,
sensors and datasets.

---

## Group B — Operational Monitoring Systems

Examples:

- Copernicus Global Flood Monitoring
- Global Forest Watch
- NASA FIRMS

Purpose:

To understand what current operational systems already provide.

---

## Group C — Peer-Reviewed Research

Examples:

- Tang et al. (2023)
- Rodríguez Paulino et al. (2024)
- Chuvieco et al. (2020)

Purpose:

To understand methods, experiments, findings and limitations reported
by previous researchers.

---

## Group D — Supporting Datasets

Examples:

- GPM IMERG
- Digital Elevation Models
- Landsat
- Sentinel-1
- Sentinel-2
- VIIRS
- MODIS

Purpose:

To identify potential datasets for future experiments.

---

# 9. Important Research Integrity Rule

A source listed in this file does not automatically support every
claim made in the project.

Before using a source to support a specific statement, the team should
verify that the source actually contains evidence for that statement.

The project will distinguish between:

- What a source directly reports.
- Our interpretation of the source.
- Our experimental results.
- Hypotheses that have not yet been tested.

No performance improvement, superiority claim or research novelty
claim will be made without appropriate evidence.

---

# 10. Reference Expansion Plan

This bibliography is an initial reference set.

The team will expand it during the research phase with:

- Additional peer-reviewed papers.
- Benchmark datasets.
- Flood-mapping studies.
- Forest-disturbance studies.
- Wildfire detection studies.
- Multi-sensor fusion studies.
- Machine-learning methodology papers.
- Validation and uncertainty studies.

Each newly added source should include:

1. Full title.
2. Authors.
3. Publication year.
4. Journal or conference.
5. DOI or permanent identifier when available.
6. Source URL.
7. Short explanation of relevance to the project.
8. Important findings or limitations.

---

# 11. Current Status

Status: Initial reference collection.

The bibliography will continue to evolve as the project progresses
from literature review to dataset selection, baseline reproduction,
experimentation and evaluation.