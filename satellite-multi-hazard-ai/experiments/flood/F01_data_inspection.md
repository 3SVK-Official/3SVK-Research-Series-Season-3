# F-01 — Sen1Floods11 Data Inspection

## 1. Experiment Overview

**Experiment ID:** F-01  
**Hazard:** Flood  
**Dataset:** Sen1Floods11 v1.1  
**Experiment Type:** Dataset inspection and quality assessment  
**Status:** Completed

This experiment establishes a reproducible understanding of the
Sen1Floods11 flood dataset before implementing a flood-detection
baseline.

The purpose is to verify the dataset structure, inspect Sentinel-1
inputs and flood labels, check data quality, verify image-label
alignment, and identify characteristics that may affect later
experiments.

---

## 2. Objective

The objectives of F-01 are:

1. Verify access to the official Sen1Floods11 v1.1 dataset.
2. Inspect the available dataset splits.
3. Understand how Sentinel-1 images and flood labels are referenced.
4. Inspect one complete Sentinel-1 and flood-label sample.
5. Verify image dimensions, bands, datatype, CRS, and spatial extent.
6. Inspect flood-label classes and class distribution.
7. Check for missing and invalid values.
8. Verify that Sentinel-1 imagery and corresponding labels are
   spatially aligned.
9. Inspect the dataset metadata and geographic coverage.
10. Identify important considerations for the next flood baseline
    experiment.

---

## 3. Dataset Access

The official Sen1Floods11 v1.1 Google Cloud Storage structure was
successfully accessed.

The inspected data includes the hand-labeled flood-event data and
associated split files.

The following split files were successfully downloaded and inspected:

- `flood_train_data.csv`
- `flood_valid_data.csv`
- `flood_test_data.csv`
- `flood_bolivia_data.csv`

The Sentinel-1 and label files were accessed from the corresponding
`HandLabeled/S1Hand` and `HandLabeled/LabelHand` directories.

---

## 4. Dataset Split Sizes

The inspected split sizes were:

| Split | Samples |
|---|---:|
| Training | 251 |
| Validation | 88 |
| Test | 89 |
| Bolivia | 14 |

The split CSV files contained two columns representing Sentinel-1
image references and corresponding flood-label references.

---

## 5. Split File Structure Observation

An important observation was that the CSV column names themselves
contain filenames.

For example, the training CSV columns were:

- `Ghana_103272_S1Hand.tif`
- `Ghana_103272_LabelHand.tif`

However, the first data record referenced:

- `Ghana_24858_S1Hand.tif`
- `Ghana_24858_LabelHand.tif`

Therefore, these CSV files should not be interpreted as ordinary
feature tables.

They function as lists of corresponding Sentinel-1 and label file
references.

This distinction is important for later data-loading code.

---

## 6. Training Split Data Quality

The training CSV was inspected for missing values and duplicate
records.

### Missing values

No missing values were found in the training split.

```text
Total missing values: 0