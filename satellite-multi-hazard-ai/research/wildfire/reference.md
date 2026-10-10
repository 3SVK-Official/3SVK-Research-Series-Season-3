Wildfire References and Research Notes



1. Purpose

This document records the scientific and technical research conducted for the wildfire-monitoring component of the Satellite-Based Multi-Hazard Intelligence System.

The purpose is to understand satellite-based wildfire detection, active-fire monitoring, burned-area mapping, limitations, datasets, algorithms, evaluation methods, and possible research directions.

2. Wildfire Research Scope

The module focuses on detecting and monitoring wildfire activity using satellite and auxiliary data.

The scope includes active-fire detection, fire location, burned-area mapping, fire intensity indicators, fire impacts, and supporting environmental conditions.

3. Central Wildfire Research Question

The main research question is:

Can multi-source satellite and auxiliary data provide more reliable wildfire detection and interpretation than a single-source active-fire system?

4. Initial Wildfire Hypothesis

Thermal active-fire observations are useful for detecting ongoing fire activity, while optical imagery and contextual data can improve spatial interpretation and post-fire assessment.

A combination of these sources may reduce important detection and interpretation limitations.

5. Wildfire Detection vs Burned-Area Mapping

Active-fire detection identifies thermal anomalies associated with fire activity at the time of satellite observation.

Burned-area mapping identifies land affected by fire after or during the event.

These are related but different monitoring problems.

6. Why Satellite Remote Sensing Is Important

Wildfires can occur across large and inaccessible areas.

Satellite observations provide repeated regional or global coverage and can support rapid fire detection, burned-area mapping, and post-fire assessment.

7. Thermal Signature of Fire

Active fires produce strong thermal and infrared signals.

Satellite fire-detection algorithms use these signals to identify pixels that are unusually hot compared with their surroundings.

8. Active Fire Detection

Active-fire products provide information about locations where fire-related thermal anomalies were detected.

They are useful for near-real-time monitoring but do not necessarily represent the complete physical boundary of a fire.

9. NASA FIRMS

NASA's Fire Information for Resource Management System (FIRMS) provides near-real-time satellite-derived active-fire information.

FIRMS uses MODIS and VIIRS active-fire algorithms and distributes fire locations in accessible formats.

10. MODIS Active Fire

MODIS provides global active-fire observations from Terra and Aqua satellites.

Its long historical record makes it useful for studying fire activity at regional and global scales.

11. VIIRS Active Fire

VIIRS provides active-fire observations at approximately 375 m spatial resolution in the FIRMS global product.

Its finer spatial resolution compared with MODIS improves the detection of many smaller fire features.

12. Active-Fire Detection Is Not Fire Boundary Detection

An active-fire point or pixel indicates a detected thermal anomaly.

It should not automatically be interpreted as the exact perimeter or total area of the wildfire.

13. Fire Radiative Power

Fire Radiative Power (FRP) describes the rate of radiant energy emitted by actively burning fires.

FRP can provide information related to fire intensity and energy release and is available with several satellite active-fire products.

14. FIRMS Detection Limitations

FIRMS detections can be affected by cloud cover, smoke, sensor viewing geometry, fire size, fire temperature, vegetation, and satellite overpass timing.

Therefore, absence of a FIRMS detection does not necessarily prove absence of fire.

15. Small Fire Limitation

Small fires may occupy only a fraction of a satellite pixel.

Their thermal signal can therefore become mixed with the surrounding land surface and may not be detected reliably.

16. Cloud and Smoke Limitation

Clouds can block optical and thermal observations.

Dense smoke can also reduce the visibility or reliability of satellite observations depending on the sensor and fire conditions.

17. Satellite Overpass Timing

Polar-orbiting satellites observe an area only at specific times.

A fire can start, grow, or extinguish between observations.

18. Geostationary Satellite Advantage

Geostationary satellites can observe the same region much more frequently than polar-orbiting satellites.

This can support higher-frequency monitoring where suitable geostationary coverage exists.

19. False Positive Sources

Thermal anomalies can sometimes originate from sources other than wildfires.

Examples include agricultural burning, industrial heat sources, gas flares, and other hot surfaces.

