# Flood Research References and Research Notes

## 1. Purpose

This document contains the continuous research notes and references for
the flood-monitoring component of the project:

**Satellite-Based Multi-Hazard Intelligence System**

The flood track investigates whether complementary satellite and
environmental observations can improve the reliability of flood
inundation detection and assessment.

The notes cover:

- Flood detection and flood prediction
- Sentinel-1 SAR
- Sentinel-2 optical imagery
- SAR backscatter
- Pre/post flood analysis
- Baseline thresholding
- Copernicus Global Flood Monitoring
- Reference water and exclusion masks
- Rainfall and terrain context
- Multi-source flood research
- Public datasets
- Evaluation metrics
- Error analysis
- Research experiments
- Reproducibility
- Candidate research directions
- Scientific references and data sources

---

# 2. Flood Research Scope

The flood component focuses primarily on **satellite-based flood
inundation detection**, while also studying environmental variables
that may provide useful context.

Potential observations include:

- Sentinel-1 SAR
- Sentinel-2 optical imagery
- Rainfall
- Digital Elevation Models
- Historical flood labels
- Land-cover or water-reference information

The project does not assume that satellite imagery alone can predict
all floods before they happen.

Flood-related research can be divided into different tasks:

1. Flood-risk estimation before an event
2. Flood inundation detection during or after an event
3. Flood extent mapping
4. Flood impact assessment
5. Flood forecasting

The initial experiments will focus on **flood inundation detection and
mapping** because this can be evaluated using historical satellite
observations and reference labels.

---

# 3. Central Flood Research Question

> Can combining complementary satellite and environmental observations
> reduce missed detections and false alarms in flood inundation mapping
> compared with relying on individual observations?

This is part of the larger project research question.

The flood component will test this question experimentally rather than
assuming that multi-source information always improves performance.

---

# 4. Initial Flood Hypothesis

> Complementary satellite and environmental observations may reduce
> certain false alarms and missed flood detections compared with using
> a single observation source, but the improvement may vary according
> to terrain, land cover, flood size, environmental conditions and
> observation quality.

This is a **hypothesis**, not a confirmed result.

The final research contribution must be based on measured experiments.

---

# 5. Flood Detection vs Flood Prediction

These terms must not be confused.

## Flood Prediction

Prediction attempts to estimate where flooding may occur before or
during an event.

Possible inputs include:

- Rainfall
- River discharge
- Soil moisture
- Terrain
- Hydrological models
- Weather forecasts
- Historical flood information

## Flood Detection

Detection identifies areas that are already flooded using observations
of the Earth's surface.

Satellite imagery is particularly useful for this task.

## Flood Mapping

Flood mapping estimates the spatial extent of inundated areas.

For example:

```text
Satellite Image
      ↓
Preprocessing
      ↓
Water/Flood Analysis
      ↓
Flood Classification
      ↓
Flood Mask
      ↓
Flood Area / Map
```

Our first experiments should concentrate on **detection and mapping**.

---

# 6. Why Sentinel-1 SAR Is Important

Sentinel-1 uses Synthetic Aperture Radar (SAR).

Unlike optical satellite imagery, SAR actively transmits microwave
signals and measures the returned signal.

This provides important advantages for flood monitoring.

SAR can collect observations:

- During daytime
- During nighttime
- Under many cloudy conditions

This is especially useful during floods because optical imagery can be
blocked by clouds.

However, SAR is not perfect.

Its observations can be affected by:

- Terrain geometry
- Radar shadows
- Vegetation
- Surface roughness
- Urban structures
- Water surface conditions
- Incidence angle
- Speckle
- Other radar-specific effects

Therefore, SAR should not be treated as an automatically correct flood
label.

---

# 7. Basic SAR Backscatter Concept

A SAR image records information about the amount of radar energy
returned toward the satellite.

This returned signal is commonly called **backscatter**.

A simplified interpretation is:

```text
Radar Signal
     ↓
Earth Surface
     ↓
Returned Signal
     ↓
Backscatter Measurement
```

Different surfaces can produce different backscatter characteristics.

Open, smooth water often produces relatively low radar backscatter
because much of the radar energy is reflected away from the satellite.

Land, vegetation and built surfaces can produce stronger or more
complex returns.

This physical difference makes SAR useful for flood mapping.

However, low backscatter does not automatically mean "flood."

Other surfaces or observation conditions can also produce low or
ambiguous radar responses.

---

# 8. Pre-Flood and Post-Flood Analysis

A common flood-mapping strategy compares observations before and after
a flood event.

Conceptually:

```text
Pre-Flood SAR
      +
Post-Flood SAR
      ↓
Change Analysis
      ↓
Potential Flooded Areas
```

If an area changes from a normal land response to a water-like radar
response, it may indicate inundation.

However, change detection can also respond to changes unrelated to
flooding.

Therefore, contextual information and validation are important.

---

# 9. Simple Threshold Baseline

A simple baseline can classify pixels using a SAR backscatter
threshold.

Conceptually:

```text
SAR Backscatter
      ↓
Compare with Threshold
      ↓
Low Backscatter → Candidate Water/Flood
High Backscatter → Candidate Non-Water/Flood
```

For example:

```text
if backscatter < threshold:
    candidate_flood = 1
else:
    candidate_flood = 0
```

The exact threshold must be determined experimentally.

A threshold must not be selected simply because it produces a visually
good map.

