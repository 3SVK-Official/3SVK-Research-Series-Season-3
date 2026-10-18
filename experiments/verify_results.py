"""
Result verification script - Regenerate and verify all experiment results
"""

import sys
import yaml
import numpy as np
from pathlib import Path
import json

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data.loader import DataLoader
from src.data.stream import DataStream
from src.preprocessing.preprocessor import Preprocessor
from src.edge.processor import EdgeProcessor
from src.cloud.coordinator import CloudCoordinator
from src.adaptive.controller import AdaptiveController
from src.evaluation.system_monitor import SystemMonitor
from src.evaluation.metrics import MetricsCalculator


def load_config(config_path: str = 'configs/default_config.yaml') -> dict:
    """Load configuration"""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def verify_metrics_calculation():
    """Verify metrics calculation is correct"""
    print("=" * 60)
    print("METRICS CALCULATION VERIFICATION")
    print("=" * 60)
    
    # Create synthetic labels and predictions
    y_true = np.array([0, 0, 0, 1, 1, 1, 0, 1, 0, 1])
    y_pred = np.array([0, 0, 1, 1, 1, 0, 0, 1, 0, 0])
    y_scores = np.array([0.1, 0.2, 0.8, 0.9, 0.7, 0.3, 0.1, 0.8, 0.2, 0.4])
    
    config = load_config()
    metrics_calc = MetricsCalculator(config)
    
    metrics = metrics_calc.calculate_detection_metrics(y_true, y_pred, y_scores)
    
    # Manual calculation
    tp = np.sum((y_true == 1) & (y_pred == 1))
    tn = np.sum((y_true == 0) & (y_pred == 0))
    fp = np.sum((y_true == 0) & (y_pred == 1))
    fn = np.sum((y_true == 1) & (y_pred == 0))
    
    manual_accuracy = (tp + tn) / (tp + tn + fp + fn)
    manual_precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    manual_recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    manual_f1 = 2 * (manual_precision * manual_recall) / (manual_precision + manual_recall) if (manual_precision + manual_recall) > 0 else 0
    
    print(f"\nConfusion Matrix:")
    print(f"  TP: {tp}, TN: {tn}, FP: {fp}, FN: {fn}")
    print(f"\nManual Calculation:")
    print(f"  Accuracy: {manual_accuracy:.4f}")
    print(f"  Precision: {manual_precision:.4f}")
    print(f"  Recall: {manual_recall:.4f}")
    print(f"  F1-Score: {manual_f1:.4f}")
    print(f"\nMetrics Calculator:")
    print(f"  Accuracy: {metrics['accuracy']:.4f}")
    print(f"  Precision: {metrics['precision']:.4f}")
    print(f"  Recall: {metrics['recall']:.4f}")
    print(f"  F1-Score: {metrics['f1']:.4f}")
    
    # Verify
    assert abs(metrics['accuracy'] - manual_accuracy) < 0.0001, "Accuracy mismatch"
    assert abs(metrics['precision'] - manual_precision) < 0.0001, "Precision mismatch"
    assert abs(metrics['recall'] - manual_recall) < 0.0001, "Recall mismatch"
    assert abs(metrics['f1'] - manual_f1) < 0.0001, "F1 mismatch"
    
    print("\n✓ Metrics calculation verified")
    return True


