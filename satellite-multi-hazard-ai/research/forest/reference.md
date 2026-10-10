Forest Disturbance Research References and Research Notes

Forest Disturbance Research References and Research Notes

1. Purpose

This document records the scientific and technical research conducted for the forest-disturbance component of the AI Agent for Multi-Hazard Environmental Monitoring Using Satellite and Auxiliary Data.

The purpose is to understand satellite-based forest disturbance detection, available datasets, limitations, algorithms, evaluation methods, and a practical research direction.

2. Forest Disturbance Research Scope

The module focuses on detecting and interpreting changes in forested areas using satellite observations.

The scope includes forest clearing, logging, wildfire impacts, storms, drought-related damage, insect or disease impacts, and other detectable disturbances.

3. Central Forest Disturbance Research Question

The main question is:

Can multi-temporal satellite observations and auxiliary information detect forest disturbance more reliably than a simple single-date or single-source change detector?

4. Initial Forest Disturbance Hypothesis

A multi-temporal approach should reduce false detections caused by seasonal vegetation changes, clouds, shadows, and temporary spectral variation.

Adding contextual information may also improve disturbance interpretation.

5. Forest Disturbance Detection vs Deforestation vs Forest Degradation

Forest disturbance is the broadest concept.

Deforestation generally implies longer-term conversion of forest to another land use, while degradation may reduce forest condition without complete clearing.

Therefore, every detected tree-cover change should not automatically be labelled as deforestation.

6. Why Landsat Is Important

Landsat provides a long historical record of multispectral Earth observation.

Its long time series and approximately 30 m spatial resolution make it valuable for studying forest disturbance and recovery over years or decades.

7. Why Sentinel-2 Is Important

Sentinel-2 provides recent multispectral observations with 10 m resolution for selected bands and frequent revisit opportunities.

It can provide finer spatial information for recent forest changes and complement Landsat time series.

8. Forest Spectral Response

Healthy vegetation interacts strongly with visible, near-infrared, and shortwave-infrared wavelengths.

Disturbance can change vegetation reflectance because of canopy removal, moisture changes, exposed soil, dead vegetation, or burned material.

9. Pre-Disturbance and Post-Disturbance Analysis

A basic strategy is to compare observations before and after a suspected disturbance.

The challenge is selecting comparable dates and separating actual disturbance from seasonal or atmospheric differences.

10. Simple Change-Detection Baseline

A first baseline can calculate spectral differences between pre- and post-disturbance images.

This establishes a simple reference against which advanced methods can be evaluated.

11. Global Forest Watch

Global Forest Watch (GFW) provides forest monitoring datasets, maps, alerts, and analysis tools.

Its datasets can support exploratory analysis and reference-label construction.

12. GFW Tree-Cover-Loss Concept

GFW tree-cover-loss data measures detectable loss of tree cover rather than directly measuring legal or permanent deforestation.

The underlying global dataset is derived from satellite observations at approximately 30 m resolution.

13. Important GFW Research Finding

Tree-cover loss can result from human activities or natural disturbances and can be temporary or permanent.

Therefore, tree-cover-loss maps should be treated as disturbance evidence rather than automatic proof of deforestation.

14. Tree-Cover Loss vs Deforestation

A cleared area may later regenerate, may be part of a plantation cycle, or may have been caused by wildfire or another natural event.

Attribution and persistence require additional temporal and contextual evidence.

15. Disturbance Attribution

Detection answers where and when change occurred.

Attribution attempts to answer why the change occurred, such as wildfire, logging, agriculture, infrastructure, or natural disturbance.

16. Observation Failure vs Algorithmic Failure

A missed disturbance does not necessarily mean that the algorithm is poor.

Clouds, smoke, observation timing, missing imagery, and sensor limitations can prevent the event from being observed clearly.

17. Temporal Observation Gaps

Forest change may occur between available clear observations.

A time-series system should represent observation gaps and should not treat missing observations as evidence of no change.

18. Disturbance Size

Large disturbances are generally easier to detect than small fragmented disturbances.

Small clearings can occupy only part of a pixel and may produce weak or mixed spectral signals.

19. Environmental Conditions

Rainfall, soil moisture, vegetation condition, temperature, and drought can change spectral responses without representing permanent forest loss.

These variables can provide useful context for interpretation.

20. Cloud / Shadow / Observation Limitations

Optical satellite observations can be blocked or contaminated by clouds and cloud shadows.

Persistent cloud cover can delay reliable detection, especially in humid tropical regions.

21. Three-State Disturbance Interpretation

A useful conceptual model is:

1. Stable forest
2. Disturbed or changed forest
3. Persistent/non-recovered change

