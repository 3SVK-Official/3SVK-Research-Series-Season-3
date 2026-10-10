# Flood Research Notes

## 1. Purpose

This document records the scientific and technical research conducted
for the flood-monitoring component of the:

> Satellite-Based Multi-Hazard Intelligence System

The purpose of this document is to understand:

- How satellite-based flood detection works.
- What existing operational systems already provide.
- Which datasets are available.
- Which algorithms have been studied.
- What limitations have been documented.
- Where satellite flood detection fails or becomes uncertain.
- How flood observations can be combined with contextual information.
- How the team can design reproducible experiments.
- Which research questions may lead to a measurable contribution.

This document is a research record.

It does not assume that a particular method is novel or superior.

Any final research contribution must be supported by experimental
evidence.

---

# 2. Research Scope

The flood component focuses primarily on:

> Satellite-based flood inundation detection and assessment.

The main observation source is:

- Sentinel-1 SAR

Potential supporting observations include:

- Sentinel-2 optical imagery
- GPM IMERG precipitation
- Digital Elevation Models
- Permanent-water datasets
- Land-cover information
- Historical flood observations

The project distinguishes between:

### Flood Risk / Forecasting

Estimating the possibility of flooding before or during an event.

### Flood Detection

Identifying areas that are currently or recently inundated.

### Flood Extent Mapping

Producing a spatial map of the inundated area.

### Flood Impact Assessment

Estimating consequences such as affected population,
infrastructure or land.

These are different scientific tasks.

Our initial research focus is:

> Flood inundation detection and mapping.

---

# 3. Central Flood Research Question

The initial flood research question is:

> Can complementary satellite and environmental observations reduce
> missed detections and false alarms in flood inundation mapping
> compared with relying primarily on a single satellite observation?

This question is intentionally broad at the beginning.

The final research question will be narrowed after:

1. Literature review.
2. Dataset investigation.
3. Baseline implementation.
4. Error analysis.
5. Controlled experiments.

---

# 4. Initial Hypothesis

The initial hypothesis is:

> Complementary observations such as terrain, rainfall or optical
> information may help resolve selected ambiguities in Sentinel-1
> flood detection, but the benefit will depend on the flood
> environment and observation conditions.

This is a hypothesis.

It is not a confirmed result.

The project must test it experimentally.

---

# 5. Why Sentinel-1 Is Important for Flood Monitoring

Sentinel-1 uses Synthetic Aperture Radar (SAR).

SAR is an active sensing system that transmits radar energy toward the
Earth and measures the returned signal.

The returned radar signal is influenced by characteristics of the
surface.

Floodwater can produce a different radar response from surrounding
land under suitable conditions.

This makes SAR useful for detecting inundated areas.

An important advantage is that Sentinel-1 can acquire imagery during
both day and night and is much less affected by cloud cover than
optical imagery.

This makes SAR particularly valuable during severe weather when
clouds may prevent useful optical observations.

---

# 6. Basic Flood Detection Concept

A simplified SAR flood-mapping concept is:

```text
Pre-flood SAR image
        +
Post-flood SAR image
        ↓
Backscatter analysis
        ↓
Change detection
        ↓
Candidate water pixels
        ↓
Permanent-water filtering
        ↓
Terrain / land-cover filtering
        ↓
Flood mask
        ↓
Validation