20. Agricultural Burning

Agricultural fires can produce genuine active-fire signals.

A detection system therefore needs land-use context when distinguishing wildfire from managed burning.

21. Industrial Heat Sources

Industrial facilities and other persistent heat sources can create thermal anomalies.

Spatial context and temporal persistence can help reduce such false interpretations.

22. Forest Fire vs Grassland Fire

Different vegetation types produce different fire behaviour and satellite signatures.

A wildfire-monitoring system should therefore consider land-cover information when interpreting detections.

23. Burned-Area Mapping

Burned-area mapping estimates the spatial extent of land affected by fire.

It is generally more appropriate for assessing fire impact than using active-fire detections alone.

24. Landsat for Burned-Area Mapping

Landsat provides higher spatial-resolution observations suitable for detailed burned-area analysis.

USGS provides Landsat burned-area science products designed to identify burned areas across ecosystems.

25. Sentinel-2 for Wildfire Monitoring

Sentinel-2 multispectral imagery can support detailed analysis of vegetation and burned areas.

Its finer spatial resolution is useful for examining fire impacts that may be difficult to resolve using coarser active-fire products.

26. Optical vs Thermal Information

Thermal sensors are valuable for detecting active fire.

Optical sensors are particularly useful for vegetation condition, burn scars, and post-fire impact assessment.

26A. Sentinel-1 SAR as Supporting Wildfire Context

Sentinel-1 SAR can provide complementary information when optical observations are affected by cloud cover and can support analysis of vegetation and post-fire structural change.

SAR should not be treated as a direct replacement for thermal active-fire observations. Its role in the wildfire module should be tested experimentally, particularly for observation conditions where optical imagery is unavailable or limited.

This also keeps the overall project consistent with the multi-source research question: different sensors provide different evidence rather than one sensor being assumed to solve every wildfire-monitoring problem.

27. NBR — Normalized Burn Ratio

The Normalized Burn Ratio (NBR) is widely used for identifying burned areas and assessing burn severity.

It is calculated as:

NBR = (NIR − SWIR) / (NIR + SWIR)

USGS provides Landsat NBR products and documentation.

28. dNBR

A common fire-severity measure is dNBR, calculated from pre-fire and post-fire NBR values.

It is specifically useful for fire-related change and should not be treated as a universal index for every environmental disturbance.

29. NDVI in Wildfire Analysis

NDVI measures vegetation-related spectral response.

Comparing NDVI before and after a fire can help estimate vegetation impact, although it is not itself a direct fire-detection method.

30. NDMI in Wildfire Analysis

NDMI is related to vegetation moisture.

Changes in vegetation moisture can provide supporting information about pre-fire conditions and post-fire impacts.

31. Pre-Fire Conditions

Vegetation dryness, drought, temperature, and moisture can influence wildfire susceptibility.

These variables are useful for understanding fire risk but should not be confused with proof that a fire will occur.

32. Weather Context

Weather information such as temperature, wind, rainfall, and humidity can provide important context for wildfire monitoring.

It can help explain fire behaviour and environmental conditions.

33. Wind Information

Wind can influence fire spread and direction.

Therefore, wind data can provide useful contextual information when analysing fire progression.

34. Rainfall Information

Recent rainfall affects vegetation moisture and fuel conditions.

Long periods of low rainfall may indicate increased dryness, but rainfall alone cannot predict an individual wildfire with certainty.

35. Vegetation and Fuel Conditions

Vegetation density and dryness influence available combustible material.

Land-cover and vegetation-condition datasets can therefore support wildfire-risk and fire-impact analysis.

36. Fire Risk vs Fire Detection

Fire-risk prediction estimates the likelihood or susceptibility of future fire.

Fire detection identifies evidence of an ongoing or recently observed event.

These should remain separate outputs in the system.

37. Fire Detection vs Fire Prediction

A model that detects an active fire should not automatically be described as predicting future wildfire occurrence.

Prediction requires historical fire events and explanatory environmental variables.

38. Fire Spread Monitoring

Repeated observations can be used to analyse changes in fire location and affected area.

