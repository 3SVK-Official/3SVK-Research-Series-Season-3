# Literature Review

## 1. Purpose of the Literature Review

This literature review examines scientific research and authoritative
Earth-observation documentation relevant to satellite-based monitoring
of floods, forest disturbances and wildfires.

The purpose of this review is to understand:

- What satellite observations are currently available.
- What characteristics different satellite sensors provide.
- How satellite observations have been used for environmental hazard
  monitoring.
- How machine-learning and deep-learning methods have been applied.
- How multiple satellite and environmental observations have been
  combined.
- What limitations and failure conditions have been reported.
- What evaluation approaches have been used.
- What research questions may be suitable for experimental
  investigation.

The literature review is intended to guide the selection of datasets,
baseline methods, experiments and evaluation metrics for this project.

The review does not assume that the proposed project is novel.
Potential research gaps will be identified only after examining
existing research and conducting appropriate experiments.

---

# 2. Review Scope

The review focuses on three environmental monitoring problems:

1. Flood monitoring
2. Forest disturbance monitoring
3. Wildfire monitoring

The review considers several types of Earth-observation information,
including:

- Synthetic Aperture Radar (SAR)
- Multispectral optical imagery
- Thermal observations
- Rainfall observations
- Terrain information
- Time-series observations
- Environmental contextual information

Particular attention is given to Sentinel-1, Sentinel-2, Landsat,
VIIRS, MODIS and supporting environmental datasets.

The project is concerned with the reliability of satellite-based
monitoring rather than assuming that a satellite observation is a
perfect representation of ground conditions.

---

# 3. Earth Observation Data Relevant to the Research

## 3.1 Sentinel-1 Synthetic Aperture Radar

Sentinel-1 is a Copernicus radar Earth-observation mission carrying
Synthetic Aperture Radar (SAR).

The Sentinel-1 mission provides all-weather, day-and-night observations
of Earth's surface. This characteristic makes SAR particularly useful
for applications where optical imagery can be affected by cloud cover
or insufficient illumination.

Sentinel-1 uses C-band SAR observations and has been used for
applications including disaster monitoring, water mapping, forest
monitoring and other environmental applications.

For this project, Sentinel-1 is particularly relevant to:

- Flood inundation mapping
- Forest disturbance monitoring
- Observation during cloudy conditions
- Complementary information for optical observations

An important research consideration is that SAR does not simply provide
a clearer version of an optical image. Radar interacts with the
physical structure and surface properties of the observed area.
Therefore, SAR observations can contain information that is different
from multispectral optical observations.

### Relevance to the project

Sentinel-1 provides one of the main complementary observation sources
for the proposed research.

The project will investigate whether information from SAR can help
address specific situations in which other observations are
insufficient or ambiguous.

### Source

European Space Agency (ESA), Sentinel-1 mission documentation.

---

## 3.2 Sentinel-2 Multispectral Optical Observation

Sentinel-2 is a Copernicus multispectral Earth-observation mission.

The mission carries a multispectral imager with 13 spectral bands.
The bands cover visible, near-infrared and shortwave-infrared portions
of the electromagnetic spectrum.

Sentinel-2 provides spatial resolutions of 10 m, 20 m and 60 m
depending on the spectral band and is designed for frequent monitoring
of land and vegetation.

The data are relevant to applications including:

- Vegetation monitoring
- Forest monitoring
- Land-cover mapping
- Land-use change
- Water monitoring
- Disaster mapping

### Relevance to the project

Sentinel-2 provides detailed spectral information that can complement
radar observations.

For this project, Sentinel-2 is particularly relevant to:

- Forest disturbance detection
- Vegetation change analysis
- Burned-area assessment
- Water and land-cover analysis
- Cross-checking satellite detections

However, optical observations can be affected by cloud cover and other
atmospheric conditions.

Therefore, Sentinel-2 should not automatically be treated as a
complete replacement for SAR.

### Source

European Space Agency (ESA), Sentinel-2 mission documentation.

---

# 4. Flood Monitoring Research

## 4.1 Satellite-Based Flood Detection

Flood monitoring using Earth-observation data generally involves
identifying areas that have become inundated or estimating the
likelihood or extent of flooding.

SAR observations are particularly relevant because radar can provide
observations independent of daylight and can operate under many
weather conditions.

