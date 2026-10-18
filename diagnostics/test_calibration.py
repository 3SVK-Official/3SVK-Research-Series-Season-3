"""
Test threshold calibration with STANDARD mode only (no adaptive controller)
"""

import sys
import yaml
import numpy as np
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data.loader import DataLoader
from src.preprocessing.preprocessor import Preprocessor
from src.models.autoencoder import AutoencoderModel
from src.evaluation.threshold_calibrator import ThresholdCalibrator
from src.evaluation.metrics import MetricsCalculator

def load_config(config_path: str = 'configs/default_config.yaml') -> dict:
    """Load configuration"""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def main():
    print("=" * 80)
    print("THRESHOLD CALIBRATION TEST - STANDARD MODE ONLY")
    print("=" * 80)
    
    config = load_config()
    np.random.seed(config['experiments']['random_seed'])
    
    data_loader = DataLoader(config)
    preprocessor = Preprocessor(config)
    threshold_calibrator = ThresholdCalibrator(method='f1_optimize')
    metrics_calculator = MetricsCalculator(config)
    
    # Load dataset
    print("\nLoading dataset...")
    data, labels = data_loader.load_dataset('synthetic', n_samples=5000, anomaly_ratio=0.05)
    
    # Train/validation/test split
    print("Splitting data (70/15/15)...")
    train_data, val_data, test_data, train_labels, val_labels, test_labels = \
        data_loader.train_val_test_split(data, labels, train_ratio=0.7, val_ratio=0.15)
    
    # Preprocess
    print("Preprocessing...")
    train_windows = preprocessor.fit_transform(train_data)
    val_windows = preprocessor.transform(val_data)
    test_windows = preprocessor.transform(test_data)
    
    # Adjust labels
    window_size = config['data']['window_size']
    val_labels_adjusted = val_labels[window_size-1:]
    test_labels_adjusted = test_labels[window_size-1:]
    
    # Train model
    print("Training STANDARD model...")
    model = AutoencoderModel(config)
    model.fit(train_windows)
    
    # Calibrate on validation
    print("\nCalibrating threshold on validation data...")
    val_scores = model.predict_scores(val_windows)
    calibrated_threshold = threshold_calibrator.calibrate(val_labels_adjusted, val_scores)
    validation_f1 = threshold_calibrator.get_validation_f1()
    
    print(f"Calibrated threshold: {calibrated_threshold:.6f}")
    print(f"Validation F1: {validation_f1:.4f}")
    
    # Evaluate on test
    print("\nEvaluating on test data...")
    test_scores = model.predict_scores(test_windows)
    test_predictions = threshold_calibrator.apply(test_scores)
    
    test_metrics = metrics_calculator.calculate_detection_metrics(
        test_labels_adjusted, test_predictions, test_scores
    )
    
    print("\n" + "=" * 80)
    print("TEST RESULTS")
    print("=" * 80)
    print(f"TP: {test_metrics['true_positive']}")
    print(f"TN: {test_metrics['true_negative']}")
    print(f"FP: {test_metrics['false_positive']}")
    print(f"FN: {test_metrics['false_negative']}")
    print(f"Precision: {test_metrics['precision']:.4f}")
    print(f"Recall: {test_metrics['recall']:.4f}")
    print(f"F1: {test_metrics['f1']:.4f}")
    print(f"ROC-AUC: {test_metrics['roc_auc']:.4f}")
    print(f"PR-AUC: {test_metrics['pr_auc']:.4f}")
    print("=" * 80)

if __name__ == '__main__':
    main()