This is more scientifically cautious than directly assigning every change to deforestation.

22. Forest Canopy and Understory Limitations

Satellite observations primarily capture the signal visible from above the canopy.

Understory damage or partial degradation may remain difficult to detect when the upper canopy remains relatively unchanged.

23. Agricultural / Plantation / Land-Use Confusion

Harvesting plantations, agricultural clearing, shifting cultivation, and natural forest disturbance can produce similar spectral patterns.

Land-cover and temporal context are therefore important for attribution.

24. Disturbance Boundaries and Mixed Pixels

A 30 m pixel can contain multiple land-cover types.

Mixed pixels near disturbance boundaries can reduce detection precision and create uncertain labels.

25. Sentinel-2 as Supporting Information

Sentinel-2 can help inspect the spatial extent and recent development of disturbances at finer resolution.

It can provide supporting evidence alongside longer Landsat time series.

26. Rainfall / Weather Context

Weather information can help explain unusual vegetation changes and distinguish environmental stress from some human-caused disturbances.

It should be treated as supporting evidence rather than direct proof of a disturbance driver.

27. Terrain Context

Elevation, slope, and terrain position can influence forest condition, accessibility, disturbance patterns, and satellite illumination.

Terrain variables may therefore be useful contextual features.

28. Multi-Source Forest Disturbance Research

A multi-source system can combine:

- Landsat
- Sentinel-2
- Global Forest Watch
- Land-cover information
- Weather/rainfall
- Terrain
- Fire information

The purpose is to reduce dependence on one observation source.

29. Hansen Global Forest Change Dataset

Hansen et al. developed a global Landsat-based dataset for mapping forest cover and forest-cover change.

It became an important foundation for large-scale forest monitoring.

30. Why Hansen Dataset Is Useful

The dataset provides globally consistent information that can support historical analysis and comparison of forest-cover change.

It is useful for building research baselines and identifying candidate disturbance areas.

31. Dataset Limitations

Global datasets use fixed definitions, thresholds, spatial resolutions, and processing assumptions.

They should therefore be interpreted within their documented scope rather than treated as perfect ground truth.

32. Event-Level / Region-Level Generalization

A model that performs well on randomly selected pixels may fail in a new geographic region.

Evaluation should include geographically separated events or regions whenever possible.

33. LandTrendr Direction

LandTrendr models Landsat spectral trajectories over time instead of comparing only two images.

It can identify gradual trends, abrupt changes, and recovery patterns.

34. Candidate Data Sources

Potential sources include:

- USGS Landsat
- Copernicus Sentinel-2
- Global Forest Watch
- Hansen Global Forest Change
- Weather datasets
- Digital elevation models
- Fire datasets where required

35. Baseline Models

Possible baselines include:

1. Simple spectral difference
2. NDVI/NDMI/NBR change
3. Threshold-based change detection
4. Random Forest
5. Gradient boosting
6. Temporal models
7. Segmentation/deep-learning methods

36. Proposed Experimental Ladder

The experiments should progress from simple to complex:

spectral change → multi-temporal indices → contextual features → machine learning → advanced temporal/deep-learning methods.

This prevents unnecessary model complexity.

37. Candidate Feature Set

Candidate features include:

- Red reflectance
- NIR reflectance
- SWIR reflectance
- NDVI
- NDMI
- NBR where fire-related change is relevant
- Pre/post differences
- Temporal statistics
- Rainfall
- Elevation/slope
- Land-cover class

38. Evaluation Metrics

Recommended metrics include:

- Precision
- Recall
- F1-score
- Intersection over Union (IoU), where spatial labels are available
- Area/change error

Accuracy alone should not be the only metric.

39. Forest-Area Change Error

A model can obtain good pixel-level accuracy but still estimate the disturbed area incorrectly.

Area-based evaluation should therefore compare predicted disturbed area with reference disturbed area.

40. Error Analysis

False positives and false negatives should be examined separately.

Examples should be grouped by cause, such as cloud contamination, agriculture, seasonal change, small disturbance, or missed event.

41. Condition-Based Evaluation

Performance should be measured under different conditions:

- Clear vs cloudy periods
- Large vs small disturbances
- Dense vs sparse forest
- Different seasons
- Different geographic regions

42. Candidate Research Direction A — Observation-Reliability-Aware Disturbance Detection

The system can estimate whether sufficient high-quality observations exist before making a strong disturbance decision.

This separates low-confidence results caused by poor observations from genuine model uncertainty.

43. Candidate Research Direction B — Multi-Temporal Change Detection

Instead of comparing only two dates, the system can analyse a sequence of observations.

Persistent change should receive greater confidence than a one-time spectral anomaly.

44. Candidate Research Direction C — Disturbance Attribution

