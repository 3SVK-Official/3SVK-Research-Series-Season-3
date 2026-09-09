"""
Baseline A: Centralized Detection Experiment
All data transmitted to cloud for processing
"""

import sys
import yaml
import numpy as np
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.data.loader import DataLoader
from src.data.stream import DataStream
from src.preprocessing.preprocessor import Preprocessor
from src.cloud.coordinator import CloudCoordinator
from src.evaluation.system_monitor import SystemMonitor
from src.evaluation.metrics import MetricsCalculator
from src.evaluation.threshold_calibrator import ThresholdCalibrator
import json
import time


def load_config(config_path: str = 'configs/default_config.yaml') -> dict:
    """Load configuration"""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def main():
    """Run centralized baseline experiment"""
    print("=" * 60)
    print("BASELINE A: Centralized Detection")
    print("=" * 60)
    
    # Load config
    config = load_config()
    
    # Set random seed
    np.random.seed(config['experiments']['random_seed'])
    
    # Initialize components
    data_loader = DataLoader(config)
    preprocessor = Preprocessor(config)
    system_monitor = SystemMonitor()
    metrics_calculator = MetricsCalculator(config)
    threshold_calibrator = ThresholdCalibrator(method='f1_optimize')
    
    # Load synthetic dataset
    print("\nLoading dataset...")
    data, labels = data_loader.load_dataset('synthetic', n_samples=5000, anomaly_ratio=0.05)
    
    # Train/validation/test split (70/15/15)
    print("Splitting data (70/15/15)...")
    train_data, val_data, test_data, train_labels, val_labels, test_labels = \
        data_loader.train_val_test_split(data, labels, train_ratio=0.7, val_ratio=0.15)
    
    # Preprocess training data
    print("Preprocessing training data...")
    train_windows = preprocessor.fit_transform(train_data)
    
    # Preprocess validation data
    print("Preprocessing validation data...")
    val_windows = preprocessor.transform(val_data)
    
    # Initialize cloud coordinator
    print("Initializing cloud coordinator...")
    cloud_coordinator = CloudCoordinator(config, system_monitor)
    
    # Set network conditions (simulated)
    cloud_coordinator.set_network_conditions(latency=50.0, bandwidth=100.0)
    
    # Train cloud model
    cloud_coordinator.train_model(train_windows)
    
    # Calibrate threshold on validation data
    print("\nCalibrating threshold on validation data...")
    window_size = config['data']['window_size']
    val_labels_adjusted = val_labels[window_size-1:]
    
    model = cloud_coordinator.model
    val_scores = model.predict_scores(val_windows)
    calibrated_threshold = threshold_calibrator.calibrate(val_labels_adjusted, val_scores)
    validation_f1 = threshold_calibrator.get_validation_f1()
    
    print(f"Calibrated threshold: {calibrated_threshold:.6f}")
    print(f"Validation F1: {validation_f1:.4f}")
    
    # Set threshold in cloud coordinator
    cloud_coordinator.set_threshold(calibrated_threshold)
    
    # Preprocess test data
    print("Preprocessing test data...")
    test_windows = preprocessor.transform(test_data)
    
    # Adjust labels for windows (use label of last sample in window)
    test_labels_adjusted = test_labels[window_size-1:]
    
    # Create data stream
    print("Creating data stream...")
    test_stream = DataStream(test_windows, test_labels_adjusted, buffer_size=1000)
    
    # Start system monitoring
    system_monitor.start_monitoring(interval=0.1)
    
    # Process stream in cloud
    print("Processing stream in cloud (centralized)...")
    start_time = time.time()
    results = cloud_coordinator.process_stream(test_stream)
    total_time = time.time() - start_time
    
    # Stop monitoring
    system_monitor.stop_monitoring()
    
    # Get actual CPU measurements from monitoring
    cpu_measurements = list(system_monitor.cpu_history)
    mem_measurements = list(system_monitor.memory_history)
    
    # Calculate metrics
    print("\nCalculating metrics...")
    detection_metrics = metrics_calculator.calculate_detection_metrics(
        results['labels'],
        results['predictions'],
        results['scores']
    )
    
    system_metrics = metrics_calculator.calculate_system_metrics(
        results['latencies'],
        cpu_measurements if cpu_measurements else [0] * len(results['latencies']),
        mem_measurements if mem_measurements else [0] * len(results['latencies']),
        cloud_coordinator.stats['total_data_transmitted'],
        results['latencies']
    )
    
    # Combine results
    all_metrics = {**detection_metrics, **system_metrics}
    all_metrics['total_processing_time'] = total_time
    all_metrics['calibrated_threshold'] = float(calibrated_threshold)
    all_metrics['validation_f1'] = float(validation_f1)
    
    # Save results
    results_dir = Path(__file__).parent.parent.parent / 'results'
    results_dir.mkdir(exist_ok=True)
    
    output_file = results_dir / 'baseline_centralized.json'
    with open(output_file, 'w') as f:
        json.dump(all_metrics, f, indent=2)
    
    print("\n" + "=" * 60)
    print("BASELINE A RESULTS (Centralized with Calibration)")
    print("=" * 60)
    print(f"Calibrated threshold: {calibrated_threshold:.6f}")
    print(f"Validation F1: {validation_f1:.4f}")
    print(f"Samples processed: {cloud_coordinator.stats['samples_processed']}")
    print(f"Anomalies detected: {cloud_coordinator.stats['anomalies_detected']}")
    print(f"Data transmitted: {cloud_coordinator.stats['total_data_transmitted']} bytes")
    print(f"Total processing time: {total_time:.2f}s")
    print(f"\nDetection Metrics:")
    print(f"  Accuracy: {detection_metrics['accuracy']:.4f}")
    print(f"  Precision: {detection_metrics['precision']:.4f}")
    print(f"  Recall: {detection_metrics['recall']:.4f}")
    print(f"  F1-Score: {detection_metrics['f1']:.4f}")
    print(f"  ROC-AUC: {detection_metrics.get('roc_auc', 0):.4f}")
    print(f"  PR-AUC: {detection_metrics.get('pr_auc', 0):.4f}")
    print(f"\nSystem Metrics:")
    print(f"  Mean latency: {system_metrics['inference_latency_mean']:.2f} ms")
    print(f"  P95 latency: {system_metrics['inference_latency_p95']:.2f} ms")
    print(f"  P99 latency: {system_metrics['inference_latency_p99']:.2f} ms")
    print("=" * 60)
    
    print(f"\nResults saved to {output_file}")


if __name__ == '__main__':
    main()