Threshold selection should be documented and evaluated using reference
labels.

---

# 10. Why a Baseline Is Necessary

A research project needs a baseline.

Without a baseline, it is difficult to determine whether a proposed
method actually improves anything.

A simple baseline could be:

**Sentinel-1 SAR threshold-based flood detection**

Later methods can be compared against it.

Possible comparison:

```text
Baseline
Sentinel-1 threshold
        ↓
       F1

Proposed method
Sentinel-1 + context
        ↓
       F1
```

The result should be reported using the same evaluation protocol.

---

# 11. Copernicus Global Flood Monitoring

Copernicus Global Flood Monitoring (GFM) is an important operational
reference system for this research.

It provides global flood monitoring using Sentinel-1 SAR observations.

The GFM service processes Sentinel-1 observations and uses multiple
automated flood-mapping algorithms.

The algorithms are combined through an ensemble approach.

The system produces flood-related information including:

- Observed flood extent
- Reference water information
- Exclusion information
- Flood likelihood

The GFM system is important because it demonstrates that large-scale
operational flood monitoring is already possible.

Therefore, the project should not claim that "satellite flood
detection" itself is novel.

The research should investigate specific limitations and measurable
improvements.

---

# 12. GFM Processing Concept

A simplified representation is:

```text
Sentinel-1 SAR
      ↓
Preprocessing
      ↓
Backscatter
      ↓
Multiple Flood Algorithms
      ↓
Ensemble
      ↓
Flood Extent
      +
Reference Water
      +
Exclusion Information
      +
Flood Likelihood
```

Copernicus documentation describes processing based on Sentinel-1
Level-1 IW GRDH observations and preprocessing toward calibrated
backscatter information.

---

# 13. Important GFM Research Finding

A 2026 scientific paper describing the Sentinel-1 Global Flood
Monitoring service reports that the system has global operational
coverage but that a significant percentage of floods may remain
undetected because of satellite coverage limitations.

The study also reports differences in performance depending on flood
scale and environmental region.

This is important for our research because it suggests that a flood
monitoring system can have errors caused not only by its classification
algorithm but also by the availability and characteristics of the
satellite observations.

Therefore, we should distinguish:

1. Observation limitations
2. Processing limitations
3. Algorithmic limitations
4. Ground-truth limitations

These should not be mixed together.

---

# 14. Reference Water

A flood detector needs to distinguish newly inundated areas from
locations that are normally water.

For example:

```text
Permanent River
     ↓
Normally Water
     ↓
Should not automatically be labelled as New Flood
```

A reference-water layer can therefore provide important contextual
information.

Conceptually:

```text
Current Water-like Signal
          +
Reference Water
          ↓
New Potential Inundation
```

This reduces the risk of interpreting permanent water bodies as flood
water.

---

# 15. Flood Likelihood

Flood mapping can also be expressed probabilistically.

Instead of only:

```text
Flood = 1
No Flood = 0
```

a system may produce something like:

```text
Flood likelihood = 0.92
Flood likelihood = 0.61
Flood likelihood = 0.08
```

This allows thresholds to be investigated and allows uncertainty to be
studied.

The project should preserve probability/confidence information where
the chosen model provides it.

---

# 16. Observation Failure vs Algorithmic Failure

This distinction is important for scientific analysis.

## Observation Failure

The satellite did not obtain suitable information.

Examples:

- No suitable acquisition
- Poor observation geometry
- Severe signal limitations
- Cloud obstruction for optical data

## Algorithmic Failure

Suitable observations exist, but the method incorrectly classifies the
scene.

Examples:

- Permanent water classified as flood
- Urban area classified as flood
- Vegetation interpreted incorrectly
- Shadow or dark surfaces classified as water

A good experiment should try to identify which type of failure caused
an error.

---

# 17. Satellite Coverage Gaps

Satellite-based monitoring depends on when and where observations are
available.

If an event occurs between suitable observations, the system may not
observe the event at the desired time.

This can produce:

- Missed events
- Delayed detection
- Incomplete flood extent
- Uncertainty in event timing

Therefore, detection performance should not be interpreted without
considering observation availability.

---

# 18. Flood Size

Flood size can influence detection.

Large flood events may be easier to detect because they contain larger
continuous areas of inundation.

Small floods can be harder to detect because:

- The flooded region may be smaller than the effective spatial
  resolution.
- Mixed pixels can occur.
- Surface conditions may be ambiguous.
- The change from pre-event conditions may be small.

Therefore, flood size can be included as a condition in error analysis.

---

# 19. Environmental Conditions

Flood detection performance may vary according to:

- Terrain
- Land cover
- Vegetation
- Urbanization
- Water-body type
- Flood depth
- Flood size
- Soil conditions
- Observation geometry

A system that performs well on one environment may behave differently
in another.

This motivates condition-based evaluation.

---

# 20. SAR Exclusion Areas

Research on C-band SAR flood mapping has shown that SAR is not equally
sensitive to floodwater everywhere.

Potential difficult areas include:

- Topographic shadow
- Obstacles
- Dense forest
- Sand
- Other surfaces with ambiguous radar response

Exclusion maps can therefore be useful.

A conceptual approach is:

```text
SAR Image
   ↓
Potential Flood Detection
   ↓
Observation Reliability / Exclusion Analysis
   ↓
Final Flood Map
```

The objective is not to hide difficult areas but to identify locations
where the observation is less reliable.

