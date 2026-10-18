"""
Investigate if anomalies are detectable in the synthetic dataset
"""

import sys
import yaml
import numpy as np
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data.loader import DataLoader
from src.preprocessing.preprocessor import Preprocessor

def load_config(config_path: str = 'configs/default_config.yaml') -> dict:
    """Load configuration"""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def main():
    print("=" * 80)
    print("DATA INVESTIGATION - ARE ANOMALIES DETECTABLE?")
    print("=" * 80)
    
    config = load_config()
    np.random.seed(config['experiments']['random_seed'])
    
    data_loader = DataLoader(config)
    preprocessor = Preprocessor(config)
    
    # Load dataset
    print("\nLoading dataset...")
    data, labels = data_loader.load_dataset('synthetic', n_samples=5000, anomaly_ratio=0.05)
    
    # Split
    train_data, val_data, test_data, train_labels, val_labels, test_labels = \
        data_loader.train_val_test_split(data, labels, train_ratio=0.7, val_ratio=0.15)
    
    print(f"\nRaw data statistics:")
    print(f"  Train: mean={np.mean(train_data):.4f}, std={np.std(train_data):.4f}")
    print(f"  Val: mean={np.mean(val_data):.4f}, std={np.std(val_data):.4f}")
    print(f"  Test: mean={np.mean(test_data):.4f}, std={np.std(test_data):.4f}")
    
    print(f"\nAnomaly statistics (raw):")
    train_anomalies = train_data[train_labels == 1]
    train_normal = train_data[train_labels == 0]
    print(f"  Train anomalies: mean={np.mean(train_anomalies):.4f}, std={np.std(train_anomalies):.4f}")
    print(f"  Train normal: mean={np.mean(train_normal):.4f}, std={np.std(train_normal):.4f}")
    print(f"  Difference in means: {abs(np.mean(train_anomalies) - np.mean(train_normal)):.4f}")
    
    # Preprocess
    print("\nPreprocessing...")
    train_windows = preprocessor.fit_transform(train_data)
    val_windows = preprocessor.transform(val_data)
    test_windows = preprocessor.transform(test_data)
    
    print(f"\nWindowed data statistics:")
    print(f"  Train windows: {train_windows.shape}")
    print(f"  Val windows: {val_windows.shape}")
    print(f"  Test windows: {test_windows.shape}")
    
    # Adjust labels
    window_size = config['data']['window_size']
    val_labels_adjusted = val_labels[window_size-1:]
    test_labels_adjusted = test_labels[window_size-1:]
    
    print(f"\nAdjusted labels:")
    print(f"  Val anomalies: {np.sum(val_labels_adjusted)}/{len(val_labels_adjusted)}")
    print(f"  Test anomalies: {np.sum(test_labels_adjusted)}/{len(test_labels_adjusted)}")
    
    # Check if anomalies are distinguishable in windowed data
    print("\n" + "=" * 80)
    print("ANOMALY DETECTABILITY IN WINDOWED DATA")
    print("=" * 80)
    
    val_anomaly_windows = val_windows[val_labels_adjusted == 1]
    val_normal_windows = val_windows[val_labels_adjusted == 0]
    
    print(f"\nValidation windows statistics:")
    print(f"  Anomaly windows: {val_anomaly_windows.shape}")
    print(f"  Normal windows: {val_normal_windows.shape}")
    
    # Flatten windows for comparison
    val_anomaly_flat = val_anomaly_windows.reshape(val_anomaly_windows.shape[0], -1)
    val_normal_flat = val_normal_windows.reshape(val_normal_windows.shape[0], -1)
    
    print(f"\nFlattened window statistics:")
    print(f"  Anomaly: mean={np.mean(val_anomaly_flat):.4f}, std={np.std(val_anomaly_flat):.4f}")
    print(f"  Normal: mean={np.mean(val_normal_flat):.4f}, std={np.std(val_normal_flat):.4f}")
    print(f"  Mean difference: {abs(np.mean(val_anomaly_flat) - np.mean(val_normal_flat)):.4f}")
    
    # Simple statistical test: can we separate with a simple threshold?
    print("\n" + "=" * 80)
    print("SIMPLE THRESHOLD TEST (on flattened windows)")
    print("=" * 80)
    
    # Use max value in each window as feature
    val_anomaly_max = np.max(val_anomaly_flat, axis=1)
    val_normal_max = np.max(val_normal_flat, axis=1)
    
    print(f"\nMax value in windows:")
    print(f"  Anomaly: mean={np.mean(val_anomaly_max):.4f}, std={np.std(val_anomaly_max):.4f}")
    print(f"  Normal: mean={np.mean(val_normal_max):.4f}, std={np.std(val_normal_max):.4f}")
    
    # Try simple threshold
    all_max = np.concatenate([val_anomaly_max, val_normal_max])
    all_labels = np.concatenate([np.ones(len(val_anomaly_max)), np.zeros(len(val_normal_max))])
    
    # Optimize threshold
    thresholds = np.linspace(np.min(all_max), np.max(all_max), 100)
    best_f1 = 0
    best_threshold = 0.5
    
    for thresh in thresholds:
        preds = (all_max >= thresh).astype(int)
        tp = np.sum((all_labels == 1) & (preds == 1))
        fp = np.sum((all_labels == 0) & (preds == 1))
        fn = np.sum((all_labels == 1) & (preds == 0))
        
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
        
        if f1 > best_f1:
            best_f1 = f1
            best_threshold = thresh
    
    print(f"\nSimple threshold on max window value:")
    print(f"  Best threshold: {best_threshold:.4f}")
    print(f"  Best F1: {best_f1:.4f}")
    
    # Try mean value
    val_anomaly_mean = np.mean(val_anomaly_flat, axis=1)
    val_normal_mean = np.mean(val_normal_flat, axis=1)
    
    print(f"\nMean value in windows:")
    print(f"  Anomaly: mean={np.mean(val_anomaly_mean):.4f}, std={np.std(val_anomaly_mean):.4f}")
    print(f"  Normal: mean={np.mean(val_normal_mean):.4f}, std={np.std(val_normal_mean):.4f}")
    
    all_mean = np.concatenate([val_anomaly_mean, val_normal_mean])
    best_f1_mean = 0
    best_threshold_mean = 0.5
    
    for thresh in thresholds:
        preds = (all_mean >= thresh).astype(int)
        tp = np.sum((all_labels == 1) & (preds == 1))
        fp = np.sum((all_labels == 0) & (preds == 1))
        fn = np.sum((all_labels == 1) & (preds == 0))
        
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
        
        if f1 > best_f1_mean:
            best_f1_mean = f1
            best_threshold_mean = thresh
    
    print(f"\nSimple threshold on mean window value:")
    print(f"  Best threshold: {best_threshold_mean:.4f}")
    print(f"  Best F1: {best_f1_mean:.4f}")
    
    print("\n" + "=" * 80)
    print("CONCLUSION")
    print("=" * 80)
    if best_f1 > 0.3:
        print("Anomalies ARE detectable with simple statistical methods.")
        print("The autoencoder should be able to learn this pattern.")
    elif best_f1 > 0.1:
        print("Anomalies are PARTIALLY detectable.")
        print("The autoencoder may struggle but should achieve some performance.")
    else:
        print("Anomalies are NOT easily detectable with simple methods.")
        print("The synthetic dataset may need stronger anomaly signals.")
    print("=" * 80)

if __name__ == '__main__':
    main()
