# F-02 — Sentinel-1 VV Threshold Flood Detection Baseline

## 1. Experiment Overview

**Experiment ID:** F-02  
**Track:** Flood  
**Dataset:** Sen1Floods11  
**Input:** Sentinel-1 SAR VV polarization  
**Task:** Pixel-level flood inundation detection  
**Experiment Type:** Baseline threshold method  
**Status:** Completed

---

## 2. Objective

The objective of F-02 was to establish a simple and reproducible
baseline for flood inundation detection using Sentinel-1 SAR VV
backscatter.

The experiment uses a single VV backscatter threshold to classify
pixels as either flooded or non-flooded.

This baseline provides a measurable reference for later experiments
that use additional information or more advanced models.

---

## 3. Research Motivation

A research workflow should establish a simple baseline before introducing
more complex machine-learning or multi-source methods.

For Sentinel-1 SAR imagery, water surfaces can produce relatively low
radar backscatter under many conditions. Therefore, a simple threshold
on VV backscatter provides a useful starting point for understanding
how well a single SAR observation can separate flooded and non-flooded
pixels.

The purpose of this experiment is not to claim that a VV threshold is
an optimal flood detector.

Instead, it establishes a reproducible reference against which later
methods can be compared.

---

## 4. Dataset

The experiment uses the **Sen1Floods11** dataset.

The dataset contains Sentinel-1 SAR imagery together with manually
labelled flood masks.

The available dataset splits used in the experiment were:

| Split | Samples |
|---|---:|
| Training | 251 |
| Validation | 88 |
| Test | 89 |
| Bolivia | 14 |

The training, validation and test split CSV files were used to identify
the corresponding Sentinel-1 image and label pairs.

The experiment used the training/validation/test structure rather than
randomly mixing pixels between the splits.

---

## 5. Input Data

Each selected Sentinel-1 sample contains:

- VV polarization
- VH polarization
- A corresponding flood label

For F-02, only the **VV polarization** was used for prediction.

The flood label was converted into a binary mask:

```text
0 → Non-flooded
1 → Flooded