---

# 21. Three-State Flood Interpretation

Instead of forcing every pixel into only two classes, an experiment can
consider:

```text
Flood
Non-Flood
Uncertain / Excluded
```

This can be scientifically useful when the sensor has known limitations.

The final implementation should determine whether this approach improves
the evaluation results.

---

# 22. Vegetation and Flood Detection

Flooding beneath dense vegetation may be difficult to detect using
certain satellite observations.

Vegetation can interact strongly with radar signals and may hide or
alter the signal associated with water underneath.

Therefore:

```text
Open Water
      ≠
Flood Under Vegetation
```

This is one reason why land-cover or vegetation information may be
useful for condition-based analysis.

---

# 23. Urban Flooding

Urban areas create another difficult environment.

Buildings, roads, vehicles and other structures produce complex radar
responses.

Consequently, urban flood detection may contain:

- False positives
- False negatives
- Shadow-related errors
- Mixed signals

A method that works well over open agricultural areas should not
automatically be assumed to work equally well in cities.

Urban and non-urban scenes should therefore be evaluated separately if
the dataset allows it.

---

# 24. Flood Boundaries and Mixed Pixels

At the boundary between water and land, one satellite pixel may contain
multiple surface types.

For example:

```text
Land | Water
Land | Water
```

A pixel near the boundary can contain both.

This creates uncertainty in classification.

Therefore, boundary pixels should be considered during error analysis.

---

# 25. Sentinel-2 as Supporting Information

Sentinel-2 provides multispectral optical observations.

It can provide information about:

- Vegetation
- Water
- Land cover
- Burned areas
- Surface conditions

However, optical imagery has a major limitation for flood monitoring:

**cloud obstruction.**

During major storms, cloud cover may make optical observations
unavailable or unreliable.

Therefore:

```text
Sentinel-1 SAR
+
Sentinel-2 Optical
```

can provide complementary information, but the combination should be
tested rather than assumed to be universally superior.

---

# 26. Rainfall as Context

Rainfall provides environmental context for flood events.

NASA's GPM IMERG product provides precipitation estimates at high
temporal frequency and can be used as contextual information.

Rainfall can potentially help answer questions such as:

- Did substantial rainfall occur before the detected inundation?
- Was the observed water increase associated with a rainfall event?
- Do false detections occur when rainfall context is absent?
- Does rainfall information improve classification?

Rainfall should not automatically be treated as proof that a pixel is
flooded.

It is contextual evidence.

---

# 27. Terrain as Context

Digital Elevation Models (DEMs) can provide terrain information.

Potential features include:

- Elevation
- Slope
- Terrain position
- Relative elevation
- Drainage-related characteristics

Terrain can help explain why some locations are more susceptible to
inundation.

However, a DEM alone does not prove that a location is flooded.

It should be treated as contextual information.

---

# 28. Multi-Source Flood Research

Modern flood research frequently investigates combinations of:

- SAR
- Optical imagery
- Rainfall
- DEM
- Hydrological information
- Land-cover information
- Historical observations

A simplified multi-source concept is:

```text
             Sentinel-1
                 |
                 v
             SAR Features
                 |
Sentinel-2 → Optical Features
                 |
Rainfall   → Environmental Features
                 |
DEM        → Terrain Features
                 |
                 v
          Flood Detection Model
                 |
                 v
          Flood Probability
                 |
                 v
           Flood Map
```

The scientific question is not simply whether more data can be
combined.

The question is:

> Under which conditions does additional information improve the
> reliability of flood detection?

---

# 29. Sen1Floods11 Dataset

Sen1Floods11 is a widely used benchmark dataset for flood mapping.

The dataset contains:

- 4,831 image chips
- 512 × 512 chip size
- Approximately 120,406 km² of area
- 11 flood events
- 14 biomes
- 357 ecoregions
- 6 continents

It contains Sentinel-1 observations and flood labels.

The dataset has been used to compare flood-mapping approaches including
threshold-based methods and fully convolutional neural networks.

---

# 30. Why Sen1Floods11 Is Useful

It is useful for an initial reproducible experiment because:

- It is publicly available.
- It contains multiple flood events.
- It covers different environmental regions.
- It provides labelled examples.
- It can support baseline comparisons.
- It is suitable for machine-learning experiments.

For the first experiment, a benchmark dataset is preferable to
immediately building a large custom dataset.

---

# 31. Sen1Floods11 Limitations

A benchmark dataset is not equivalent to global real-world
performance.

Potential limitations include:

- Limited number of flood events
- Dataset-specific labeling decisions
- Geographic distribution
- Sampling effects
- Differences between training and real-world deployment
- Potential spatial or temporal dependencies

Therefore, a model that performs well on Sen1Floods11 should not be
described as universally reliable.

---

# 32. Event-Level Generalization

One important research design is to test whether a model generalizes
to flood events that were not used during training.

Instead of randomly mixing all pixels:

```text
Random pixels → Train/Test
```

a stronger design can be:

```text
Flood Events A–I → Training
Flood Events J–K → Testing
```

This tests whether the model learned flood-related patterns rather than
memorizing characteristics of the same events.

---

# 33. GEOID-Flood Dataset Direction

A newer dataset direction is GEOID-Flood, which has been described as
a large global benchmark containing thousands of tiles across many
historical flood events and countries, with Sentinel-1, Sentinel-2,
DEM-related information and manually validated labels.