Sentinel-1 SAR has therefore become an important data source for
flood mapping.

Operational systems such as Copernicus Global Flood Monitoring use
Sentinel-1 observations for near-real-time flood monitoring.

The existence of such operational systems demonstrates that
satellite-based flood mapping is already an established field.

Therefore, a research contribution cannot simply be based on the idea
of using Sentinel-1 to detect floods.

---

## 4.2 Machine Learning and Flood Mapping

Recent research has investigated machine-learning and deep-learning
methods for flood forecasting, flood susceptibility assessment and
flood-extent mapping.

A 2026 systematic review examined studies combining artificial
intelligence with multi-sensor Earth-observation data for flood
forecasting and mapping.

The reviewed studies included combinations of:

- SAR
- Optical imagery
- Satellite precipitation
- Altimetry
- Terrain information

The review found that multi-sensor integration can be particularly
useful when different observations represent complementary aspects of
the flood process, such as:

- Hydrometeorological forcing
- Surface-water conditions
- Terrain controls

However, the review also found that differences in datasets, flood
types, spatial scales, reference labels and validation approaches make
universal comparisons between models difficult.

### Relevance to the project

This finding is important for our research design.

We should not compare models only by reporting one accuracy value.

The experiments should document:

- Dataset
- Geographic area
- Event type
- Observation conditions
- Reference labels
- Evaluation metrics
- Validation procedure
- Failure cases

This will help make the experimental results reproducible and
interpretable.

---

## 4.3 Flood Research Challenges

The literature indicates several challenges that require further
investigation:

- Differences between flood types.
- Variation in land cover.
- Urban and complex terrain conditions.
- Cloud limitations for optical imagery.
- Differences in spatial and temporal resolution.
- Quality of reference flood maps.
- Differences between training and test geographic regions.
- Uncertainty in model predictions.
- Difficulty transferring models between different environments.

These challenges suggest that a model that performs well for one event
or geographic region may not necessarily perform equally well in
another setting.

---

## 4.4 Implication for Our Flood Track

The flood component of this project should therefore investigate a
specific measurable question rather than simply building another
flood classifier.

Potential research directions include:

- Evaluating a Sentinel-1 baseline against a multi-source approach.
- Investigating whether rainfall information provides useful
  contextual information.
- Investigating whether terrain information helps reduce ambiguous
  detections.
- Studying false positives and false negatives under different
  environmental conditions.
- Testing geographic or event-level transfer.

These are research directions rather than confirmed contributions.

---

# 5. Forest Disturbance Research

## 5.1 Forest Monitoring Using Optical Observations

Optical satellite observations have been widely used for vegetation and
forest monitoring.

Sentinel-2 provides multispectral observations at relatively high
spatial resolution and includes spectral regions useful for vegetation
analysis.

Landsat provides a long historical record that is widely used for
land-cover and forest-change analysis.

Time-series analysis can identify changes in vegetation spectral
characteristics over time.

However, optical monitoring depends on usable observations and can be
affected by cloud cover.

---

## 5.2 Radar-Based Forest Disturbance Monitoring

SAR provides information based on radar interaction with the observed
surface rather than passive optical reflectance.

Sentinel-1 radar observations can therefore provide complementary
information for forest monitoring, particularly when optical
observations are unavailable because of cloud conditions.

Radar and optical observations do not respond identically to forest
changes.

This difference creates an opportunity for complementary monitoring,
but it also means that combining sensors requires careful
interpretation and validation.

---

## 5.3 Multi-Sensor Forest Disturbance Research

Previous research has already investigated the fusion of optical and
SAR observations for forest disturbance monitoring.

Tang et al. (2023) developed a near-real-time forest disturbance
monitoring approach using Landsat, Sentinel-2 and Sentinel-1 data.

Their study demonstrated that combining the three data sources could
improve disturbance detection compared with individual data sources.
The study also found that the value of Sentinel-1 was particularly
relevant in situations where optical observations were limited.

The study reported detection of approximately 70% of disturbances
within 30 days and approximately 85% within 60 days in its selected
Amazon study sites, with performance depending on the monitoring
conditions and evaluation setup.

Importantly, the study did not demonstrate that one sensor is always
superior.

Instead, the results showed that the complementary timing and
observation characteristics of different sensors can be useful.

