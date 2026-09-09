"""
Ablation Study: Evaluate contribution of adaptive components
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
from src.edge.processor import EdgeProcessor
from src.adaptive.controller import AdaptiveController
from src.evaluation.system_monitor import SystemMonitor
from src.evaluation.metrics import MetricsCalculator
import json
import time


def load_config(config_path: str = 'configs/default_config.yaml') -> dict:
    """Load configuration"""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def run_ablation_experiment(ablation_type: str, config: dict) -> dict:
    """
    Run ablation experiment
    
    Args:
        ablation_type: Type of ablation ('no_adaptive', 'no_transmission_opt', 'no_resource_aware')
        config: Configuration dictionary
        
    Returns:
        Results dictionary
    """
    print(f"\n{'=' * 60}")
    print(f"ABLATION: {ablation_type}")
    print('=' * 60)
    
    # Set random seed
    np.random.seed(config['experiments']['random_seed'])
    
    # Initialize components
    data_loader = DataLoader(config)
    preprocessor = Preprocessor(config)
    system_monitor = SystemMonitor()
    controller = AdaptiveController(config)
    metrics_calculator = MetricsCalculator(config)
    
    # Load dataset
    print("Loading dataset...")
    data, labels = data_loader.load_dataset('synthetic', n_samples=5000, anomaly_ratio=0.05)
    
    # Train/test split
    train_data, test_data, train_labels, test_labels = data_loader.train_test_split(
        data, labels, test_ratio=0.2
    )
    
    # Preprocess
    print("Preprocessing data...")
    train_windows = preprocessor.fit_transform(train_data)
    test_windows = preprocessor.transform(test_data)
    
    # Adjust labels
    window_size = config['data']['window_size']
    test_labels_adjusted = test_labels[window_size-1:]
    
    # Initialize edge processor
    edge_processor = EdgeProcessor(config, controller, system_monitor)
    edge_processor.train_models(train_windows)
    
    # Create stream
    test_stream = DataStream(test_windows, test_labels_adjusted, buffer_size=1000)
    
    # Set network conditions
    system_monitor.set_simulated_network_conditions(latency=50.0, bandwidth=100.0)
    
    # Start monitoring
    system_monitor.start_monitoring(interval=0.1)
    
    # Configure ablation
    adaptive = True
    if ablation_type == 'no_adaptive':
        adaptive = False
        print("Ablation: Disabled adaptive controller (static mode)")
    elif ablation_type == 'no_transmission_opt':
        # Modify controller to always transmit
        original_decide = controller.decide
        controller.decide = lambda: ('STANDARD', 'TRANSMIT')
        print("Ablation: Disabled transmission optimization (always transmit)")
    elif ablation_type == 'no_resource_aware':
        # Modify controller to ignore resource constraints
        original_check_feasibility = controller.check_feasibility
        controller.check_feasibility = lambda mode, transmit: True
        print("Ablation: Disabled resource awareness (ignore constraints)")
    
    # Process stream
    print("Processing stream...")
    start_time = time.time()
    results = edge_processor.process_stream(test_stream, adaptive=adaptive)
    total_time = time.time() - start_time
    
    # Stop monitoring
    system_monitor.stop_monitoring()
    
    # Calculate metrics
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
    
    all_metrics = {**detection_metrics, **system_metrics}
    all_metrics['total_processing_time'] = total_time
    all_metrics['ablation_type'] = ablation_type
    
    print(f"\n{ablation_type} Results:")
    print(f"  F1-Score: {detection_metrics['f1']:.4f}")
    print(f"  Mean latency: {system_metrics['inference_latency_mean']:.2f} ms")
    print(f"  Data transmitted: {edge_processor.stats['data_transmitted']} bytes")
    
    return all_metrics


def main():
    """Run all ablation experiments"""
    print("=" * 60)
    print("ABLATION STUDY")
    print("=" * 60)
    
    # Load config
    config = load_config()
    
    # Ablation configurations
    ablations = [
        'full_adaptive',  # Full system (reference)
        'no_adaptive',    # Without adaptive controller
        'no_transmission_opt',  # Without transmission optimization
        'no_resource_aware'     # Without resource awareness
    ]
    
    all_results = {}
    
    for ablation in ablations:
        if ablation == 'full_adaptive':
            # Run full adaptive system (same as proposed)
            from experiments.proposed.run import main as run_proposed
            # Import and run proposed method
            # For simplicity, we'll run it inline
            from src.data.loader import DataLoader
            from src.data.stream import DataStream
            from src.preprocessing.preprocessor import Preprocessor
            from src.edge.processor import EdgeProcessor
            from src.adaptive.controller import AdaptiveController
            from src.evaluation.system_monitor import SystemMonitor
            from src.evaluation.metrics import MetricsCalculator
            import time
            
            np.random.seed(config['experiments']['random_seed'])
            data_loader = DataLoader(config)
            preprocessor = Preprocessor(config)
            system_monitor = SystemMonitor()
            controller = AdaptiveController(config)
            metrics_calculator = MetricsCalculator(config)
            
            data, labels = data_loader.load_dataset('synthetic', n_samples=5000, anomaly_ratio=0.05)
            train_data, test_data, train_labels, test_labels = data_loader.train_test_split(data, labels, test_ratio=0.2)
            train_windows = preprocessor.fit_transform(train_data)
            test_windows = preprocessor.transform(test_data)
            
            window_size = config['data']['window_size']
            test_labels_adjusted = test_labels[window_size-1:]
            
            edge_processor = EdgeProcessor(config, controller, system_monitor)
            edge_processor.train_models(train_windows)
            test_stream = DataStream(test_windows, test_labels_adjusted, buffer_size=1000)
            system_monitor.set_simulated_network_conditions(latency=50.0, bandwidth=100.0)
            system_monitor.start_monitoring(interval=0.1)
            
            start_time = time.time()
            results = edge_processor.process_stream(test_stream, adaptive=True)
            total_time = time.time() - start_time
            system_monitor.stop_monitoring()
            
            detection_metrics = metrics_calculator.calculate_detection_metrics(
                results['labels'], results['predictions'], results['scores']
            )
            system_metrics = metrics_calculator.calculate_system_metrics(
                results['latencies'], results['cpu_utils'], results['mem_utils'],
                edge_processor.stats['data_transmitted'], results['latencies']
            )
            
            all_results['full_adaptive'] = {**detection_metrics, **system_metrics}
            all_results['full_adaptive']['total_processing_time'] = total_time
        else:
            all_results[ablation] = run_ablation_experiment(ablation, config)
    
    # Save results
    results_dir = Path('../../results')
    results_dir.mkdir(exist_ok=True)
    
    output_file = results_dir / 'ablation_results.json'
    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print("\n" + "=" * 60)
    print("ABLATION STUDY SUMMARY")
    print("=" * 60)
    
    for ablation, metrics in all_results.items():
        print(f"\n{ablation}:")
        print(f"  F1-Score: {metrics['f1']:.4f}")
        print(f"  Mean latency: {metrics['inference_latency_mean']:.2f} ms")
        print(f"  Mean CPU: {metrics['cpu_utilization_mean']:.2f}%")
        print(f"  Data transmitted: {metrics.get('data_transmitted', 0)} bytes")
    
    print(f"\nResults saved to {output_file}")


if __name__ == '__main__':
    main()