Because this is a newer research resource, the exact dataset version,
access conditions and benchmark protocol must be verified before being
used in the final experiments.

It may be useful for testing broader geographical generalization.

---

# 34. Candidate Data Sources

Potential flood research data sources include:

## Sentinel-1

Primary SAR observation source.

Use for:

- Flood extent
- Pre/post comparison
- Backscatter analysis

## Sentinel-2

Optical supporting source.

Use for:

- Water/land information
- Vegetation context
- Land-cover context
- Post-event visual interpretation

## GPM IMERG

Rainfall context.

Use for:

- Precipitation history
- Event context
- Temporal analysis

## DEM

Terrain context.

Use for:

- Elevation
- Slope
- Terrain analysis

## Historical Flood Labels

Use for:

- Training
- Validation
- Testing
- Evaluation

---

# 35. Baseline Models

Possible baselines include:

### Baseline 1: SAR Threshold

Input:

- Sentinel-1 backscatter

Method:

- Fixed or experimentally selected threshold

Output:

- Flood / non-flood mask

### Baseline 2: SAR Change Detection

Input:

- Pre-event SAR
- Post-event SAR

Method:

- Detect significant change

Output:

- Candidate flood mask

### Baseline 3: Machine Learning

Inputs may include:

- SAR features
- Optical features
- Rainfall
- Terrain

Possible models:

- Logistic Regression
- Random Forest
- Gradient Boosting

### Baseline 4: Deep Learning

Possible models:

- FCNN
- U-Net
- CNN-based segmentation networks

Deep learning should be introduced after the simpler baselines are
understood.

---

# 36. Proposed Experimental Ladder

The research can progress from simple to complex:

```text
F-01
Data Inspection
      ↓
F-02
Simple SAR Baseline
      ↓
F-03
Pre/Post Change Detection
      ↓
F-04
SAR + Environmental Context
      ↓
F-05
Multi-Source Machine Learning
      ↓
F-06
Deep Learning / Segmentation
      ↓
Error Analysis
      ↓
Generalization Testing
```

This prevents the project from jumping directly to a complex neural
network without understanding the data.

---

# 37. Candidate Feature Set

Potential features include:

## SAR

- VV backscatter
- VH backscatter
- VV/VH ratio
- Pre-event values
- Post-event values
- Difference
- Ratio
- Temporal statistics

## Optical

- Reflectance bands
- NDVI
- NDWI or related water indices
- Change in spectral response

## Rainfall

- Recent rainfall
- Cumulative rainfall
- Rainfall anomaly

## Terrain

- Elevation
- Slope
- Terrain-derived features

The final feature set should be determined experimentally.

---

# 38. Evaluation Metrics

Flood segmentation can be evaluated using:

## Precision

Of the pixels predicted as flood, how many were actually flood?

```text
Precision = TP / (TP + FP)
```

## Recall

Of the actual flooded pixels, how many were detected?

```text
Recall = TP / (TP + FN)
```

## F1 Score

Harmonic mean of precision and recall.

```text
F1 = 2 × Precision × Recall / (Precision + Recall)
```

## Intersection over Union

```text
IoU = TP / (TP + FP + FN)
```

IoU is especially useful for comparing predicted flood masks with
reference masks.

---

# 39. Flood-Area Error

A model may produce a visually reasonable mask but estimate the wrong
total flooded area.

Therefore, flooded-area error can also be measured.

Conceptually:

```text
Reference Flood Area
        vs
Predicted Flood Area
```

Possible measure:

```text
Area Error =
|Predicted Area - Reference Area|
```

A normalized version can also be considered.

---

# 40. Error Analysis

Aggregate metrics are not enough.

The project should inspect:

- False positives
- False negatives
- Boundary errors
- Permanent water confusion
- Urban errors
- Vegetation-related errors
- Terrain-related errors
- Small-flood errors
- Large-flood errors
- Observation-gap cases

Example:

```text
Prediction
    ↓
Compare with Label
    ↓
TP / FP / FN / TN
    ↓
Map Error Locations
    ↓
Investigate Cause
```

This is where scientific insight may emerge.

---

# 41. Condition-Based Evaluation

Instead of reporting only one global score, results can be grouped
according to conditions.

For example:

| Condition | Possible Analysis |
|---|---|
| Urban | Precision/Recall/F1 |
| Rural | Precision/Recall/F1 |
| Forested | Precision/Recall/F1 |
| Open terrain | Precision/Recall/F1 |
| Small flood | Detection performance |
| Large flood | Detection performance |
| High rainfall | Detection performance |
| Low rainfall | Detection performance |

This can reveal where the model actually helps.

---

# 42. Candidate Research Direction A: Observation-Reliability-Aware Flood Mapping

Possible research idea:

> Can flood mapping performance be improved by explicitly identifying
> observation conditions where SAR-based flood detection is less
> reliable?

Possible approach:

```text
SAR Observation
      ↓
Flood Candidate
      +
Observation Reliability
      ↓
Flood / Non-Flood / Uncertain
```

This should be tested against a normal binary baseline.

---

# 43. Candidate Research Direction B: Terrain-Aware Flood Mapping

Possible research question:

> Does terrain information improve flood classification in difficult
> environments?

Inputs:

- SAR
- DEM
- Terrain features

Compare:

```text
SAR only
vs
SAR + Terrain
```