def run_all_experiments():
    """Run all experiments and save results"""
    print("\n" + "=" * 60)
    print("RUNNING ALL EXPERIMENTS")
    print("=" * 60)
    
    config = load_config()
    np.random.seed(config['experiments']['random_seed'])
    
    # Setup
    data_loader = DataLoader(config)
    preprocessor = Preprocessor(config)
    system_monitor = SystemMonitor()
    metrics_calculator = MetricsCalculator(config)
    
    # Load dataset
    print("\nLoading dataset...")
    data, labels = data_loader.load_dataset('synthetic', n_samples=5000, anomaly_ratio=0.05)
    train_data, test_data, train_labels, test_labels = data_loader.train_test_split(data, labels, test_ratio=0.2)
    
    # Preprocess
    print("Preprocessing data...")
    train_windows = preprocessor.fit_transform(train_data)
    test_windows = preprocessor.transform(test_data)
    window_size = config['data']['window_size']
    test_labels_adjusted = test_labels[window_size-1:]
    
    results = {}
    
    # Baseline A: Centralized
    print("\n--- BASELINE A: CENTRALIZED ---")
    cloud_coordinator = CloudCoordinator(config, system_monitor)
    cloud_coordinator.set_network_conditions(latency=50.0, bandwidth=100.0)
    cloud_coordinator.train_model(train_windows)
    
    test_stream = DataStream(test_windows, test_labels_adjusted, buffer_size=1000)
    cloud_results = cloud_coordinator.process_stream(test_stream)
    
    detection_metrics = metrics_calculator.calculate_detection_metrics(
        cloud_results['labels'], cloud_results['predictions'], cloud_results['scores']
    )
    system_metrics = metrics_calculator.calculate_system_metrics(
        cloud_results['latencies'], [0]*len(cloud_results['latencies']), 
        [0]*len(cloud_results['latencies']), cloud_coordinator.stats['total_data_transmitted'],
        cloud_results['latencies']
    )
    results['baseline_centralized'] = {**detection_metrics, **system_metrics}
    results['baseline_centralized']['samples_processed'] = cloud_coordinator.stats['samples_processed']
    results['baseline_centralized']['anomalies_detected'] = cloud_coordinator.stats['anomalies_detected']
    
    # Baseline B: Static Edge
    print("\n--- BASELINE B: STATIC EDGE ---")
    controller = AdaptiveController(config)
    edge_processor = EdgeProcessor(config, controller, system_monitor)
    edge_processor.train_models(train_windows)
    
    test_stream = DataStream(test_windows, test_labels_adjusted, buffer_size=1000)
    system_monitor.start_monitoring(interval=0.1)
    edge_results = edge_processor.process_stream(test_stream, adaptive=False)
    system_monitor.stop_monitoring()
    
    detection_metrics = metrics_calculator.calculate_detection_metrics(
        edge_results['labels'], edge_results['predictions'], edge_results['scores']
    )
    system_metrics = metrics_calculator.calculate_system_metrics(
        edge_results['latencies'], edge_results['cpu_utils'], edge_results['mem_utils'],
        edge_processor.stats['data_transmitted'], edge_results['latencies']
    )
    results['baseline_static_edge'] = {**detection_metrics, **system_metrics}
    results['baseline_static_edge']['samples_processed'] = edge_processor.stats['samples_processed']
    results['baseline_static_edge']['anomalies_detected'] = edge_processor.stats['anomalies_detected']
    
    # Proposed: Adaptive
    print("\n--- PROPOSED: ADAPTIVE ---")
    controller = AdaptiveController(config)
    edge_processor = EdgeProcessor(config, controller, system_monitor)
    edge_processor.train_models(train_windows)
    
    test_stream = DataStream(test_windows, test_labels_adjusted, buffer_size=1000)
    system_monitor.set_simulated_network_conditions(latency=50.0, bandwidth=100.0)
    system_monitor.start_monitoring(interval=0.1)
    adaptive_results = edge_processor.process_stream(test_stream, adaptive=True)
    system_monitor.stop_monitoring()
    
    detection_metrics = metrics_calculator.calculate_detection_metrics(
        adaptive_results['labels'], adaptive_results['predictions'], adaptive_results['scores']
    )
    system_metrics = metrics_calculator.calculate_system_metrics(
        adaptive_results['latencies'], adaptive_results['cpu_utils'], adaptive_results['mem_utils'],
        edge_processor.stats['data_transmitted'], adaptive_results['latencies']
    )
    results['proposed_adaptive'] = {**detection_metrics, **system_metrics}
    results['proposed_adaptive']['samples_processed'] = edge_processor.stats['samples_processed']
    results['proposed_adaptive']['anomalies_detected'] = edge_processor.stats['anomalies_detected']
    results['proposed_adaptive']['controller_decisions'] = controller.decision_count
    
    # Save results
    results_dir = Path('results')
    results_dir.mkdir(exist_ok=True)
    
    for name, metrics in results.items():
        output_file = results_dir / f'{name}.json'
        with open(output_file, 'w') as f:
            json.dump(metrics, f, indent=2)
        print(f"Saved {output_file}")
    
    return results


def main():
    """Main verification function"""
    verify_metrics_calculation()
    results = run_all_experiments()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    for name, metrics in results.items():
        print(f"\n{name}:")
        print(f"  F1-Score: {metrics['f1']:.4f}")
        print(f"  Mean latency: {metrics['inference_latency_mean']:.2f} ms")
        print(f"  Mean CPU: {metrics.get('cpu_utilization_mean', 0):.2f}%")
        print(f"  Data transmitted: {metrics.get('data_transmitted', 0)} bytes")


if __name__ == '__main__':
    main()
