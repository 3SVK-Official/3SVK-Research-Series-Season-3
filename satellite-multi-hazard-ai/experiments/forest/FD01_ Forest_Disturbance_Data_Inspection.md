# FD01 — Forest Disturbance Data Inspection

## 1. Experiment Overview

* **Experiment ID:** FD01
* **Track:** Forest Disturbance Monitoring
* **Dataset:** Hansen Global Forest Change v1.11 (2023)
* **Experiment type:** Data inspection and exploratory analysis
* **Status:** Initial inspection completed; spatial quality checks require confirmation.
* **Notebook:** `notebooks/forest/FD01_data_inspection.ipynb`

## 2. Objective

The objective of FD01 is to inspect satellite-derived tree-canopy cover and tree-cover-loss data, understand their raster structure and value ranges, and establish an initial foundation for future forest-disturbance experiments.

This experiment does not train or evaluate a predictive model.

## 3. Dataset and Data Layers

The experiment uses two layers from the Hansen Global Forest Change dataset:

| Layer           | Description                                                                                                                              |
| --------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `treecover2000` | Estimated percentage of tree canopy cover in the year 2000                                                                               |
| `lossyear`      | Encoded year of detected tree-cover loss, with values 1–23 representing 2001–2023 and 0 representing no recorded loss during that period |

**Dataset reference:**
https://storage.googleapis.com/earthenginepartners-hansen/GFC-2023-v1.11/download.html

## 4. Data Inspection Results

Both layers were sampled to arrays of size **1000 × 1000** for initial inspection.

| Observation                            |      Result |
| -------------------------------------- | ----------: |
| Tree-cover sample dimensions           | 1000 × 1000 |
| Loss-year sample dimensions            | 1000 × 1000 |
| Valid tree-cover sample pixels (0–100) |   1,000,000 |
| Valid loss-year sample pixels (0–23)   |   1,000,000 |
| Pixels with non-zero loss-year values  |       3,440 |
| Pixels with loss-year value 0          |     996,560 |
| Pixels with tree cover ≥30%            |      36,224 |

These figures describe the sampled raster arrays, not the total geographic area covered by the original dataset.

## 5. Loss-Year Distribution

The sampled raster contained non-zero loss-year values across the following years:

| Year | Sampled pixels |
| ---- | -------------: |
| 2001 |             55 |
| 2002 |             60 |
| 2003 |             76 |
| 2004 |             77 |
| 2005 |             85 |
| 2006 |             91 |
| 2007 |            117 |
| 2008 |            137 |
| 2009 |            169 |
| 2010 |             37 |
| 2011 |            220 |
| 2012 |            122 |
| 2013 |            123 |
| 2014 |            203 |
| 2015 |             87 |
| 2016 |            215 |
| 2017 |            196 |
| 2018 |            227 |
| 2019 |            195 |
| 2020 |            203 |
| 2021 |            122 |
| 2022 |            180 |
| 2023 |            443 |

The highest sampled count occurred in 2023, with 443 pixels. This is a descriptive observation from the sampled data and should not be interpreted as a regional or global trend without further analysis.

## 6. Methodology

The experiment followed these steps:

1. Downloaded the selected tree-cover and loss-year raster layers.
2. Inspected raster metadata, including dimensions, coordinate reference systems, transforms, and bounds.
3. Read downsampled versions of both layers for exploratory analysis.
4. Examined valid value ranges and the distribution of recorded loss years.
5. Visualized the tree-cover and loss-year layers.
6. Explored the relationship between canopy cover and recorded loss using an exploratory canopy threshold of 30%.
7. Generated a conclusion report and saved the inspection outputs.

## 7. Interpretation

The inspected layers provide a starting point for studying tree-cover patterns and recorded tree-cover loss.

However, a non-zero loss-year value alone does not establish why the loss occurred. It does not prove illegal deforestation, identify a particular human activity, or demonstrate permanent forest conversion.

The 30% canopy threshold is exploratory and is not a universal definition of forest.

## 8. Limitations

* The analysis uses downsampled raster arrays rather than a full-resolution regional assessment.
* Pixel counts are not equivalent to hectares or square kilometres.
* Spatial alignment must be verified before comparing pixels across layers.
* Matching array dimensions alone do not prove that two rasters are spatially aligned.
* No independent ground-truth validation has been completed.
* No predictive model or detection-performance evaluation has been completed.
* Recorded tree-cover loss must not automatically be interpreted as permanent deforestation.

## 9. Output Artifacts

The notebook generates inspection outputs under the configured results directory, including:

* `FD01_raster_metadata.csv`
* `FD01_forest_layers.png`
* `FD01_loss_year_distribution.csv`
* `FD01_loss_by_year.csv`
* `FD01_loss_by_year.png`
* `FD01_treecover_loss_crosscheck.csv`
* `FD01_loss_overlay.png`
* `FD01_research_observations.md`
* `FD01_conclusion.md`

The existence of each artifact should be verified before the experiment is considered fully documented.

## 10. Conclusion

FD01 completed an initial descriptive inspection of the Hansen Global Forest Change tree-cover and loss-year layers. The sampled data contained 3,440 pixels with non-zero loss-year values and 36,224 pixels with estimated canopy cover of at least 30%.

These findings establish an exploratory data-inspection baseline only. They do not demonstrate the accuracy of a forest-disturbance detection system.

The next step is to confirm spatial alignment and metadata compatibility, select a clearly defined study area, identify suitable reference labels, and develop a reproducible baseline that can be evaluated using appropriate metrics.

**Final status:** Initial data inspection completed. Scientific validation and predictive evaluation remain future work.