The contribution would require measurable improvement and error analysis.

---

# 44. Candidate Research Direction C: Rainfall-Aware Flood Interpretation

Possible research question:

> Does recent rainfall context reduce false flood detections or improve
> interpretation of ambiguous SAR changes?

Compare:

```text
SAR only
vs
SAR + Rainfall
```

Rainfall should be aligned temporally with the satellite observation.

---

# 45. Candidate Research Direction D: Difficult-Scene Multi-Source Detection

Possible research question:

> Does combining complementary observations improve flood mapping
> specifically in difficult scenes?

Difficult scenes could include:

- Urban areas
- Vegetated areas
- Complex terrain
- Small floods
- Ambiguous water surfaces

This direction may be stronger than simply measuring performance on
average scenes because it focuses on failure cases.

---

# 46. Candidate Research Direction E: Unseen-Event Generalization

Possible research question:

> Does a model trained on some flood events generalize to geographically
> or temporally different flood events?

Evaluation:

```text
Known Events
     ↓
Training
     ↓
Unseen Event
     ↓
Testing
```

This can be more informative than random pixel splitting.

---

# 47. What Would Count as a Meaningful Result?

A meaningful research result should contain:

1. A clearly defined problem.
2. A documented baseline.
3. A reproducible dataset.
4. A controlled experiment.
5. Appropriate evaluation metrics.
6. Statistical or repeated evidence where appropriate.
7. Error analysis.
8. Limitations.
9. Reproducible code and configuration.

Example structure:

```text
Baseline:
SAR threshold

Proposed:
SAR + terrain + rainfall

Evaluation:
Same test events

Result:
Metric comparison

Then:
Error analysis

Then:
Determine whether the additional information actually helped.
```

The project must not choose a method merely because it produces a
higher score on one split.

---

# 48. Event-Level Evaluation

Random pixel-level splitting can produce overly optimistic results if
nearby pixels from the same event appear in both training and testing.

Therefore, event-level separation should be considered.

Example:

```text
Training:
Flood Event A
Flood Event B
Flood Event C

Testing:
Flood Event D
```

This better represents deployment on a new flood event.

---

# 49. Generalization Evaluation

Generalization can be tested across:

- Different locations
- Different countries
- Different climate zones
- Different terrain
- Different flood sizes
- Different land-cover conditions
- Different acquisition dates

A strong experiment should clearly state which type of generalization
is being measured.

---

# 50. Data Leakage

Data leakage occurs when information from the test set indirectly
influences training or preprocessing.

Examples:

- Normalizing using all data before splitting.
- Selecting thresholds using the test labels.
- Training on pixels from an event that later appears in the test set.
- Tuning hyperparameters using the final test set.

Correct structure:

```text
Training Data
     ↓
Model / Threshold Selection
     ↓
Validation
     ↓
Final Test
```

The test set should remain untouched until final evaluation.

---

# 51. Class Imbalance

Flood datasets may contain many more non-flood pixels than flood
pixels.

For example:

```text
Non-Flood: 95%
Flood:      5%
```

A model could obtain high accuracy by predicting nearly everything as
non-flood.

Therefore, accuracy alone can be misleading.

Use metrics such as:

- Precision
- Recall
- F1
- IoU
- Flood-area error

---

# 52. Threshold Selection

If a threshold-based method is used, the threshold should be selected
using a documented procedure.

Possible approaches:

- Literature-supported threshold
- Training/validation optimization
- Event-specific calibration
- Otsu or other image-based thresholding

The same evaluation protocol should then be applied consistently.

---

# 53. Spatial Resolution

Different observations have different spatial resolutions.

For example:

- Sentinel-1
- Sentinel-2
- Rainfall products
- DEM products

cannot simply be combined without considering their spatial grids.

A multi-source model may require:

```text
Original Datasets
       ↓
Projection Alignment
       ↓
Spatial Resampling
       ↓
Common Grid
       ↓
Feature Stack
```

The resampling method should be documented because it can affect the
final result.

---

# 54. Temporal Alignment

Different sensors observe the Earth at different times.

For example:

```text
Rainfall
   ↓
Time history

Sentinel-1
   ↓
Satellite acquisition

Sentinel-2
   ↓
Different acquisition time
```

Therefore, features should be aligned using a clearly defined temporal
window.

Example:

```text
Satellite observation:
T

Rainfall context:
T-1 day to T
```

The exact window should be determined experimentally and documented.

---

# 55. Ground Truth / Reference Labels

Satellite flood detection requires reference information.

Possible sources include:

- Manually interpreted satellite imagery
- Benchmark dataset labels
- High-resolution imagery
- Official flood maps
- Other validated reference products

Labels themselves can contain uncertainty.

Therefore, "ground truth" should not automatically be treated as
perfect truth.

The source, labeling method and limitations must be documented.

---

# 56. Validation Hierarchy

A useful validation structure is:

```text
Dataset Validation
       ↓
Preprocessing Validation
       ↓
Baseline Validation
       ↓
Model Validation
       ↓
Event-Level Testing
       ↓
Error Analysis
       ↓
Independent / Additional Dataset
```

The strongest claims should be supported by more than one evaluation
setting where practical.

---

# 57. Experiment F-01 — Data Inspection

Objective:

Understand the actual flood dataset before building models.

Tasks:

1. Load one sample.
2. Inspect dimensions.
3. Inspect data types.
4. Inspect value ranges.
5. Visualize SAR.
6. Visualize the flood label.
7. Check missing values.
8. Check class distribution.
9. Understand the coordinate/reference information.
10. Document observations.

Output:

```text
notebooks/flood/F01_data_inspection.ipynb
```

---

# 58. Experiment F-02 — Simple SAR Baseline

Objective:

Build the simplest reproducible flood detector.

Steps:

1. Load SAR.
2. Preprocess.
3. Select threshold.
4. Generate flood mask.
5. Compare with reference label.
6. Calculate precision.
7. Calculate recall.
8. Calculate F1.
9. Calculate IoU.
10. Visualize errors.

Output:

- Baseline flood mask
- Metrics
- Error map
- Threshold documentation

---

# 59. Experiment F-03 — Pre/Post Change Detection

Objective:

Investigate whether change between pre-flood and post-flood SAR
observations improves detection.

Concept:

```text
Pre-Flood SAR
       +
Post-Flood SAR
       ↓
Difference / Ratio
       ↓
Threshold
       ↓
Flood Mask
```

Compare this against the single-image baseline.

---

# 60. Experiment F-04 — SAR + Environmental Context

Objective:

Test whether environmental information improves difficult cases.

Possible inputs:

- SAR
- Rainfall
- DEM

Comparison:

```text
SAR only
     vs
SAR + Rainfall
     vs
SAR + Terrain
     vs
SAR + Rainfall + Terrain
```

Use the same test protocol.

---

# 61. Experiment F-05 — Multi-Source Machine Learning

Possible models:

- Logistic Regression
- Random Forest
- Gradient Boosting

Example:

```text
VV
VH
VV/VH
SAR Change
Rainfall
Elevation
Slope
       ↓
Machine Learning Model
       ↓
Flood Probability
       ↓
Flood Mask
```

The purpose is not to use a complex model simply because it is
available.

The purpose is to test whether complementary information improves
classification.

---

# 62. Experiment F-06 — Deep Learning / Segmentation

Only after the simpler experiments should the team consider:

- CNN
- FCNN
- U-Net
- Other segmentation architectures

Possible input:

```text
SAR
+
Optical
+
Context
```

Output:

```text
Pixel-wise Flood Probability
```

The deep-learning model should be compared with simpler baselines.

---

# 63. Experimental Comparison Matrix

| Experiment | Main Input | Method | Main Question |
|---|---|---|---|
| F-01 | Dataset | Inspection | What does the data contain? |
| F-02 | SAR | Threshold | How strong is a simple baseline? |
| F-03 | Pre/Post SAR | Change detection | Does temporal change help? |
| F-04 | SAR + Context | Rule/ML | Does context help? |
| F-05 | Multi-source | ML | Does complementary information improve results? |
| F-06 | Multi-source | Deep learning | Can segmentation improve further? |

---

# 64. Research Decision Tree

```text
Start
  ↓
Can SAR baseline detect floods?
  ↓
Yes / No
  ↓
Where does it fail?
  ↓
Identify difficult conditions
  ↓
Select relevant contextual information
  ↓
Test additional information
  ↓
Does performance improve?
  ↓
Yes / No
  ↓
Check whether improvement generalizes
  ↓
Analyze errors
  ↓
Define research contribution
```

This approach keeps the research evidence-driven.

---

# 65. What Would NOT Be a Strong Contribution?

The following alone would not establish a strong research contribution:

- Creating a dashboard
- Showing satellite images
- Applying a common CNN
- Combining datasets without evaluation
- Claiming "AI-powered flood detection"
- Reporting only accuracy
- Testing only one event
- Randomly splitting pixels without considering event leakage
- Showing one attractive map
- Claiming novelty without literature evidence

---

# 66. What Could Become a Stronger Contribution?

A stronger contribution could be:

- Identification of a reproducible failure condition.
- A measurable improvement over a documented baseline.
- Better performance on difficult scenes.
- Improved generalization to unseen events.
- Reduction of false alarms.
- Reduction of missed flood areas.
- Better uncertainty handling.
- A documented observation-reliability framework.

The exact contribution must be decided after experiments.

---

# 67. Possible Final Research Contribution Structure

A possible final paper structure:

```text
Problem
  ↓
Existing Systems
  ↓
Documented Limitation
  ↓
Research Question
  ↓
Baseline
  ↓
Proposed Method
  ↓
Controlled Experiments
  ↓
Results
  ↓
Error Analysis
  ↓
Generalization
  ↓
Limitations
  ↓
Scientific Finding
```

---

# 68. Reproducibility Requirements

For every experiment record:

- Dataset name
- Dataset version
- Download source
- Date accessed
- Geographic coverage
- Event IDs
- Train/validation/test split
- Preprocessing
- Feature definitions
- Model parameters
- Thresholds
- Random seeds
- Evaluation metrics
- Software versions
- Hardware information when relevant

This makes the experiment auditable.

---

# 69. GitHub Research Record

Flood research files can be organized as:

```text
research/
└── flood/
    ├── research_notes.md
    ├── datasets.md
    ├── experiments.md
    └── findings.md

notebooks/
└── flood/
    ├── F01_data_inspection.ipynb
    ├── F02_sar_baseline.ipynb
    ├── F03_change_detection.ipynb
    └── F04_context_experiment.ipynb

results/
└── flood/
    ├── figures/
    ├── tables/
    └── maps/
```

