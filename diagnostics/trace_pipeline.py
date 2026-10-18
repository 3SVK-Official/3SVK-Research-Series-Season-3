"""
Diagnostic script to trace the complete detection pipeline
Identify root cause of F1=0 failure
"""

import sys
import yaml
import numpy as np
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data.loader import DataLoader
from src.preprocessing.preprocessor import Preprocessor
from src.models.isolation_forest import IsolationForestModel
from src.models.autoencoder import AutoencoderModel
from src.models.lstm_autoencoder import LSTMAutoencoderModel

def load_config(config_path: str = 'configs/default_config.yaml') -> dict:
    """Load configuration"""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def main():
    print("=" * 80)
    print("PIPELINE DIAGNOSTIC - F1=0 FAILURE INVESTIGATION")
    print("=" * 80)
    
    # Load config
    config = load_config()
    np.random.seed(config['experiments']['random_seed'])
    
    # STEP 1: Load dataset
    print("\n[STEP 1] DATASET LOADING")
    print("-" * 80)
    data_loader = DataLoader(config)
    data, labels = data_loader.load_dataset('synthetic', n_samples=5000, anomaly_ratio=0.05)
    print(f"Raw data shape: {data.shape}")
    print(f"Raw labels shape: {labels.shape}")
    print(f"Total anomalies in raw data: {np.sum(labels)}")
    print(f"Anomaly ratio: {np.sum(labels) / len(labels):.4f}")
    print(f"Label distribution: normal={np.sum(labels==0)}, anomaly={np.sum(labels==1)}")
    
    # STEP 2: Train/test split
    print("\n[STEP 2] TRAIN/TEST SPLIT")
    print("-" * 80)
    train_data, test_data, train_labels, test_labels = data_loader.train_test_split(
        data, labels, test_ratio=0.2
    )
    print(f"Train data shape: {train_data.shape}")
    print(f"Train labels shape: {train_labels.shape}")
    print(f"Train anomalies: {np.sum(train_labels)}")
    print(f"Test data shape: {test_data.shape}")
    print(f"Test labels shape: {test_labels.shape}")
    print(f"Test anomalies: {np.sum(test_labels)}")
    
    # STEP 3: Preprocessing
    print("\n[STEP 3] PREPROCESSING")
    print("-" * 80)
    preprocessor = Preprocessor(config)
    train_windows = preprocessor.fit_transform(train_data)
    test_windows = preprocessor.transform(test_data)
    print(f"Train windows shape: {train_windows.shape}")
    print(f"Test windows shape: {test_windows.shape}")
    
    # Label adjustment
    window_size = config['data']['window_size']
    test_labels_adjusted = test_labels[window_size-1:]
    print(f"Adjusted test labels shape: {test_labels_adjusted.shape}")
    print(f"Adjusted test anomalies: {np.sum(test_labels_adjusted)}")
    
    # Check if anomalies are preserved
    original_test_anomalies = np.sum(test_labels)
    adjusted_test_anomalies = np.sum(test_labels_adjusted)
    print(f"Anomaly loss due to windowing: {original_test_anomalies - adjusted_test_anomalies}")
    
    # STEP 4: Train models
    print("\n[STEP 4] MODEL TRAINING")
    print("-" * 80)
    
    # LIGHT model (Z-score)
    print("\nTraining LIGHT model (Z-score)...")
    light_model = IsolationForestModel(config)
    light_model.fit(train_windows)
    print(f"LIGHT threshold: {light_model.threshold}")
    
    # STANDARD model (Autoencoder)
    print("\nTraining STANDARD model (Autoencoder)...")
    standard_model = AutoencoderModel(config)
    standard_model.fit(train_windows)
    print(f"STANDARD threshold: {standard_model.threshold}")
    
    # HEAVY model (LSTM Autoencoder)
    print("\nTraining HEAVY model (LSTM Autoencoder)...")
    heavy_model = LSTMAutoencoderModel(config)
    heavy_model.fit(train_windows)
    print(f"HEAVY model trained (uses median threshold)")
    
    # STEP 5: Prediction on test data
    print("\n[STEP 5] PREDICTION ON TEST DATA")
    print("-" * 80)
    
    # Test with each model
    for mode, model in [('LIGHT', light_model), ('STANDARD', standard_model), ('HEAVY', heavy_model)]:
        print(f"\n{mode} model predictions:")
        scores, preds = model.predict(test_windows)
        print(f"  Score range: [{np.min(scores):.4f}, {np.max(scores):.4f}]")
        print(f"  Score mean: {np.mean(scores):.4f}")
        print(f"  Score std: {np.std(scores):.4f}")
        print(f"  Predictions: {np.sum(preds)} anomalies detected")
        print(f"  Actual anomalies: {np.sum(test_labels_adjusted)}")
        
        # Calculate confusion matrix
        tp = np.sum((test_labels_adjusted == 1) & (preds == 1))
        tn = np.sum((test_labels_adjusted == 0) & (preds == 0))
        fp = np.sum((test_labels_adjusted == 0) & (preds == 1))
        fn = np.sum((test_labels_adjusted == 1) & (preds == 0))
        
        print(f"  TP: {tp}, TN: {tn}, FP: {fp}, FN: {fn}")
        
        if tp + fp > 0:
            precision = tp / (tp + fp)
        else:
            precision = 0.0
        if tp + fn > 0:
            recall = tp / (tp + fn)
        else:
            recall = 0.0
        if precision + recall > 0:
            f1 = 2 * precision * recall / (precision + recall)
        else:
            f1 = 0.0
        
        print(f"  Precision: {precision:.4f}")
        print(f"  Recall: {recall:.4f}")
        print(f"  F1: {f1:.4f}")
    
    # STEP 6: Check threshold alignment
    print("\n[STEP 6] THRESHOLD ALIGNMENT CHECK")
    print("-" * 80)
    thresholds = config.get('controller', {}).get('thresholds', {})
    threshold_high = thresholds.get('anomaly_high', 0.8)
    threshold_low = thresholds.get('anomaly_low', 0.5)
    print(f"EdgeProcessor threshold_high: {threshold_high}")
    print(f"EdgeProcessor threshold_low: {threshold_low}")
    
    # Check if model scores exceed these thresholds
    scores_standard, _ = standard_model.predict(test_windows)
    print(f"\nSTANDARD model scores vs thresholds:")
    print(f"  Scores > {threshold_high}: {np.sum(scores_standard > threshold_high)}")
    print(f"  Scores > {threshold_low}: {np.sum(scores_standard > threshold_low)}")
    print(f"  Scores <= {threshold_low}: {np.sum(scores_standard <= threshold_low)}")
    
    # STEP 7: Anomaly score direction check
    print("\n[STEP 7] ANOMALY SCORE DIRECTION CHECK")
    print("-" * 80)
    # Check if anomalies have higher or lower scores
    anomaly_indices = np.where(test_labels_adjusted == 1)[0]
    normal_indices = np.where(test_labels_adjusted == 0)[0]
    
    if len(anomaly_indices) > 0 and len(normal_indices) > 0:
        anomaly_scores = scores_standard[anomaly_indices]
        normal_scores = scores_standard[normal_indices]
        
        print(f"Anomaly score mean: {np.mean(anomaly_scores):.4f}")
        print(f"Normal score mean: {np.mean(normal_scores):.4f}")
        print(f"Anomaly score median: {np.median(anomaly_scores):.4f}")
        print(f"Normal score median: {np.median(normal_scores):.4f}")
        
        if np.mean(anomaly_scores) > np.mean(normal_scores):
            print("Direction: Higher scores = more anomalous (CORRECT)")
        else:
            print("Direction: Lower scores = more anomalous (PROBLEM!)")
    
    print("\n" + "=" * 80)
    print("DIAGNOSTIC COMPLETE")
    print("=" * 80)

if __name__ == '__main__':
    main()