However, satellite revisit intervals can leave gaps in the observed progression.

39. Burned-Area Time Delay

Burned-area products are often generated after sufficient observations become available.

Therefore, burned-area mapping should not be treated as equivalent to near-real-time active-fire detection.

40. Multi-Temporal Fire Analysis

Using observations from multiple dates can help distinguish temporary thermal anomalies from persistent fire activity.

It can also support pre-fire, active-fire, and post-fire analysis.

41. Observation Failure vs Algorithmic Failure

A missed fire may result from cloud cover, small fire size, observation timing, smoke, or sensor limitations.

It is important to distinguish these observation failures from genuine algorithmic failures.

42. Candidate Multi-Source Workflow

A practical wildfire workflow can combine:

FIRMS active fire → Sentinel-2/Landsat impact analysis → weather context → land-cover context → confidence assessment.

43. Candidate Research Direction A — Active-Fire Reliability

The system can estimate the reliability of an active-fire detection using sensor, observation, land-cover, and environmental context.

44. Candidate Research Direction B — Active Fire + Burned Area

Combine near-real-time active-fire detections with higher-resolution post-fire burned-area mapping.

This provides both event detection and impact assessment.

45. Candidate Research Direction C — Multi-Temporal Fire Confirmation

Repeated active-fire observations can be used to increase confidence when multiple observations support the same event.

46. Candidate Research Direction D — Fire Attribution

The system can distinguish likely wildfire activity from agricultural burning or other thermal anomalies using land-use, temporal, and spatial context.

47. Candidate Research Direction E — Fire Impact Assessment

After detection, the agent can estimate affected vegetation using NBR, dNBR, NDVI, and other change indicators.

48. Candidate Research Direction F — Fire Risk Context

Weather, vegetation moisture, drought, and land-cover information can be used to describe conditions surrounding a detected or potential fire event.

49. What Would Count as a Meaningful Result?

A meaningful result should demonstrate measurable improvement over a simple active-fire or spectral-change baseline.

The improvement should be evaluated using defined datasets and metrics.

50. Event-Level Evaluation

Wildfire events should ideally be evaluated as events rather than only as individual pixels.

Useful event-level measures include detection rate, false alarms, detection delay, and spatial overlap.

51. Spatial Evaluation

For burned-area mapping, spatial metrics such as IoU, precision, recall, and F1-score can be used when reference polygons or raster labels are available.

52. Detection Delay

For near-real-time wildfire monitoring, the time between actual event occurrence and satellite detection is an important metric.

Lower detection delay can improve practical usefulness.

53. Fire Area Error

Predicted burned area can be compared with a reference burned-area estimate.

Area error provides information that pixel accuracy alone may not reveal.

54. False Alarm Rate

A useful wildfire-monitoring system should minimise false detections from agricultural fires, industrial heat, and other thermal anomalies.

55. Small-Fire Evaluation

Performance should be evaluated separately for small, medium, and large fire events.

This helps determine whether the system is biased toward larger fires.

56. Regional Evaluation

A model should ideally be tested across different ecosystems and geographic regions.

This helps identify whether it generalises beyond the area used for development.

57. Data Leakage

Fire observations from the same event should not unintentionally appear in both training and test sets.

Spatial and temporal leakage can produce unrealistically high performance.

58. Class Imbalance

Non-fire pixels can greatly outnumber active-fire pixels.

Evaluation should therefore use suitable metrics rather than relying only on overall accuracy.

59. Reference Data Limitations

Satellite fire products and manually interpreted fire boundaries can contain uncertainty.

Reference data should therefore be treated as observations with known limitations rather than perfect ground truth.

60. Temporal Alignment

Pre-fire, active-fire, and post-fire observations must be correctly aligned.

Poor temporal alignment can create misleading change measurements.

61. Spatial Resolution Differences

FIRMS, Landsat, and Sentinel-2 operate at different spatial resolutions.

Combining them requires careful resampling and documentation.

62. Sensor Differences

Different sensors observe different wavelengths, spatial resolutions, revisit frequencies, and viewing conditions.

A multi-source system must account for these differences.