After detecting change, the system can compare the event against contextual signals to estimate likely disturbance categories.

The output should include uncertainty rather than presenting attribution as absolute truth.

45. Candidate Research Direction D — Multi-Source Forest Monitoring

The proposed agent can select appropriate data sources depending on the detected problem.

For example, optical imagery can establish vegetation change while fire and weather information can support interpretation.

46. Candidate Research Direction E — Unseen-Region Generalization

A strong experiment is to develop using some regions and evaluate on geographically separate regions.

This tests whether the approach learned general disturbance patterns rather than local visual characteristics.

47. What Would Count as a Meaningful Result?

A meaningful result would show measurable improvement over a simple baseline.

The improvement should be demonstrated using defined datasets, metrics, and controlled experiments.

48. Event-Level Evaluation

Where possible, evaluation should treat a disturbance event as a meaningful unit rather than evaluating only independent pixels.

This better reflects practical forest-monitoring performance.

49. Generalization Evaluation

The final system should ideally be tested outside the exact areas used for development.

This is important for an agent intended for multi-region environmental monitoring.

50. Data Leakage

Temporal or spatial leakage can make results appear better than they really are.

Training and test samples should be separated carefully, especially when neighbouring pixels or repeated observations come from the same event.

51. Class Imbalance

Stable forest pixels may greatly outnumber disturbed pixels.

Metrics and sampling strategies should account for this imbalance.

52. Threshold Selection

Thresholds for spectral change should be selected using training/validation data rather than tuned on the final test set.

53. Spatial Resolution

Different sources operate at different spatial resolutions.

Resampling should be documented because changing resolution can alter disturbance boundaries and class proportions.

54. Temporal Alignment

Pre- and post-event images should be compared using appropriate seasonal and temporal alignment.

Otherwise normal seasonal vegetation changes may be incorrectly classified as disturbance.

55. Reference Labels / Ground Truth

Reference labels can come from curated datasets, interpreted satellite imagery, event records, or expert/manual interpretation.

No reference dataset should automatically be assumed to be perfect ground truth.

56. Validation Hierarchy

A practical validation hierarchy is:

dataset inspection → visual verification → baseline comparison → quantitative evaluation → geographically separated testing.

57. Experiment FD-01 — Data Inspection

Inspect a small number of forest areas using Landsat/Sentinel-2 imagery and available disturbance layers.

Record spatial resolution, dates, cloud conditions, forest condition, and obvious disturbance patterns.

58. Experiment FD-02 — Simple Spectral Change Baseline

Calculate pre/post spectral or index differences.

Measure whether obvious disturbances receive stronger change signals than stable forest.

59. Experiment FD-03 — Multi-Temporal Change Detection

Use multiple observations instead of only two dates.

Test whether persistent or abrupt changes can be separated from temporary spectral variation.

60. Experiment FD-04 — Sentinel-2 + Vegetation Indices

Evaluate whether Sentinel-2's finer spatial resolution and vegetation indices improve detection of smaller disturbances.

Compare results against the simpler baseline.

61. Experiment FD-05 — Multi-Source Machine Learning

Combine spectral, temporal, terrain, weather, and land-cover features.

Train a lightweight model such as Random Forest and compare it with the baseline.

62. Experiment FD-06 — Deep Learning / Segmentation

Only after simpler experiments should segmentation or deep learning be considered.

The goal is to determine whether additional complexity provides measurable improvement.

63. Experimental Comparison Matrix

Each experiment should record:

- Dataset
- Input features
- Spatial/temporal resolution
- Model
- Thresholds
- Precision
- Recall
- F1
- Area error
- Main failure cases

64. Research Decision Tree

If simple change detection performs well, document its strengths and limits.

If it fails under seasonal, cloud, or small-disturbance conditions, test multi-temporal and multi-source methods.

65. What Would NOT Be a Strong Contribution?

A generic statement such as “AI detects deforestation using satellite images” is not sufficient.

A strong research artifact needs a defined problem, baseline, measurable gap, experiment, and evidence.

66. What Could Become a Stronger Contribution?

A stronger direction is:

observation-aware, multi-temporal, multi-source forest disturbance detection with uncertainty-aware interpretation.

This directly addresses practical limitations of single-source monitoring.

67. Possible Final Research Contribution Structure

The final work can be organised as:

1. Problem
2. Existing systems
3. Failure analysis
4. Proposed workflow
5. Dataset strategy
6. Experiments
7. Results
8. Limitations
9. Research gap
10. Future work

68. Reproducibility Requirements

Record dataset names, versions, acquisition dates, preprocessing, spatial resolution, thresholds, model parameters, and evaluation procedures.

