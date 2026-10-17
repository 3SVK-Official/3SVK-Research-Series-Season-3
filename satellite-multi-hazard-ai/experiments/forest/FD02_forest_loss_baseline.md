  # FD02 — Forest Loss Baseline Experiment

## 1. Experiment Overview

* **Experiment ID:** FD02
* **Track:** Forest Disturbance Monitoring
* **Experiment type:** Rule-based baseline and threshold-sensitivity analysis
* **Dataset:** Hansen Global Forest Change v1.11 (2000–2023)
* **Notebook:** `notebooks/forest/FD02_forest_loss_baseline.ipynb`
* **Status:** Baseline implementation prepared; results and quality checks must be confirmed from the completed notebook run.

## 2. Objective

The objective of FD02 is to establish a simple, reproducible baseline for examining the relationship between estimated tree-canopy cover and recorded historical tree-cover loss.

The experiment compares three canopy-cover thresholds: 10%, 30%, and 50%. It investigates how the number of sampled pixels with recorded loss changes when different minimum canopy-cover thresholds are applied.

This is a descriptive baseline, not a trained machine-learning model.

## 3. Dataset

The experiment uses two raster layers from the Hansen Global Forest Change dataset:

| Layer           | Description                                                                                                                        |
| --------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| `treecover2000` | Estimated percentage of tree-canopy cover in the year 2000                                                                         |
| `lossyear`      | Encoded year of detected tree-cover loss; values 1–23 correspond to 2001–2023, and 0 indicates no recorded loss during that period |

**Official dataset reference:**
https://storage.googleapis.com/earthenginepartners-hansen/GFC-2023-v1.11/download.html

### Previous inspection context

FD01 inspected downsampled arrays of 1,000 × 1,000 pixels and reported:

* Valid tree-cover sample pixels: 1,000,000
* Valid loss-year sample pixels: 1,000,000
* Pixels with non-zero loss-year values: 3,440
* Pixels with tree cover of at least 30%: 36,224

These figures are from FD01 and must not be treated as FD02 results. FD02 uses a separate sampling configuration and must report its own measured counts.

## 4. Methodology

The planned workflow is:

1. Locate or download the required raster layers.
2. Check that the two rasters have matching coordinate reference systems, dimensions, transforms, and bounds.
3. Read the rasters on matching grids and create a valid-pixel mask.
4. Identify pixels with a recorded loss year (`lossyear > 0`).
5. Apply canopy-cover thresholds of 10%, 30%, and 50%.
6. Count canopy-qualified pixels and pixels that satisfy both the canopy threshold and recorded-loss condition.
7. Calculate the proportion of recorded-loss pixels that satisfy each threshold.
8. Save the results table, visualizations, and experiment summary.

### Baseline rule

For canopy threshold \(T\), a pixel is flagged when:

`treecover2000 >= T AND lossyear > 0`

The rule is applied to valid sampled pixels only.

## 5. Experimental Results

**Complete this section using the actual output from `FD02_threshold_sensitivity.csv`. Do not copy the FD01 values into this table.**

| Canopy threshold | Canopy-qualified pixels | Recorded-loss pixels passing threshold | Share of recorded-loss pixels passing threshold |
| ---------------: | ----------------------: | -------------------------------------: | ----------------------------------------------: |
|              10% | Pending notebook output |                Pending notebook output |                         Pending notebook output |
|              30% | Pending notebook output |                Pending notebook output |                         Pending notebook output |
|              50% | Pending notebook output |                Pending notebook output |                         Pending notebook output |

Other required measurements:

* Sample dimensions: Pending notebook output
* Valid sampled pixels: Pending notebook output
* Total sampled pixels with non-zero recorded loss: Pending notebook output
* Spatial-alignment check: Pending confirmation

## 6. Expected Output Artifacts

The notebook is designed to generate the following files under its configured results directory:

* `FD02_threshold_sensitivity.csv`
* `FD02_threshold_sensitivity.png`
* `FD02_summary.txt`
* `FD02_baseline_visualization.png`
* `FD02_30pct_baseline_map.png`
* `FD02_conclusion.md`

Verify that each file exists before marking the experiment run as complete.

## 7. Interpretation

The threshold-sensitivity analysis describes how the selected canopy-cover condition changes the number of pixels associated with recorded tree-cover loss.

A higher threshold may select fewer pixels, but the actual relationship must be established from the measured output. The threshold comparison alone does not establish whether the rule detects forest disturbance accurately.

The `lossyear` layer is part of the same dataset used in the analysis. It is therefore not independent ground truth for validating a detection model.

## 8. Limitations

* The experiment uses downsampled raster data.
* Pixel counts are not direct estimates of hectares or square kilometres.
* Matching array dimensions alone does not guarantee spatial alignment; metadata checks are required.
* The canopy thresholds are exploratory and are not universal definitions of forest.
* Recorded tree-cover loss does not necessarily mean permanent deforestation.
* The experiment does not establish the cause or legality of tree-cover loss.
* No independent reference dataset or ground-truth validation has been used.
* No precision, recall, F1-score, or other detection-performance metric has been established.
* This baseline does not predict future forest loss.

## 9. Conclusion

FD02 implements a simple rule-based baseline for examining historical tree-cover loss under different canopy-cover thresholds. Its purpose is to establish a reproducible starting point for later forest-disturbance research.

The final findings must be completed from the actual threshold-sensitivity results and after confirming the raster quality checks. No claim of improved detection, model accuracy, or independent validation is justified by this experiment alone.

**Final status:** Results pending verification from the completed notebook run.