63. Baseline Model 1 — FIRMS Only

Use active-fire detections from FIRMS as the simplest operational baseline.

Measure detection coverage and false-alarm behaviour.

64. Baseline Model 2 — Spectral Change

Use pre-fire and post-fire optical indices such as NBR or NDVI to detect fire-related change.

65. Baseline Model 3 — Threshold-Based Detection

Apply a defined threshold to thermal or spectral features.

This provides a transparent baseline for comparison.

66. Baseline Model 4 — Machine Learning

Combine active-fire, spectral, land-cover, weather, and temporal features using a model such as Random Forest.

67. Advanced Model — Deep Learning

Deep learning can be considered if sufficient labelled imagery is available.

It should only be introduced after simpler methods have been evaluated.

68. Proposed Experimental Ladder

The experiments should progress as:

FIRMS baseline → optical change baseline → multi-temporal analysis → multi-source ML → advanced model.

This keeps the research scientifically controlled.

69. Experiment WF-01 — FIRMS Data Inspection

Inspect active-fire detections for selected known wildfire events.

Record detection dates, coordinates, confidence information where available, and surrounding land cover.

70. Experiment WF-02 — FIRMS Detection Reliability

Compare FIRMS detections against known fire events and visually inspect false positives and missed detections.

Document the environmental conditions associated with failures.

71. Experiment WF-03 — NBR/dNBR Burned-Area Baseline

Calculate pre-fire and post-fire NBR and evaluate dNBR for selected fire events.

Compare the detected burned region with reference information.

72. Experiment WF-04 — Sentinel-2 Fire Impact

Use Sentinel-2 imagery to examine vegetation change around detected active-fire locations.

Evaluate whether finer spatial information improves burned-area interpretation.

73. Experiment WF-05 — Multi-Source Machine Learning

Combine:

- FIRMS features
- Spectral indices
- Weather
- Land cover
- Temporal features

and evaluate whether multi-source information improves detection or classification.

74. Experiment WF-06 — Event-Level Generalization

Develop the approach using selected wildfire events and evaluate it on geographically separate events.

This tests whether the method generalises beyond individual fires.

75. Candidate Feature Set

Possible features include:

- FIRMS fire confidence
- FRP
- Latitude/longitude
- NIR
- SWIR
- NBR
- dNBR
- NDVI
- NDMI
- Land-cover type
- Temperature
- Rainfall
- Wind
- Soil moisture
- Terrain

76. Confidence-Aware Output

The agent should avoid presenting every fire detection as certain.

A useful output can include:

Detected / Likely / Uncertain / Not Confirmed

with supporting evidence.

77. Observation Quality Score

A quality score can consider cloud cover, sensor availability, observation timing, and spatial resolution.

This can help the agent determine whether additional data are required.

78. Proposed Wildfire Agent Workflow

Fire-related signal
       ↓
Check observation quality
       ↓
Active-fire data search
       ↓
Cross-check with optical imagery
       ↓
Check land-cover and weather context
       ↓
Estimate fire confidence
       ↓
If confirmed → map/assess impact
       ↓
If uncertain → request additional observations

79. Reproducibility Requirements

Record:

- Dataset
- Sensor
- Acquisition date
- Spatial resolution
- Preprocessing
- Cloud filtering
- Indices
- Thresholds
- Model parameters
- Evaluation metrics

80. GitHub Research Record

The repository should contain research notes, methodology, experiments, references, code, and later results.

Each major experiment should have a separate documented record.

81. What Would NOT Be a Strong Contribution?

A generic statement such as “AI detects wildfires using satellite images” is not enough.

The work needs a measurable research problem and comparison against a baseline.

Research Novelty Boundary

Multi-source wildfire monitoring is already represented in scientific and operational work. Therefore, simply combining FIRMS, optical imagery, weather, and land-cover data must not be presented as novel by itself.

The research contribution must come from a measurable problem, a controlled baseline comparison, a documented failure mode, and evidence that the proposed method addresses that failure.

82. What Could Become a Stronger Contribution?

A candidate stronger direction is:

observation-aware multi-source wildfire detection and impact assessment using active-fire, optical, and environmental context.

