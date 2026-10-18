
# F-03 — VV vs VV + VH Threshold Baseline

## 1. Overview

**Project:** Satellite-Based Multi-Hazard Intelligence System  
**Research Track:** Flood Inundation Detection  
**Experiment ID:** F-03  
**Dataset:** Sen1Floods11  
**Status:** Initial baseline comparison completed; geospatial alignment validation remains pending.

## 2. Objective

Compare a single-polarization Sentinel-1 VV threshold baseline with a two-polarization VV + VH threshold baseline for flood inundation mapping.

The experiment investigates whether adding a VH threshold condition changes flood-detection performance compared with using VV alone.

## 3. Methods

### VV-only baseline

A pixel is classified as flooded when its VV backscatter is below the selected VV threshold.

### VV + VH baseline

A pixel is classified as flooded only when both conditions are satisfied:

- VV is below the selected VV threshold.
- VH is below the selected VH threshold.

This is a rule-based threshold baseline, not a trained machine-learning model.

## 4. Threshold Selection and Evaluation

Thresholds were selected using the validation data. The VV + VH threshold search used sampled validation pixels to reduce computation time.

The selected methods were evaluated on the test data using a common valid-pixel mask.

The results must be interpreted in the context of the selected threshold rules, validation sampling procedure and dataset.

## 5. Test Results

The measured results are available in `F03_test_comparison.csv`.

The following metrics were evaluated:

- Precision
- Recall
- F1-score
- Intersection over Union (IoU)

The differences between the two methods are recorded in `F03_metric_differences.csv`.

Actual metric values should be taken from these generated result files rather than estimated or manually entered.

## 6. Main Observation

The experiment compares the performance of VV-only and VV + VH threshold rules on the selected test data.

Whether VV + VH performs better or worse must be determined from the actual test metrics. Precision, recall, F1-score and IoU should be considered together because an improvement in one metric does not necessarily mean that all types of errors have decreased.

## 7. Research Interpretation

This experiment establishes an initial comparison between a single-polarization threshold and a simple two-polarization threshold rule.

It does not prove that adding VH universally improves flood detection. Performance may depend on surface conditions, land cover, acquisition geometry, location and selected thresholds.

The results provide a baseline for deciding which further experiments are justified.

## 8. Limitations and Quality Checks

- Both methods are threshold-based and do not learn parameters from labelled examples.
- Threshold selection for VV + VH used sampled validation pixels.
- The VV + VH rule requires both threshold conditions. This may reduce false alarms but can also miss flooded pixels.
- Pooled pixel metrics can be influenced by large images and class imbalance.
- A geospatial alignment warning occurred during data loading. Equal array dimensions alone do not prove that the image and label are spatially aligned.
- The image-label alignment issue must be investigated before treating the metrics as scientifically validated.
- Label values and their meanings must be verified before final evaluation.
- These results should not be generalized to other locations without further testing.

## 9. Reproducibility

Retain the notebook and generated results alongside this experiment record.

Expected output files:

- `F03_vv_validation.csv`
- `F03_vv_vh_validation.csv`
- `F03_test_comparison.csv`
- `F03_per_sample_results.csv`
- `F03_metric_differences.csv`
- `F03_vv_vh_visual_comparison.png`
- `F03_summary.txt`

## 10. Conclusion

F-03 completed an initial comparison of VV-only and VV + VH threshold baselines using the Sen1Floods11 test data.

The experiment provides a measurable baseline comparison without assuming in advance that the two-polarization rule is superior.

The next research decision should be based on the observed metric differences, visual error analysis and verification of spatial alignment. Any more advanced model should be justified by the limitations observed in these baseline experiments.