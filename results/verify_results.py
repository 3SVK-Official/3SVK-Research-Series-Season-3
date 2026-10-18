"""
Results Verification Script

This script verifies the consistency and correctness of experimental results.
It loads the final results and performs sanity checks on calculations.
"""

import json
import sys
from pathlib import Path


def load_results(results_path: str) -> dict:
    """Load results from JSON file"""
    with open(results_path, 'r') as f:
        return json.load(f)


def verify_detection_metrics(metrics: dict, name: str) -> bool:
    """Verify detection metrics are internally consistent"""
    tp = metrics['true_positive']
    tn = metrics['true_negative']
    fp = metrics['false_positive']
    fn = metrics['false_negative']
    
    # Calculate derived metrics
    total = tp + tn + fp + fn
    if total == 0:
        print(f"ERROR [{name}]: Total samples is zero")
        return False
    
    calculated_accuracy = (tp + tn) / total
    calculated_precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    calculated_recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    calculated_f1 = 2 * (calculated_precision * calculated_recall) / (calculated_precision + calculated_recall) if (calculated_precision + calculated_recall) > 0 else 0
    calculated_fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
    calculated_fnr = fn / (fn + tp) if (fn + tp) > 0 else 0
    
    # Check consistency (allow small floating point errors)
    tolerance = 0.001
    
    if abs(calculated_accuracy - metrics['accuracy']) > tolerance:
        print(f"ERROR [{name}]: Accuracy mismatch. Calculated: {calculated_accuracy:.4f}, Reported: {metrics['accuracy']:.4f}")
        return False
    
    if abs(calculated_precision - metrics['precision']) > tolerance:
        print(f"ERROR [{name}]: Precision mismatch. Calculated: {calculated_precision:.4f}, Reported: {metrics['precision']:.4f}")
        return False
    
    if abs(calculated_recall - metrics['recall']) > tolerance:
        print(f"ERROR [{name}]: Recall mismatch. Calculated: {calculated_recall:.4f}, Reported: {metrics['recall']:.4f}")
        return False
    
    if abs(calculated_f1 - metrics['f1']) > tolerance:
        print(f"ERROR [{name}]: F1 mismatch. Calculated: {calculated_f1:.4f}, Reported: {metrics['f1']:.4f}")
        return False
    
    if abs(calculated_fpr - metrics['false_positive_rate']) > tolerance:
        print(f"ERROR [{name}]: FPR mismatch. Calculated: {calculated_fpr:.4f}, Reported: {metrics['false_positive_rate']:.4f}")
        return False
    
    if abs(calculated_fnr - metrics['false_negative_rate']) > tolerance:
        print(f"ERROR [{name}]: FNR mismatch. Calculated: {calculated_fnr:.4f}, Reported: {metrics['false_negative_rate']:.4f}")
        return False
    
    print(f"PASS [{name}]: Detection metrics are consistent")
    return True


def verify_system_metrics(metrics: dict, name: str) -> bool:
    """Verify system metrics are reasonable"""
    # Check latency is positive
    if metrics['inference_latency_mean_ms'] <= 0:
        print(f"ERROR [{name}]: Mean latency is not positive: {metrics['inference_latency_mean_ms']}")
        return False
    
    # Check CPU is in valid range [0, 100]
    if not (0 <= metrics['cpu_utilization_mean_percent'] <= 100):
        print(f"ERROR [{name}]: CPU utilization out of range: {metrics['cpu_utilization_mean_percent']}")
        return False
    
    # Check memory is in valid range [0, 100]
    if not (0 <= metrics['memory_utilization_mean_percent'] <= 100):
        print(f"ERROR [{name}]: Memory utilization out of range: {metrics['memory_utilization_mean_percent']}")
        return False
    
    # Check data transmitted is non-negative
    if metrics['data_transmitted_bytes'] < 0:
        print(f"ERROR [{name}]: Data transmitted is negative: {metrics['data_transmitted_bytes']}")
        return False
    
    # Check processing time is positive
    if metrics['total_processing_time_seconds'] <= 0:
        print(f"ERROR [{name}]: Total processing time is not positive: {metrics['total_processing_time_seconds']}")
        return False
    
    print(f"PASS [{name}]: System metrics are reasonable")
    return True