69. GitHub Research Record

The repository should contain research notes, methodology, experiment descriptions, source references, and later results.

Commit messages should describe meaningful research progress.

70. Reproducibility Principle

Another researcher should be able to understand what data and processing produced a reported result.

Hidden manual decisions should be minimized and documented.

71. Current Scientific Understanding

Forest disturbance detection is well established, but reliable attribution and generalization remain challenging.

Long time series and multiple information sources can improve interpretation.

72. Current Research Gap Status

The practical gap selected for this project is not basic forest-change detection.

It is the reliable combination of multi-temporal observations and auxiliary context while explicitly handling observation limitations and uncertainty.

73. Research Questions Generated So Far

1. Can multi-temporal data reduce false disturbance detections?
2. Does Sentinel-2 improve detection of small disturbances?
3. Does contextual information improve attribution?
4. Can the method generalise to unseen regions?
5. Can observation quality be incorporated into confidence?

74. First Practical Dataset Strategy

Start with a small number of clearly documented forest-disturbance events.

Use manageable geographic areas before attempting global-scale analysis.

75. Forest Disturbance Research Workflow

AOI selection → data acquisition → quality filtering → temporal compositing → feature generation → disturbance detection → attribution/context → confidence → validation.

76. Immediate Coding Plan

Begin with data inspection and visualisation.

Do not start with a complex AI model before understanding the input data and baseline behaviour.

77. Coding Experiment FD-01

Create a small notebook/script that:

1. Loads selected imagery or prepared datasets.
2. Displays forest areas.
3. Compares pre/post observations.
4. Calculates basic indices.
5. Visualises detected change.

78. What to Learn From FD-01

The first experiment should reveal:

- Data availability
- Cloud problems
- Seasonal variation
- Spatial resolution effects
- Index behaviour
- Obvious false positives/negatives

79. Expected First Coding Folder Structure

forest-disturbance/
├── research-notes.md
├── methodology.md
├── experiments/
│   └── FD-01-data-inspection.md
├── notebooks/
├── data/
│   └── README.md
├── results/
│   └── README.md
└── references.md

80. First Milestone

Produce a working baseline showing forest areas and simple spectral/vegetation-index change.

81. Second Milestone

Add multi-temporal observations and compare them against the two-date baseline.

82. Third Milestone

Add contextual information and evaluate whether it reduces major false detections or improves attribution.

83. Fourth Milestone

Evaluate the final candidate workflow on a geographically separate test area.

84. Final Scientific Goal

The objective is not simply to produce a forest-loss map.

The goal is to develop a transparent workflow that identifies likely forest disturbance, explains supporting evidence, represents uncertainty, and can be extended to multiple regions.

85. Key Scientific References

1. Hansen, M. C., et al. (2013). High-Resolution Global Maps of 21st-Century Forest Cover Change. Science, 342(6160), 850–853. DOI: 10.1126/science.1244693.

2. Kennedy, R. E., Yang, Z., & Cohen, W. B. (2010). Detecting Trends in Forest Disturbance and Recovery Using Yearly Landsat Time Series: 1. LandTrendr—Temporal Segmentation Algorithms. Remote Sensing of Environment, 114(12), 2897–2910. DOI: 10.1016/j.rse.2010.07.008.

3. Stahl, A. T., et al. (2023). Automated Attribution of Forest Disturbance Types from Remote Sensing Data: A Synthesis. Remote Sensing of Environment, 285, 113416. DOI: 10.1016/j.rse.2022.113416.

4. Hirschmugl, M., et al. (2017). Methods for Mapping Forest Disturbance and Degradation from Optical Earth Observation Data: A Review.

86. Official Data Sources

- Global Forest Watch — https://www.globalforestwatch.org/
- USGS Landsat Missions — https://www.usgs.gov/landsat-missions
- Copernicus Sentinel-2 — https://www.esa.int/Applications/Observing_the_Earth/Copernicus/Sentinel-2
- Copernicus Data Space Ecosystem — https://dataspace.copernicus.eu/

87. Research Integrity Rules

Do not claim that tree-cover loss automatically means deforestation.

Do not describe predictions as confirmed events without suitable validation.

Report limitations, uncertainty, dataset definitions, and failure cases.

88. Research Status

Status: Research and baseline-design phase.

The literature and data sources have been identified. Coding and controlled experiments are the next stage.

89. Immediate Next Step

Complete Experiment FD-01 — Data Inspection, document the observations, and then implement the simple spectral-change baseline.

90. Final Note

The forest-disturbance module should remain scientifically connected to the overall multi-hazard agent.

The final agent should select suitable data and analysis steps based on the hazard and observation conditions instead of applying one fixed model to every environmental event.