### Relevance to our project

This research directly affects our research-gap definition.

We cannot claim:

> "No one has combined optical and radar data for forest
> disturbance detection."

Previous research has already demonstrated such approaches.

Instead, our investigation must identify a more specific question,
such as:

- Which disturbance conditions benefit most from additional radar
  observations?
- Which types of false alerts remain difficult?
- How does performance change under persistent cloud conditions?
- Can multiple alert sources improve reliability under particular
  conditions?
- Can natural and human-caused disturbances be separated reliably?

These questions require further literature investigation and
experimentation before any final contribution is claimed.

---

## 5.4 Forest Disturbance Mapping Review

A 2024 mapping review examined 104 publications related to forest
disturbance characterization.

The review found substantial variation in:

- Change-detection methods
- Predictor selection
- Classification algorithms
- Data-fusion methods
- Reference data availability

The review also reported that fewer than 10% of the studies included
accessible datasets for their analyses.

This is important from a research-reproducibility perspective.

### Relevance to our project

Our repository should therefore document:

- Data sources
- Data versions or acquisition periods
- Processing methods
- Training and testing regions
- Labels
- Evaluation procedures
- Code
- Experimental configurations

This can make our experiments easier for other researchers to
understand and reproduce.

---

# 6. Wildfire Research

## 6.1 Different Stages of Wildfire Monitoring

Wildfire monitoring is not a single prediction problem.

Satellite remote-sensing research commonly considers different stages
of fire management:

1. Pre-fire assessment
2. Active-fire detection
3. Post-fire assessment

These stages use different observations and have different objectives.

### Pre-fire assessment

The objective is generally to estimate fire danger, susceptibility
or risk using environmental and meteorological conditions.

### Active-fire detection

The objective is to identify thermal anomalies or active burning.

### Post-fire assessment

The objective is to estimate burned area, vegetation damage or other
effects after a fire.

### Relevance to our project

Our wildfire component should therefore avoid using the term
"wildfire prediction" without specifying which stage is being studied.

The project will distinguish between:

- Fire-risk assessment
- Active-fire detection
- Post-fire burned-area assessment

---

# 7. MODIS and VIIRS Active-Fire Monitoring

## 7.1 NASA FIRMS

NASA's Fire Information for Resource Management System (FIRMS)
provides satellite-derived active-fire and thermal-anomaly information.

FIRMS includes products derived from satellite sensors including:

- MODIS
- VIIRS
- Landsat-based products

VIIRS active-fire observations are available at approximately
375 m spatial resolution, while MODIS active-fire observations are
approximately 1 km.

These observations are useful for identifying potential active-fire
locations over large geographic areas.

---

## 7.2 Important Limitations of Active-Fire Detection

NASA explicitly states that satellite-derived active-fire and
thermal-anomaly detections have limited accuracy.

A detected thermal anomaly may be associated with:

- Fire
- Hot smoke
- Agricultural activity
- Other hot sources

Cloud cover can also obscure active-fire detections.

In addition, the spatial footprint of a satellite detection does not
mean that the entire pixel is burning.

Therefore, an active-fire detection should be interpreted as
satellite-derived evidence rather than automatically treating it as a
complete ground-truth representation of a fire.

### Relevance to our project

This provides a concrete research opportunity.

Instead of simply producing another hotspot map, the wildfire track can
investigate:

- False thermal anomalies.
- Missed detections.
- Cloud-related omissions.
- Detection confidence.
- Spatial-resolution effects.
- Whether additional optical or environmental information improves
  interpretation.

Any improvement must be demonstrated experimentally.

---

# 8. Multi-Sensor Research in Wildfire Monitoring

A review of satellite remote sensing contributions to wildland fire
science and management examined research covering:

- Pre-fire assessment
- Active-fire detection
- Post-fire effects

The review reported growing use of combinations of different sensors,
including optical and radar observations.

This supports the broader principle that different sensors can provide
complementary information across different stages of fire monitoring.

However, multi-sensor use by itself is not a sufficient research
contribution.

The important question is:

> Under which conditions does additional information actually improve
> detection or assessment?

This question can be evaluated using controlled experiments.

---

# 9. Cross-Hazard Findings

The literature reviewed so far shows several common themes across the
three hazards.

