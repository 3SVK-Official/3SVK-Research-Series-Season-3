# FD03 — Spatial Forest-Loss Analysis

## 1. Experiment Overview

**Experiment ID:** FD03
**Experiment name:** Spatial Forest-Loss Analysis
**Track:** Forest Disturbance Monitoring
**Dataset:** Hansen Global Forest Change v1.11
**Study tile:** `20N_080E`
**Notebook:** `notebooks/forest/FD03_spatial_loss_analysis.ipynb`
**Status:** Implementation prepared; results must be verified from notebook outputs.

## 2. Objective

The objective of FD03 is to examine the spatial distribution of recorded tree-cover loss in the selected Hansen Global Forest Change tile.

The experiment investigates:

1. How many spatially connected recorded-loss patches occur in the sampled raster.
2. How patch sizes vary between small and large connected regions.
3. How the distribution changes when recorded loss is restricted to areas with at least 30% tree cover in the year 2000.
4. How the number of recorded-loss pixels varies by year from 2001 to 2023.
5. How different exploratory canopy-cover thresholds affect the spatial patch statistics.

This experiment extends FD01 data inspection and FD02 threshold sensitivity analysis. It is a descriptive spatial analysis, not a trained machine-learning model.

## 3. Dataset and Input Layers

The experiment uses two raster layers from Hansen Global Forest Change v1.11.

| Layer           | Purpose                                                                             |
| --------------- | ----------------------------------------------------------------------------------- |
| `treecover2000` | Represents estimated tree canopy cover in the year 2000, expressed as a percentage. |
| `lossyear`      | Represents the recorded year of tree-cover loss during 2001–2023.                   |

Official dataset source:

https://storage.googleapis.com/earthenginepartners-hansen/GFC-2023-v1.11/download.html

The selected `20N_080E` tile covers a broad geographic area. It must not be interpreted as representing only Andhra Pradesh or any single administrative region.

### Interpretation of the loss-year layer

* Values `1–23` correspond to recorded loss years from 2001–2023.
* Value `0` means no loss year is recorded for that pixel during the dataset period.
* A recorded tree-cover-loss pixel does not, by itself, prove illegal logging, permanent deforestation, or human-caused disturbance.

## 4. Research Questions

**RQ1:** What are the sizes and counts of connected recorded-loss patches in the sampled raster?

**RQ2:** How does restricting recorded loss to pixels with at least 30% baseline tree cover change the patch distribution?

**RQ3:** How does recorded tree-cover loss vary across years in the dataset?

**RQ4:** How sensitive are patch statistics to exploratory canopy-cover thresholds of 10%, 30%, and 50%?

These questions describe the dataset and test sensitivity to analysis choices. They do not establish the real-world cause of each disturbance.

## 5. Methodology

### Step 1 — Input discovery and download

The notebook locates the two required raster files or downloads them from the official Hansen dataset source when they are missing.

### Step 2 — Spatial alignment checks

The notebook compares the input rasters' coordinate reference systems, dimensions, and spatial transforms.

The analysis should stop if the rasters are not spatially aligned. Matching array shapes alone is insufficient to establish geographic alignment.

### Step 3 — Raster sampling and validity checks

The rasters are read at a reduced resolution of up to 2000 × 2000 pixels using nearest-neighbour resampling.

Values are checked against the expected ranges:

* Tree cover: 0–100.
* Loss year: 0–23.

The resulting statistics describe the sampled raster, not necessarily the full-resolution pixel counts.

### Step 4 — Recorded-loss masks

Two masks are compared:

* **All recorded loss:** valid pixels where `lossyear > 0`.
* **Recorded loss with baseline canopy cover ≥30%:** valid pixels where `lossyear > 0` and `treecover2000 >= 30`.

The 30% threshold is an exploratory analytical choice, not a universal definition of forest.

### Step 5 — Connected-patch analysis

Connected components are identified using 8-neighbour connectivity. Pixels touching horizontally, vertically, or diagonally are treated as connected.

For each mask, the notebook calculates:

* Number of connected patches.
* Total pixels belonging to recorded-loss patches.
* Mean patch size.
* Median patch size.
* Largest patch size.
* Number of single-pixel patches.
* Number of patches containing 2–10 pixels.
* Number of patches containing more than 10 pixels.

Patch size is measured in sampled pixels. It should not be reported as an area in hectares or square kilometres without an appropriate geospatial area calculation.

### Step 6 — Patch-size visualization

The notebook creates a patch-size distribution plot to compare the two masks and examine whether the sampled loss pattern is dominated by small or large connected patches.

### Step 7 — Spatial visualization

Sampled spatial maps are generated to compare the baseline canopy layer, recorded-loss layer, and canopy-filtered loss.

These visualizations support exploratory interpretation; they do not independently validate the mapped loss.

### Step 8 — Year-wise analysis

The notebook counts recorded-loss pixels for each year from 2001 through 2023 and separately counts pixels meeting the 30% baseline canopy threshold.

The counts are based on the sampled raster. They should not be interpreted as full-resolution national or global forest-loss estimates.

### Step 9 — Threshold comparison

Patch statistics are compared using exploratory canopy-cover thresholds of 10%, 30%, and 50%.

