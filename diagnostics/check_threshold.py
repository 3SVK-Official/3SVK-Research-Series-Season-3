"""
Check if calibrated threshold is appropriate for test data
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
    print("THRESHOLD DIAGNOSTIC - VALIDATION VS TEST SCORE DISTRIBUTION")
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
    
    # Split
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
    print("Training model...")
    model = AutoencoderModel(config)
    model.fit(train_windows)
    
    # Get scores
    print("\nGetting scores...")
    val_scores = model.predict_scores(val_windows)
    test_scores = model.predict_scores(test_windows)
    
    print(f"\nValidation score distribution:")
    print(f"  Min: {np.min(val_scores):.6f}")
    print(f"  Max: {np.max(val_scores):.6f}")
    print(f"  Mean: {np.mean(val_scores):.6f}")
    print(f"  Median: {np.median(val_scores):.6f}")
    print(f"  Std: {np.std(val_scores):.6f}")
    
    print(f"\nTest score distribution:")
    print(f"  Min: {np.min(test_scores):.6f}")
    print(f"  Max: {np.max(test_scores):.6f}")
    print(f"  Mean: {np.mean(test_scores):.6f}")
    print(f"  Median: {np.median(test_scores):.6f}")
    print(f"  Std: {np.std(test_scores):.6f}")
    
    # Calibrate on validation
    print("\nCalibrating threshold on validation...")
    calibrated_threshold = threshold_calibrator.calibrate(val_labels_adjusted, val_scores)
    print(f"Calibrated threshold: {calibrated_threshold:.6f}")
    
    # Check how many scores exceed threshold
    val_above = np.sum(val_scores >= calibrated_threshold)
    test_above = np.sum(test_scores >= calibrated_threshold)
    
    print(f"\nScores above threshold:")
    print(f"  Validation: {val_above}/{len(val_scores)} ({val_above/len(val_scores)*100:.2f}%)")
    print(f"  Test: {test_above}/{len(test_scores)} ({test_above/len(test_scores)*100:.2f}%)")
    
    # Apply threshold to test
    test_predictions = (test_scores >= calibrated_threshold).astype(int)
    
    # Calculate metrics
    test_metrics = metrics_calculator.calculate_detection_metrics(
        test_labels_adjusted, test_predictions, test_scores
    )
    
    print(f"\nTest metrics with calibrated threshold:")
    print(f"  TP: {test_metrics['true_positive']}")
    print(f"  TN: {test_metrics['true_negative']}")
    print(f"  FP: {test_metrics['false_positive']}")
    print(f"  FN: {test_metrics['false_negative']}")
    print(f"  Precision: {test_metrics['precision']:.4f}")
    print(f"  Recall: {test_metrics['recall']:.4f}")
    print(f"  F1: {test_metrics['f1']:.4f}")
    
    # Try recalibrating on test (just to see what would be optimal)
    print("\n" + "=" * 80)
    print("OPTIMAL THRESHOLD ON TEST DATA (for comparison only)")
    print("=" * 80)
    
    test_calibrator = ThresholdCalibrator(method='f1_optimize')
    test_optimal_threshold = test_calibrator.calibrate(test_labels_adjusted, test_scores)
    test_optimal_f1 = test_calibrator.get_validation_f1()
    
    print(f"Optimal test threshold: {test_optimal_threshold:.6f}")
    print(f"Optimal test F1: {test_optimal_f1:.4f}")
    
    print("\n" + "=" * 80)
    print("CONCLUSION")
    print("=" * 80)
    if test_metrics['f1'] < test_optimal_f1 * 0.5:
        print("Validation threshold performs poorly on test data.")
        print("Consider: using percentile-based threshold, or larger validation set.")
    else:
        print("Validation threshold generalizes reasonably to test data.")
    print("=" * 80)

if __name__ == '__main__':
    main()