## 9.1 No Single Sensor Observes Everything

Different sensors measure different physical properties.

For example:

- SAR provides radar-based surface information.
- Optical sensors provide spectral information.
- Thermal sensors provide information related to heat anomalies.
- Rainfall datasets provide hydrometeorological context.
- Terrain datasets provide elevation and topographic context.

Therefore, different observations can contain complementary
information.

---

## 9.2 Sensor Fusion Is Already an Established Research Area

Existing research has already demonstrated multi-sensor approaches.

Examples include:

- SAR and optical observations for forest disturbance.
- SAR, optical, precipitation and terrain information for flood
  analysis.
- Multiple satellite observations for wildfire monitoring.

Therefore, the project will not claim that "combining satellite
sensors" is itself novel.

The research must instead identify a specific measurable limitation,
failure condition or evaluation problem.

---

## 9.3 Performance Depends on Conditions

Research results can depend on:

- Geographic region
- Weather
- Cloud cover
- Land cover
- Terrain
- Event type
- Sensor availability
- Spatial resolution
- Temporal resolution
- Quality of reference labels
- Validation methodology

Consequently, a model's performance on one dataset should not
automatically be interpreted as universal performance.

---

## 9.4 False Positives and False Negatives Matter

A single overall accuracy value may hide important failure cases.

For environmental monitoring, both types of errors can be important:

### False positive

The system reports a hazard where the reference data indicate that
the hazard is absent.

### False negative

The system fails to detect a hazard that is present in the reference
data.

The experiments in this project will therefore examine both types of
error wherever suitable reference data are available.

---

## 9.5 Reproducibility Is an Important Research Requirement

The reviewed forest-disturbance literature shows that accessibility
of datasets and experimental information can be limited.

Therefore, this project will attempt to maintain a transparent record
of:

- Data sources
- Processing steps
- Experimental configurations
- Code
- Evaluation metrics
- Results
- Limitations

The GitHub repository will serve as the central research record.

---

# 10. Findings Relevant to Our Research Question

The initial research question of this project is:

> Can combining complementary satellite and environmental observations
> reduce missed detections and false alarms compared with relying on
> individual observations for flood, forest-disturbance and wildfire
> monitoring?

The literature provides support for investigating this question, but
does not prove that a common multi-hazard approach will improve
performance across all three hazards.

Previous research suggests that complementary observations can provide
additional information, but the usefulness of the additional
information depends on:

- Hazard type
- Observation conditions
- Geographic environment
- Temporal availability
- Sensor characteristics
- Reference-data quality
- Evaluation methodology

Therefore, the hypothesis remains an experimental hypothesis.

---

# 11. Research Questions Emerging from the Literature

Based on the literature reviewed so far, the team will investigate
questions such as:

### Flood

1. Under what conditions does a Sentinel-1 flood-mapping baseline
   produce false detections or missed detections?

2. Can rainfall or terrain information provide useful context for
   ambiguous flood detections?

3. Does adding complementary information improve performance on
   selected historical flood events?

### Forest Disturbance

4. Under what conditions does optical-based disturbance monitoring
   become unreliable?

5. When does Sentinel-1 provide useful additional information?

6. Which disturbance types remain difficult to distinguish?

7. Can complementary observations reduce selected false alerts or
   missed disturbances?

### Wildfire

8. What types of false thermal anomalies occur in satellite active-fire
   observations?

9. Under what conditions can active fires be missed?

10. Can optical or environmental information improve interpretation of
    satellite thermal anomalies?

### Cross-Hazard

11. Can a common research framework be used to evaluate complementary
    observations across different environmental hazards?

12. Which failure patterns are common across hazards, and which are
    specific to individual hazard types?

These questions are research directions and will be refined after
dataset inspection and baseline experiments.

---

# 12. Implications for the Proposed Research

The literature review leads to several methodological principles for
this project.

### Principle 1: Establish a baseline

Each hazard should first have a clearly defined baseline approach
before additional information is introduced.

### Principle 2: Add information incrementally

Where possible, additional observations should be introduced in
controlled experiments.

For example:

```text
Baseline
   ↓
Sentinel-1

Baseline + Context
   ↓
Sentinel-1 + rainfall

Baseline + Additional Context
   ↓
Sentinel-1 + rainfall + terrain