def verify_improvement_calculations(results: dict) -> bool:
    """Verify percentage improvement calculations"""
    comparisons = results['comparisons']
    
    # Verify latency reduction
    centralized_latency = results['baselines']['centralized']['system_metrics']['inference_latency_mean_ms']
    static_edge_latency = results['baselines']['static_edge']['system_metrics']['inference_latency_mean_ms']
    adaptive_edge_latency = results['baselines']['adaptive_edge']['system_metrics']['inference_latency_mean_ms']
    
    calculated_static_reduction = ((centralized_latency - static_edge_latency) / centralized_latency) * 100
    calculated_adaptive_reduction = ((centralized_latency - adaptive_edge_latency) / centralized_latency) * 100
    
    tolerance = 0.1
    
    if abs(calculated_static_reduction - comparisons['edge_vs_centralized_latency_reduction']['static_edge_percent']) > tolerance:
        print(f"ERROR: Static edge latency reduction mismatch. Calculated: {calculated_static_reduction:.2f}%, Reported: {comparisons['edge_vs_centralized_latency_reduction']['static_edge_percent']:.2f}%")
        return False
    
    if abs(calculated_adaptive_reduction - comparisons['edge_vs_centralized_latency_reduction']['adaptive_edge_percent']) > tolerance:
        print(f"ERROR: Adaptive edge latency reduction mismatch. Calculated: {calculated_adaptive_reduction:.2f}%, Reported: {comparisons['edge_vs_centralized_latency_reduction']['adaptive_edge_percent']:.2f}%")
        return False
    
    # Verify data reduction
    centralized_data = results['baselines']['centralized']['system_metrics']['data_transmitted_bytes']
    static_edge_data = results['baselines']['static_edge']['system_metrics']['data_transmitted_bytes']
    adaptive_edge_data = results['baselines']['adaptive_edge']['system_metrics']['data_transmitted_bytes']
    
    calculated_static_data_reduction = ((centralized_data - static_edge_data) / centralized_data) * 100
    calculated_adaptive_data_reduction = ((centralized_data - adaptive_edge_data) / centralized_data) * 100
    
    if abs(calculated_static_data_reduction - comparisons['edge_vs_centralized_data_reduction']['static_edge_percent']) > tolerance:
        print(f"ERROR: Static edge data reduction mismatch. Calculated: {calculated_static_data_reduction:.2f}%, Reported: {comparisons['edge_vs_centralized_data_reduction']['static_edge_percent']:.2f}%")
        return False
    
    if abs(calculated_adaptive_data_reduction - comparisons['edge_vs_centralized_data_reduction']['adaptive_edge_percent']) > tolerance:
        print(f"ERROR: Adaptive edge data reduction mismatch. Calculated: {calculated_adaptive_data_reduction:.2f}%, Reported: {comparisons['edge_vs_centralized_data_reduction']['adaptive_edge_percent']:.2f}%")
        return False
    
    print("PASS: Improvement calculations are consistent")
    return True


def verify_calibration(results: dict) -> bool:
    """Verify threshold calibration was performed"""
    for baseline_name, baseline_data in results['baselines'].items():
        if 'calibration' not in baseline_data:
            print(f"ERROR [{baseline_name}]: Missing calibration data")
            return False
        
        if 'calibrated_threshold' not in baseline_data['calibration']:
            print(f"ERROR [{baseline_name}]: Missing calibrated threshold")
            return False
        
        if 'validation_f1' not in baseline_data['calibration']:
            print(f"ERROR [{baseline_name}]: Missing validation F1")
            return False
        
        # Check threshold is in reasonable range
        threshold = baseline_data['calibration']['calibrated_threshold']
        if not (0 <= threshold <= 1):
            print(f"WARNING [{baseline_name}]: Threshold outside [0,1] range: {threshold}")
        
        # Check validation F1 is in valid range
        val_f1 = baseline_data['calibration']['validation_f1']
        if not (0 <= val_f1 <= 1):
            print(f"ERROR [{baseline_name}]: Validation F1 outside [0,1] range: {val_f1}")
            return False
    
    print("PASS: All baselines have calibration data")
    return True


def verify_no_hardcoded_cpu(results: dict) -> bool:
    """Verify CPU is not hardcoded to 0.0 (except for min values which can be 0)"""
    for baseline_name, baseline_data in results['baselines'].items():
        cpu_mean = baseline_data['system_metrics']['cpu_utilization_mean_percent']
        cpu_max = baseline_data['system_metrics']['cpu_utilization_max_percent']
        
        # Mean should not be 0.0 (unless truly idle)
        if cpu_mean == 0.0 and baseline_name != 'centralized':
            print(f"WARNING [{baseline_name}]: CPU mean is 0.0, may be hardcoded")
        
        # Max should not be 0.0
        if cpu_max == 0.0:
            print(f"ERROR [{baseline_name}]: CPU max is 0.0, likely hardcoded")
            return False
    
    print("PASS: CPU values are not hardcoded to 0.0")
    return True


def main():
    """Main verification function"""
    results_path = Path(__file__).parent / 'final_results.json'
    
    if not results_path.exists():
        print(f"ERROR: Results file not found at {results_path}")
        sys.exit(1)
    
    print("=" * 60)
    print("RESULTS VERIFICATION")
    print("=" * 60)
    
    results = load_results(results_path)
    
    all_passed = True
    
    # Verify each baseline
    for baseline_name, baseline_data in results['baselines'].items():
        print(f"\nVerifying {baseline_name}...")
        
        if not verify_detection_metrics(baseline_data['detection_metrics'], baseline_name):
            all_passed = False
        
        if not verify_system_metrics(baseline_data['system_metrics'], baseline_name):
            all_passed = False
    
    # Verify comparisons
    print("\nVerifying improvement calculations...")
    if not verify_improvement_calculations(results):
        all_passed = False
    
    # Verify calibration
    print("\nVerifying calibration...")
    if not verify_calibration(results):
        all_passed = False
    
    # Verify no hardcoded CPU
    print("\nVerifying CPU measurements...")
    if not verify_no_hardcoded_cpu(results):
        all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("VERIFICATION PASSED: All checks passed")
        print("=" * 60)
        sys.exit(0)
    else:
        print("VERIFICATION FAILED: Some checks failed")
        print("=" * 60)
        sys.exit(1)


if __name__ == '__main__':
    main()