This is a candidate research direction, not the final research contribution. The final gap and contribution must be established after baseline experiments and error analysis.

83. Possible Final Research Contribution

If experiments support it, a final system could provide:

1. Fire detection
2. Confidence estimation
3. Fire-location mapping
4. Burned-area estimation
5. Fire-impact assessment
6. Supporting environmental context
7. Uncertainty reporting

84. First Practical Dataset Strategy

Start with a small set of clearly documented wildfire events.

Select events with usable FIRMS and optical observations before expanding the dataset.

85. Wildfire Research Workflow

Event selection → FIRMS detection → observation-quality check → optical imagery → preprocessing → active-fire validation → burned-area analysis → contextual analysis → confidence → evaluation.

86. Immediate Coding Plan

Begin with FIRMS data inspection and visualisation.

Then add a simple NBR/dNBR or spectral-change analysis for selected fire events.

87. First Milestone

Produce a reproducible baseline showing:

- Active-fire locations
- Selected wildfire events
- Optical imagery
- Basic fire-impact indicators

88. Second Milestone

Add multi-temporal and multi-source information.

Evaluate whether additional information reduces false alarms or improves fire-impact mapping.

89. Research Status and Immediate Next Step

Status: Research and baseline-design phase.

The immediate next step is Experiment WF-01 — FIRMS Data Inspection, followed by the simple burned-area/NBR baseline.

90. Final Note

The wildfire module should remain connected to the overall multi-hazard agent.

The agent should distinguish between active fire detection, burned-area mapping, fire-impact assessment, and fire-risk context, rather than treating all four as the same task.

---

Key Scientific References

1. Wooster, M. J., et al. (2021). Satellite remote sensing of active fires: History and current status, applications and future requirements. Remote Sensing of Environment, 267, 112694. DOI: 10.1016/j.rse.2021.112694.

2. Chuvieco, E., et al. (2019). Historical background and current developments for mapping burned area from satellite Earth observation. Remote Sensing of Environment, 225, 45–64. DOI: 10.1016/j.rse.2019.02.013.

3. Mouillot, F., et al. (2014). Ten years of global burned area products from spaceborne remote sensing—A review: Analysis of user needs and recommendations for future developments. International Journal of Applied Earth Observation and Geoinformation, 26, 64–79. DOI: 10.1016/j.jag.2013.05.014.

4. Advancements in remote sensing for active fire detection: A review of datasets and methods. Science of the Total Environment, 943, 173273, 2024. DOI: 10.1016/j.scitotenv.2024.173273.

5. Remote sensing for wildfire monitoring: Insights into burned area, emissions, and fire dynamics. One Earth, 7(6), 1022–1028, 2024. DOI: 10.1016/j.oneear.2024.05.014.

6. Trends and applications in wildfire burned area mapping: Remote sensing data, cloud geoprocessing platforms, and emerging algorithms. 2024. DOI: 10.1016/j.geomat.2024.100008.

Official Data Sources

- NASA FIRMS — https://firms.modaps.eosdis.nasa.gov/
- NASA Earthdata FIRMS — https://earthdata.nasa.gov/
- USGS Landsat Missions — https://www.usgs.gov/landsat-missions
- USGS Landsat NBR — https://www.usgs.gov/landsat-missions/landsat-normalized-burn-ratio
- USGS Landsat Burned Area — https://www.usgs.gov/landsat-missions/landsat-burned-area-science-products
- Copernicus Sentinel-2 — https://www.esa.int/Applications/Observing_the_Earth/Copernicus/Sentinel-2
- Copernicus Data Space — https://dataspace.copernicus.eu/

Research Integrity Rules

- Do not treat every FIRMS detection as a confirmed wildfire.
- Do not treat an active-fire point as the exact fire boundary.
- Do not treat burned-area estimates as perfect ground truth.
- Clearly distinguish detection, impact assessment, risk, and prediction.
- Report cloud, smoke, spatial-resolution, temporal, and sensor limitations.
- Record all preprocessing, thresholds, datasets, and evaluation procedures.
- Report uncertainty instead of presenting uncertain detections as confirmed events.]