The exact structure can evolve as the research develops.

---

# 70. Reproducibility Principle

Every important research result should be traceable:

```text
Result
  ↓
Experiment
  ↓
Code
  ↓
Dataset
  ↓
Source
```

A reviewer should be able to understand how a result was obtained.

---

# 71. Current Scientific Understanding

Based on the reviewed material:

1. Sentinel-1 SAR is highly useful for flood mapping.
2. Optical imagery can provide complementary information but may be
   limited by clouds.
3. Rainfall can provide useful environmental context.
4. Terrain can provide useful geographic context.
5. Operational systems such as Copernicus GFM already perform global
   Sentinel-1-based flood monitoring.
6. Existing research already investigates multi-source flood mapping.
7. Therefore, sensor fusion alone should not be claimed as novel.
8. Flood detection has observation and algorithmic failure modes.
9. Difficult scenes require specific error analysis.
10. Generalization to unseen flood events is important.
11. The final research contribution must be established through
    experiments.

---

# 72. Current Research Gap Status

The final research gap is **not yet established**.

The current working direction is:

> Investigate whether complementary observations can address specific,
> measurable failure conditions in satellite flood mapping.

Potential directions include:

- Observation-reliability-aware mapping
- Terrain-aware mapping
- Rainfall-aware interpretation
- Difficult-scene multi-source detection
- Unseen-event generalization

The final direction should be selected only after reviewing the data and
baseline results.

---

# 73. Research Questions Generated So Far

### RQ1

Can Sentinel-1 SAR alone reliably detect flood inundation across
different environments?

### RQ2

Which conditions produce the largest false-positive and false-negative
rates?

### RQ3

Does pre/post SAR change analysis improve flood detection compared with
single-image thresholding?

### RQ4

Does rainfall context improve interpretation of ambiguous flood
detections?

### RQ5

Does terrain information improve flood classification in difficult
environments?

### RQ6

Does multi-source information improve performance on unseen flood
events?

### RQ7

Can observation-reliability information identify areas where flood
classification should be treated as uncertain?

---

# 74. First Practical Dataset Strategy

The first implementation should use a manageable benchmark dataset
rather than immediately downloading massive global satellite archives.

Recommended initial sequence:

```text
Benchmark Dataset
       ↓
Understand Data
       ↓
Build Baseline
       ↓
Evaluate
       ↓
Identify Errors
       ↓
Decide Next Experiment
```

After the baseline is stable, the team can expand to additional
datasets or real-world event analysis.

---

# 75. Flood Research Workflow

The complete workflow is:

```text
Research Question
       ↓
Literature Review
       ↓
Existing Systems
       ↓
Documented Limitations
       ↓
Dataset Selection
       ↓
Data Inspection
       ↓
Baseline
       ↓
Evaluation
       ↓
Error Analysis
       ↓
Research Direction
       ↓
Controlled Experiment
       ↓
Comparison
       ↓
Generalization
       ↓
Scientific Finding
       ↓
Documentation
       ↓
Integration
```

---

# 76. Immediate Coding Plan

The project is now ready to enter the coding stage, but coding should
begin with **data inspection and a baseline**, not immediately with
CNN/U-Net development.

The first practical objective is:

> Generate and evaluate one reproducible flood mask from a real flood
> dataset.

---

# 77. Coding Experiment F-01

Create:

```text
notebooks/flood/F01_data_inspection.ipynb
```

The notebook should contain:

1. Environment check
2. Imports
3. Dataset loading
4. File/sample inspection
5. Shape inspection
6. Value-range inspection
7. SAR visualization
8. Label visualization
9. Class distribution
10. Missing-value checks
11. Basic observations

The notebook should be understandable by every team member.

---

# 78. What to Learn From F-01

After F-01, the team should be able to answer:

- What is one training example?
- What is the input shape?
- What is the label shape?
- Which bands/channels are present?
- What are the value ranges?
- Which values represent flood?
- How imbalanced is the dataset?
- Are there missing or invalid pixels?
- How does the flood mask visually correspond to the SAR image?

Do not proceed to modeling until these questions are understood.

---

# 79. Expected First Coding Folder Structure

```text
satellite-multi-hazard-ai/
│
├── research/
│   └── flood/
│       ├── research_notes.md
│       ├── datasets.md
│       ├── experiments.md
│       └── findings.md
│
├── notebooks/
│   └── flood/
│       └── F01_data_inspection.ipynb
│
├── src/
│   ├── preprocessing/
│   ├── features/
│   ├── models/
│   └── evaluation/
│
└── results/
    └── flood/
        ├── figures/
        ├── tables/
        └── maps/
```

Do not create unnecessary files before they are needed.

---

# 80. First Milestone

The first milestone is:

> Successfully inspect a real flood dataset and generate a reproducible
> baseline flood mask.

Evidence should include:

- Dataset identification
- Sample visualization
- Label visualization
- Class distribution
- Baseline method
- Metrics
- Error visualization

---

# 81. Second Milestone

The second milestone is:

> Understand where the baseline fails.

The team should investigate:

- Urban scenes
- Vegetated scenes
- Permanent water
- Small floods
- Large floods
- Terrain-related cases
- Observation limitations

---

# 82. Third Milestone

The third milestone is:

> Test whether additional information addresses a documented failure.

Possible additions:

- Rainfall
- DEM
- Optical information
- Temporal SAR information

---