This analysis examines how a threshold choice changes the spatial pattern. It does not identify one threshold as universally correct.

## 6. Results

**Important:** Populate this section after running the notebook and checking the generated CSV files and plots. Do not use FD01 counts as FD03 results.

### 6.1 Connected-patch statistics

Source file: `FD03_patch_summary.csv`

| Metric                        |    All recorded loss | Recorded loss with canopy ≥30% |
| ----------------------------- | -------------------: | -----------------------------: |
| Number of patches             | Pending verification |           Pending verification |
| Total patch pixels            | Pending verification |           Pending verification |
| Mean patch size               | Pending verification |           Pending verification |
| Median patch size             | Pending verification |           Pending verification |
| Largest patch                 | Pending verification |           Pending verification |
| Single-pixel patches          | Pending verification |           Pending verification |
| Patches of 2–10 pixels        | Pending verification |           Pending verification |
| Patches larger than 10 pixels | Pending verification |           Pending verification |

### 6.2 Year-wise recorded loss

Source file: `FD03_loss_by_year.csv`

The year-wise counts must be examined to identify the years with the largest and smallest recorded-loss pixel counts in the sampled raster.

No trend or peak year should be claimed until the actual output is reviewed.

### 6.3 Threshold comparison

Source file: `FD03_threshold_patch_comparison.csv`

The 10%, 30%, and 50% threshold results should be compared to determine how canopy filtering affects:

* The number of connected patches.
* The total number of retained loss pixels.
* The typical patch size.
* The largest connected patch.

A change in patch statistics demonstrates sensitivity to the chosen threshold; it does not prove that one threshold provides more accurate forest monitoring.

### 6.4 Visual inspection

The following figures are generated for interpretation:

* `FD03_patch_size_distribution.png`
* `FD03_sampled_spatial_maps.png`
* `FD03_loss_by_year.png`

The figures should be inspected alongside the CSV results before writing final findings.

## 7. Output Files

The notebook is designed to generate the following artifacts in the results directory:

| File                                  | Purpose                                                 |
| ------------------------------------- | ------------------------------------------------------- |
| `FD03_patch_summary.csv`              | Connected-patch statistics for the two principal masks. |
| `FD03_patch_size_distribution.png`    | Comparison of patch-size distributions.                 |
| `FD03_sampled_spatial_maps.png`       | Spatial visualization of the sampled raster layers.     |
| `FD03_loss_by_year.csv`               | Year-wise recorded-loss pixel counts.                   |
| `FD03_loss_by_year.png`               | Visualization of year-wise loss counts.                 |
| `FD03_threshold_patch_comparison.csv` | Patch statistics for the 10%, 30%, and 50% thresholds.  |
| `FD03_summary.md`                     | Automatically generated experiment summary.             |
| `FD03_output_verification.csv`        | Verification of expected output files.                  |

The presence and successful generation of these files must be confirmed from the notebook before marking the experiment complete.

## 8. Limitations

1. **Reduced resolution:** The spatial analysis uses a downsampled raster, so small patches and detailed boundaries may be lost or altered.
2. **Connected-patch definition:** Eight-neighbour connectivity can combine diagonally touching pixels into one patch. Different connectivity rules may produce different results.
3. **Baseline canopy threshold:** Tree cover from 2000 is used as a historical reference. A threshold of 30% is an analytical choice, not a universal forest definition.
4. **Recorded loss is not causal attribution:** The Hansen loss layer does not, by itself, determine whether a change resulted from illegal logging, fire, harvesting, agriculture, or another cause.
5. **No independent ground-truth validation:** Patch analysis describes the supplied dataset and does not establish the accuracy of the loss labels.
6. **No trained model:** This experiment does not train or evaluate a machine-learning classifier.
7. **Geographic scope:** The selected tile is a broad study area, and its results cannot automatically be generalized to other regions.
8. **Pixel counts are not area estimates:** Area reporting requires suitable geospatial calculations and correct handling of the raster's projection and pixel dimensions.
9. **Year-wise interpretation:** Sampled pixel counts are descriptive and should not be presented as full-resolution annual forest-loss estimates.

## 9. Reproducibility

To reproduce the experiment:

1. Open `notebooks/forest/FD03_spatial_loss_analysis.ipynb`.
2. Run the notebook cells in order using the same input tile and documented processing settings.
3. Confirm the raster alignment checks pass.
4. Inspect the generated CSV files and plots.
5. Verify that the expected outputs exist.
6. Record the actual numerical findings in Section 6.
7. Commit the notebook, report, and appropriate result artifacts to the project repository.

The report and notebook should describe the same processing choices and results.

## 10. Conclusion

FD03 is designed to extend forest-disturbance analysis from basic raster inspection to spatial patch characterization, year-wise recorded-loss summaries, and canopy-threshold sensitivity analysis.

Its scientific value depends on reporting the actual notebook outputs and interpreting them within the limitations of the Hansen dataset, reduced-resolution sampling, and the chosen connectivity and canopy thresholds.

**Final status:** Mark FD03 complete only after spatial alignment has been verified, all required outputs have been generated, and the result tables and figures have been reviewed. Numerical conclusions remain pending until those checks are complete.
