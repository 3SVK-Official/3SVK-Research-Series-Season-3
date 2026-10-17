# Existing Systems and Research Landscape

This document records existing satellite-based systems relevant to the
project.

The purpose is to understand what already exists before defining the
research contribution.

---

## 1. Copernicus Global Flood Monitoring

### Organization

Copernicus Emergency Management Service (CEMS)

### Purpose

Global Flood Monitoring (GFM) provides continuous monitoring of
flooding worldwide using incoming Sentinel-1 SAR observations.

### Satellite / Data

- Sentinel-1 SAR
- Level-1 IW GRDH acquisitions
- Backscatter-derived information

### Method

The operational GFM implementation preprocesses Sentinel-1 SAR
observations and applies multiple automated flood-mapping algorithms.
An ensemble approach combines the outputs of the individual flood
algorithms.

### Output

The GFM product provides flood-related output layers including:

- Observed flood extent
- Reference water mask
- Exclusion mask
- Likelihood information

### Importance to Our Research

GFM provides an important baseline for understanding operational
satellite-based flood monitoring.

### Research Questions

We need to investigate:

- Under what conditions does Sentinel-1 flood mapping perform well?
- Where can flood detections fail?
- How do terrain, land cover and urban environments affect results?
- Can contextual datasets such as rainfall or elevation provide
  useful additional information?

### Source

Copernicus Data Space documentation on Global Flood Monitoring.

---

## 2. Global Forest Watch Integrated Disturbance Alerts

### Organization

Global Forest Watch / World Resources Institute and contributing
research institutions

### Purpose

Global Forest Watch provides near-real-time information about
vegetation and forest disturbances.

### Data Sources

The integrated disturbance alerts layer currently combines multiple
alert systems, including:

- GLAD-L
- GLAD-S2
- RADD
- DIST-ALERT

These systems use optical and radar observations from satellites
including Landsat and Sentinel-1/Sentinel-2.

### Important Characteristics

GLAD-L uses Landsat imagery at 30 m resolution.

GLAD-S2 uses Sentinel-2 imagery at 10 m resolution.

RADD uses Sentinel-1 radar data and can detect forest changes through
cloud cover that can limit optical observations.

DIST-ALERT combines Landsat and Sentinel-2 observations to detect
vegetation disturbances.

### Importance to Our Research

This is especially important because it demonstrates that
multi-source observations are already being used operationally for
forest disturbance monitoring.

Therefore, our project must not simply claim that combining optical
and radar data is itself a novel idea.

We need to identify a more specific research question or failure case
through literature review and experiments.

### Research Questions

We need to investigate:

- When do optical alerts fail?
- When does radar provide useful additional information?
- What causes false disturbance alerts?
- Can natural disturbances be distinguished from human-caused
  disturbances?
- Under what conditions does combining multiple alerts improve
  reliability?

### Source

Global Forest Watch, Integrated Disturbance Alerts documentation,
updated January 2026.

---

## 3. NASA FIRMS

### Organization

NASA Earth Science Data and Information System / LANCE

### Purpose

FIRMS provides active-fire and thermal-anomaly information from
satellite sensors.

### Main Satellite Products

- MODIS
- VIIRS
- Landsat OLI active-fire products

### VIIRS

VIIRS active-fire products are available at approximately 375 m
spatial resolution.

### Output

FIRMS provides active-fire or thermal-anomaly detections and
associated information such as location and detection confidence.

### Important Limitations

NASA states that satellite-derived active-fire and thermal-anomaly
detections have limited accuracy.

A detected thermal anomaly may originate from:

- Fire
- Hot smoke
- Agricultural activity
- Other hot sources

Cloud cover can also obscure active-fire detections.

The size of the satellite pixel does not mean that the entire pixel
area is burning.

### Importance to Our Research

FIRMS provides an important operational baseline for wildfire-related
satellite monitoring.

Our research must therefore investigate whether additional
information can reduce false detections or missed events rather than
simply creating another hotspot map.

### Research Questions

We need to investigate:

- Which fire events are missed?
- Which thermal anomalies are false positives?
- How do clouds affect detection?
- How does detection confidence relate to actual fire conditions?
- Can environmental or optical information improve assessment?

### Source

NASA FIRMS Active Fire Data and FIRMS documentation.

---

# Initial Comparison

| System | Hazard | Main Data | Main Output | Important Limitation / Research Question |
|---|---|---|---|---|
| Copernicus GFM | Flood | Sentinel-1 SAR | Flood extent | Investigate conditions causing missed/ambiguous flood detections |
| GFW Integrated Alerts | Forest disturbance | Landsat, Sentinel-1, Sentinel-2 | Disturbance alerts | Investigate false alerts and separation of natural vs human disturbance |
| NASA FIRMS | Wildfire | VIIRS, MODIS, Landsat | Active-fire / thermal anomalies | False thermal anomalies and cloud-obscured detections |

## Current Conclusion

Existing systems already provide substantial satellite-based monitoring
capabilities.

Therefore, the research contribution of this project cannot simply be
"using satellites for disaster detection."

The team must identify a specific measurable limitation and test a
well-defined hypothesis against an appropriate baseline.