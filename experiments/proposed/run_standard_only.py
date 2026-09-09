"""
Proposed Method: Static Edge with STANDARD mode (no adaptive switching)
Validates that detection works with proper threshold calibration
"""

import sys
import yaml
import numpy as np
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.data.loader import DataLoader
from src.data.stream import DataStream
from src.preprocessing.preprocessor import Preprocessor
from src.edge.processor import EdgeProcessor
from src.adaptive.controller import AdaptiveController
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
    """Run static edge experiment with STANDARD mode only"""
    print("=" * 80)
    print("STATIC EDGE: STANDARD MODE ONLY (No Adaptive Switching)")
    print("=" * 80)
    
    config = load_config()
    np.random.seed(config['experiments']['random_seed'])
    
    data_loader = DataLoader(config)
    preprocessor = Preprocessor(config)
    system_monitor = SystemMonitor()
    controller = AdaptiveController(config)
    metrics_calculator = MetricsCalculator(config)
    threshold_calibrator = ThresholdCalibrator(method='f1_optimize')
    
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
    
    # Initialize edge processor
    print("Initializing edge processor...")
    edge_processor = EdgeProcessor(config, controller, system_monitor)
    
    # Train all models
    edge_processor.train_models(train_windows)
    
    # Calibrate threshold on validation data
    print("\n" + "=" * 80)
    print("THRESHOLD CALIBRATION ON VALIDATION DATA")
    print("=" * 80)
    
    model = edge_processor.models['STANDARD']
    val_scores = model.predict_scores(val_windows)
    
    calibrated_threshold = threshold_calibrator.calibrate(val_labels_adjusted, val_scores)
    validation_f1 = threshold_calibrator.get_validation_f1()
    
    print(f"Calibrated threshold: {calibrated_threshold:.6f}")
    print(f"Validation F1: {validation_f1:.4f}")
    
    # Set threshold in edge processor
    edge_processor.set_threshold(calibrated_threshold)
    print(f"Threshold set in processor: {edge_processor.threshold}")
    print(f"Processor calibrated flag: {edge_processor.calibrated}")
    
    # Quick test: get first test score and check threshold
    first_score = model.predict_scores(test_windows[:1])[0]
    first_prediction = 1 if first_score >= calibrated_threshold else 0
    print(f"\nQuick test on first sample:")
    print(f"  Score: {first_score:.6f}")
    print(f"  Threshold: {calibrated_threshold:.6f}")
    print(f"  Prediction: {first_prediction}")
    print(f"  Score >= threshold: {first_score >= calibrated_threshold}")
    
    # Create data stream
    print("Creating data stream...")
    test_stream = DataStream(test_windows, test_labels_adjusted, buffer_size=1000)
    
    # Set network conditions
    system_monitor.set_simulated_network_conditions(latency=50.0, bandwidth=100.0)
    
    # Start monitoring
    system_monitor.start_monitoring(interval=0.1)
    
    # Process stream with STANDARD mode only (no adaptive switching)
    print("Processing stream with STANDARD mode only...")
    start_time = time.time()
    results = edge_processor.process_stream(test_stream, adaptive=False)  # Disable adaptive
    total_time = time.time() - start_time
    
    # Stop monitoring
    system_monitor.stop_monitoring()
    
    # Calculate metrics
    print("\nCalculating metrics...")
    detection_metrics = metrics_calculator.calculate_detection_metrics(
        results['labels'],
        results['predictions'],
        results['scores']
    )
    
    system_metrics = metrics_calculator.calculate_system_metrics(
        results['latencies'],
        results['cpu_utils'],
        results['mem_utils'],
        edge_processor.stats['data_transmitted'],
        results['latencies']
    )
    
    # Combine results
    all_metrics = {**detection_metrics, **system_metrics}
    all_metrics['total_processing_time'] = float(total_time)
    all_metrics['controller_decisions'] = 0  # No adaptive decisions
    all_metrics['calibrated_threshold'] = float(calibrated_threshold)
    all_metrics['validation_f1'] = float(validation_f1)
    
    # Save results
    results_dir = Path('../../results')
    results_dir.mkdir(exist_ok=True)
    
    output_file = results_dir / 'static_edge_standard.json'
    with open(output_file, 'w') as f:
        json.dump(all_metrics, f, indent=2)
    
    print("\n" + "=" * 80)
    print("STATIC EDGE RESULTS (STANDARD MODE)")
    print("=" * 80)
    print(f"Calibrated threshold: {calibrated_threshold:.6f}")
    print(f"Validation F1: {validation_f1:.4f}")
    print(f"Samples processed: {edge_processor.stats['samples_processed']}")
    print(f"Anomalies detected: {edge_processor.stats['anomalies_detected']}")
    print(f"Data transmitted: {edge_processor.stats['data_transmitted']} bytes")
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
    print(f"  Mean CPU: {system_metrics['cpu_utilization_mean']:.2f}%")
    print(f"  Mean Memory: {system_metrics['memory_utilization_mean']:.2f}%")
    print("=" * 80)
    
    print(f"\nResults saved to {output_file}")


if __name__ == '__main__':
    main()