# 83. Fourth Milestone

The fourth milestone is:

> Test whether the observed improvement generalizes beyond the
> conditions used to develop the method.

This can include:

- Unseen flood events
- Different regions
- Different environmental conditions

---

# 84. Final Scientific Goal

The final goal is not simply to build a flood-detection application.

The goal is to determine, using reproducible evidence:

> Which complementary observations, if any, improve flood-monitoring
> reliability, under which conditions, and by how much compared with
> appropriate baselines?

That question should guide the experiments.

---

# 85. Key Scientific References

## Global Flood Monitoring

**The fully-automatic Sentinel-1 Global Flood Monitoring service:
Scientific challenges and future directions**

Remote Sensing of Environment, 2026.

DOI:

`10.1016/j.rse.2025.115108`

This work describes the scientific and operational design of the
Sentinel-1 Global Flood Monitoring service, including its ensemble
approach, reference information, global processing and documented
limitations.

---

## Copernicus Global Flood Monitoring Documentation

Copernicus Data Space documentation on Global Flood Monitoring.

The documentation describes:

- Sentinel-1 Level-1 IW GRDH input
- Backscatter preprocessing
- Automated flood algorithms
- Ensemble processing
- Observed flood extent
- Reference water
- Exclusion information
- Flood likelihood

Official source:

https://documentation.dataspace.copernicus.eu/Data/CopernicusServices/ContinentalFloodMonitoring.html

Verify the current documentation version before citing specific
implementation details in the final paper.

---

## SAR Exclusion Maps

**Deriving exclusion maps from C-band SAR time-series in support of
floodwater mapping**

Remote Sensing of Environment, 2021, 265, 112668.

DOI:

`10.1016/j.rse.2021.112668`

This work investigates areas where C-band SAR is less suitable for
floodwater mapping and the use of temporal SAR information for
exclusion maps.

---

## Sen1Floods11

**Sen1Floods11: A Geospatial Dataset for Training and Benchmarking
Flood Segmentation in Sentinel-1 Imagery**

Bonafilia et al., 2020.

The dataset provides thousands of Sentinel-1 image chips associated
with flood events and reference flood labels and is useful for
benchmarking flood segmentation approaches.

---

## GEOID-Flood

**GEOID-Flood: A Global Earth Observation Dataset for Flood Mapping**

2026 research preprint/dataset direction.

The reported dataset contains a large collection of flood-event tiles
across many countries and combines Earth-observation information with
validated flood labels.

The exact version, metadata and access conditions should be verified
before inclusion in the final experimental protocol.

---

# 86. Official Data Sources

## ESA Sentinel-1

https://www.esa.int/Applications/Observing_the_Earth/Copernicus/Sentinel-1

## ESA Sentinel-2

https://www.esa.int/Applications/Observing_the_Earth/Copernicus/Sentinel-2

## Copernicus Data Space Ecosystem

https://dataspace.copernicus.eu/

## NASA GPM IMERG

https://gpm.nasa.gov/data/imerg

## NASA Earthdata

https://www.earthdata.nasa.gov/

## Global Flood Monitoring

https://documentation.dataspace.copernicus.eu/Data/CopernicusServices/ContinentalFloodMonitoring.html

---

# 87. Research Integrity Rules

The flood component must follow these rules:

1. Do not claim novelty before literature review and experiments.
2. Do not invent accuracy values.
3. Do not report unverified results.
4. Do not treat a benchmark label as perfect ground truth.
5. Do not use the final test set for tuning.
6. Do not hide failure cases.
7. Do not report only the best-performing experiment.
8. Record dataset versions and preprocessing.
9. Record thresholds and model parameters.
10. Keep the GitHub research history reproducible.
11. Distinguish detection from prediction.
12. Distinguish observation limitations from algorithmic limitations.
13. Report limitations together with results.
14. Clearly identify which findings are experimental and which are
    established from previous literature.

---

# 88. Research Status

Current status:

**Research phase completed sufficiently to begin baseline coding.**

Completed conceptual work:

- Flood scope defined
- Research question defined
- Initial hypothesis defined
- Existing systems reviewed
- Sentinel-1 role understood
- Sentinel-2 role understood
- Rainfall context identified
- Terrain context identified
- Candidate datasets identified
- Evaluation metrics identified
- Baseline strategy defined
- Candidate research directions identified

Not yet completed:

- Actual dataset experiment
- Baseline metrics
- Error maps
- Comparative experiments
- Final research gap
- Final research contribution

Therefore, no final performance claim should yet be made.

---

# 89. Immediate Next Step

Start with:

```text
F-01 Data Inspection
```

Then proceed in this order:

```text
F-01 Data Inspection
        ↓
F-02 SAR Baseline
        ↓
F-03 Pre/Post Change Detection
        ↓
Error Analysis
        ↓
Select Research Direction
        ↓
F-04 Context Experiment
        ↓
F-05 Multi-Source ML
        ↓
Generalization Testing
        ↓
Final Research Finding
```

The first coding goal is simple:

> Understand the data before trying to make the model intelligent.

---

# 90. Final Note

This document is a research working document, not the final research
paper.

As experiments are completed, the following sections should be updated
with actual evidence:

- Research gap
- Experimental methodology
- Results
- Error analysis
- Findings
- Limitations
- Final contribution

No experimental result should be added here unless it is reproducible
from the project's recorded code, data and evaluation procedure.
