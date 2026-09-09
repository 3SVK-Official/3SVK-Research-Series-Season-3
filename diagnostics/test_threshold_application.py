"""
Minimal test to verify threshold application in EdgeProcessor
"""

import sys
import yaml
import numpy as np
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data.loader import DataLoader
from src.preprocessing.preprocessor import Preprocessor
from src.edge.processor import EdgeProcessor
from src.adaptive.controller import AdaptiveController
from src.evaluation.system_monitor import SystemMonitor
from src.evaluation.threshold_calibrator import ThresholdCalibrator

def load_config(config_path: str = 'configs/default_config.yaml') -> dict:
    """Load configuration"""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def main():
    print("=" * 80)
    print("MINIMAL THRESHOLD APPLICATION TEST")
    print("=" * 80)
    
    config = load_config()
    np.random.seed(config['experiments']['random_seed'])
    
    data_loader = DataLoader(config)
    preprocessor = Preprocessor(config)
    system_monitor = SystemMonitor()
    controller = AdaptiveController(config)
    threshold_calibrator = ThresholdCalibrator(method='f1_optimize')
    
    # Load dataset
    print("Loading dataset...")
    data, labels = data_loader.load_dataset('synthetic', n_samples=1000, anomaly_ratio=0.05)
    
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
    
    # Initialize edge processor
    print("Initializing edge processor...")
    edge_processor = EdgeProcessor(config, controller, system_monitor)
    edge_processor.train_models(train_windows)
    
    # Calibrate threshold
    print("Calibrating threshold...")
    model = edge_processor.models['STANDARD']
    val_scores = model.predict_scores(val_windows)
    calibrated_threshold = threshold_calibrator.calibrate(val_labels_adjusted, val_scores)
    
    print(f"Calibrated threshold: {calibrated_threshold:.6f}")
    
    # Set threshold in edge processor
    edge_processor.set_threshold(calibrated_threshold)
    print(f"Edge processor threshold: {edge_processor.threshold}")
    print(f"Edge processor calibrated: {edge_processor.calibrated}")
    
    # Test threshold application on first 10 samples
    print("\nTesting threshold application on first 10 test samples:")
    test_scores = model.predict_scores(test_windows[:10])
    
    for i, score in enumerate(test_scores):
        label = 1 if score >= calibrated_threshold else 0
        print(f"  Sample {i}: score={score:.6f}, threshold={calibrated_threshold:.6f}, label={label}")
    
    # Test via process_sample
    print("\nTesting via process_sample:")
    for i in range(5):
        sample = test_windows[i]
        print(f"  Sample {i}: shape={sample.shape}, min={sample.min():.4f}, max={sample.max():.4f}")
        print(f"  Direct model call on sample {i}:")
        direct_score = model.predict_scores(sample.reshape(1, -1))[0]
        print(f"    Direct score (2D): {direct_score:.6f}")
        score, _ = edge_processor.process_sample(sample, mode='STANDARD')
        label = 1 if score >= edge_processor.threshold else 0
        print(f"  Process_sample result: score={score:.6f}, threshold={edge_processor.threshold:.6f}, label={label}")
    
    print("\n" + "=" * 80)
    print("If labels are 0 for all samples with score >= threshold, there's a bug.")
    print("=" * 80)

if __name__ == '__main__':
    main()
