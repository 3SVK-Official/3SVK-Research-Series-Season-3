"""
Generate figures and tables for the research paper
"""

import json
import numpy as np
from pathlib import Path
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns


def load_results():
    """Load experiment results"""
    results_dir = Path('results')
    results = {}
    
    for file in results_dir.glob('*.json'):
        with open(file, 'r') as f:
            results[file.stem] = json.load(f)
    
    return results


def generate_benchmark_table(results):
    """Generate benchmark comparison table"""
    print("=" * 60)
    print("BENCHMARK TABLE")
    print("=" * 60)
    
    # Extract key metrics
    methods = ['baseline_centralized', 'baseline_static_edge', 'proposed_adaptive']
    method_names = {
        'baseline_centralized': 'Centralized',
        'baseline_static_edge': 'Static Edge',
        'proposed_adaptive': 'Adaptive Edge (Ours)'
    }
    
    metrics = ['accuracy', 'precision', 'recall', 'f1', 'inference_latency_mean', 
               'cpu_utilization_mean', 'data_transmitted']
    metric_names = {
        'accuracy': 'Accuracy',
        'precision': 'Precision',
        'recall': 'Recall',
        'f1': 'F1-Score',
        'inference_latency_mean': 'Latency (ms)',
        'cpu_utilization_mean': 'CPU (%)',
        'data_transmitted': 'Data (bytes)'
    }
    
    # Create table
    table = []
    for method in methods:
        if method in results:
            row = [method_names[method]]
            for metric in metrics:
                value = results[method].get(metric, 0)
                if metric in ['accuracy', 'precision', 'recall', 'f1']:
                    row.append(f"{value:.4f}")
                elif metric == 'data_transmitted':
                    row.append(f"{value}")
                else:
                    row.append(f"{value:.2f}")
            table.append(row)
    
    # Print table
    header = ['Method'] + [metric_names[m] for m in metrics]
    print("\n" + " | ".join(header))
    print("-" * 80)
    for row in table:
        print(" | ".join(row))
    
    # Calculate improvements
    print("\n" + "=" * 60)
    print("IMPROVEMENTS OVER BASELINES")
    print("=" * 60)
    
    baseline_centralized = results.get('baseline_centralized', {})
    baseline_static_edge = results.get('baseline_static_edge', {})
    proposed = results.get('proposed_adaptive', {})
    
    # Latency improvement
    if baseline_centralized.get('inference_latency_mean', 0) > 0:
        latency_improv = (1 - proposed.get('inference_latency_mean', 0) / baseline_centralized.get('inference_latency_mean', 1)) * 100
        print(f"Latency improvement vs Centralized: {latency_improv:.2f}%")
    
    if baseline_static_edge.get('inference_latency_mean', 0) > 0:
        latency_improv = (1 - proposed.get('inference_latency_mean', 0) / baseline_static_edge.get('inference_latency_mean', 1)) * 100
        print(f"Latency improvement vs Static Edge: {latency_improv:.2f}%")
    
    # CPU improvement
    if baseline_static_edge.get('cpu_utilization_mean', 0) > 0:
        cpu_improv = (1 - proposed.get('cpu_utilization_mean', 0) / baseline_static_edge.get('cpu_utilization_mean', 1)) * 100
        print(f"CPU improvement vs Static Edge: {cpu_improv:.2f}%")
    
    # Data transmission improvement
    if baseline_centralized.get('data_transmitted', 0) > 0:
        data_improv = (1 - proposed.get('data_transmitted', 0) / baseline_centralized.get('data_transmitted', 1)) * 100
        print(f"Data transmission reduction vs Centralized: {data_improv:.2f}%")
    
    # Save table to file
    figures_dir = Path('figures')
    figures_dir.mkdir(exist_ok=True)
    
    table_file = figures_dir / 'benchmark_table.md'
    with open(table_file, 'w') as f:
        f.write("# Benchmark Results\n\n")
        f.write("| Method | " + " | ".join(metric_names[m] for m in metrics) + " |\n")
        f.write("|--------" + "|--------" * len(metrics) + "|\n")
        for row in table:
            f.write("| " + " | ".join(row) + " |\n")
    
    print(f"\nTable saved to {table_file}")


def generate_performance_comparison_plot(results):
    """Generate performance comparison bar chart"""
    figures_dir = Path('figures')
    figures_dir.mkdir(exist_ok=True)
    
    methods = ['baseline_centralized', 'baseline_static_edge', 'proposed_adaptive']
    method_names = ['Centralized', 'Static Edge', 'Adaptive Edge (Ours)']
    
    # Detection metrics
    detection_metrics = ['accuracy', 'precision', 'recall', 'f1']
    metric_labels = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()
    
    for i, (metric, label) in enumerate(zip(detection_metrics, metric_labels)):
        values = [results.get(m, {}).get(metric, 0) for m in methods]
        axes[i].bar(method_names, values, color=['#ff6b6b', '#4ecdc4', '#45b7d1'])
        axes[i].set_title(label)
        axes[i].set_ylim(0, 1)
        axes[i].set_ylabel('Score')
        axes[i].tick_params(axis='x', rotation=15)
    
    plt.tight_layout()
    plt.savefig(figures_dir / 'detection_metrics_comparison.png', dpi=300, bbox_inches='tight')
    print(f"Saved detection metrics comparison to {figures_dir / 'detection_metrics_comparison.png'}")
    plt.close()
    
    # System metrics
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Latency
    latencies = [results.get(m, {}).get('inference_latency_mean', 0) for m in methods]
    axes[0].bar(method_names, latencies, color=['#ff6b6b', '#4ecdc4', '#45b7d1'])
    axes[0].set_title('Mean Latency (ms)')
    axes[0].set_ylabel('Latency (ms)')
    axes[0].tick_params(axis='x', rotation=15)
    
    # CPU
    cpu = [results.get(m, {}).get('cpu_utilization_mean', 0) for m in methods]
    axes[1].bar(method_names, cpu, color=['#ff6b6b', '#4ecdc4', '#45b7d1'])
    axes[1].set_title('Mean CPU Utilization (%)')
    axes[1].set_ylabel('CPU (%)')
    axes[1].tick_params(axis='x', rotation=15)
    
    # Data transmitted
    data = [results.get(m, {}).get('data_transmitted', 0) for m in methods]
    axes[2].bar(method_names, data, color=['#ff6b6b', '#4ecdc4', '#45b7d1'])
    axes[2].set_title('Data Transmitted (bytes)')
    axes[2].set_ylabel('Bytes')
    axes[2].tick_params(axis='x', rotation=15)
    
    plt.tight_layout()
    plt.savefig(figures_dir / 'system_metrics_comparison.png', dpi=300, bbox_inches='tight')
    print(f"Saved system metrics comparison to {figures_dir / 'system_metrics_comparison.png'}")
    plt.close()


def generate_ablation_table(results):
    """Generate ablation study table"""
    ablation_file = Path('results/ablation_results.json')
    if not ablation_file.exists():
        print("Ablation results not found")
        return
    
    with open(ablation_file, 'r') as f:
        ablation_results = json.load(f)
    
    print("\n" + "=" * 60)
    print("ABLATION STUDY TABLE")
    print("=" * 60)
    
    variants = ['full_adaptive', 'no_adaptive', 'no_transmission_opt', 'no_resource_aware']
    variant_names = {
        'full_adaptive': 'Full Adaptive',
        'no_adaptive': 'No Adaptation',
        'no_transmission_opt': 'No Trans. Opt.',
        'no_resource_aware': 'No Resource Aware'
    }
    
    metrics = ['f1', 'inference_latency_mean', 'cpu_utilization_mean']
    metric_names = {
        'f1': 'F1-Score',
        'inference_latency_mean': 'Latency (ms)',
        'cpu_utilization_mean': 'CPU (%)'
    }
    
    # Create table
    table = []
    for variant in variants:
        if variant in ablation_results:
            row = [variant_names[variant]]
            for metric in metrics:
                value = ablation_results[variant].get(metric, 0)
                if metric == 'f1':
                    row.append(f"{value:.4f}")
                else:
                    row.append(f"{value:.2f}")
            table.append(row)
    
    # Print table
    header = ['Variant'] + [metric_names[m] for m in metrics]
    print("\n" + " | ".join(header))
    print("-" * 60)
    for row in table:
        print(" | ".join(row))
    
    # Save table
    figures_dir = Path('figures')
    figures_dir.mkdir(exist_ok=True)
    
    table_file = figures_dir / 'ablation_table.md'
    with open(table_file, 'w') as f:
        f.write("# Ablation Study Results\n\n")
        f.write("| Variant | " + " | ".join(metric_names[m] for m in metrics) + " |\n")
        f.write("|---------" + "|--------" * len(metrics) + "|\n")
        for row in table:
            f.write("| " + " | ".join(row) + " |\n")
    
    print(f"\nAblation table saved to {table_file}")


def generate_summary_report(results):
    """Generate summary report with all results"""
    figures_dir = Path('figures')
    figures_dir.mkdir(exist_ok=True)
    
    report_file = figures_dir / 'summary_report.md'
    
    with open(report_file, 'w') as f:
        f.write("# Experimental Results Summary\n\n")
        f.write("## Overview\n")
        f.write("This document summarizes the experimental results for the Adaptive Edge-AI Framework for Real-Time Anomaly Detection.\n\n")
        
        f.write("## Benchmark Results\n\n")
        f.write("### Detection Performance\n")
        f.write("- **Centralized Baseline**: All data transmitted to cloud for processing\n")
        f.write("- **Static Edge Baseline**: Fixed local processing with STANDARD model\n")
        f.write("- **Adaptive Edge (Proposed)**: Dynamic resource-aware processing\n\n")
        
        f.write("### Key Findings\n\n")
        
        baseline_centralized = results.get('baseline_centralized', {})
        baseline_static_edge = results.get('baseline_static_edge', {})
        proposed = results.get('proposed_adaptive', {})
        
        f.write(f"- **Latency**: Adaptive edge achieves {proposed.get('inference_latency_mean', 0):.2f}ms average latency, ")
        f.write(f"compared to {baseline_centralized.get('inference_latency_mean', 0):.2f}ms for centralized ")
        f.write(f"and {baseline_static_edge.get('inference_latency_mean', 0):.2f}ms for static edge.\n\n")
        
        f.write(f"- **CPU Utilization**: Adaptive edge uses {proposed.get('cpu_utilization_mean', 0):.2f}% CPU on average, ")
        f.write(f"compared to {baseline_static_edge.get('cpu_utilization_mean', 0):.2f}% for static edge.\n\n")
        
        f.write(f"- **Data Transmission**: Adaptive edge transmits {proposed.get('data_transmitted', 0)} bytes, ")
        f.write(f"compared to {baseline_centralized.get('data_transmitted', 0)} bytes for centralized.\n\n")
        
        f.write(f"- **Detection Performance**: F1-Score of {proposed.get('f1', 0):.4f} for adaptive edge, ")
        f.write(f"compared to {baseline_centralized.get('f1', 0):.4f} for centralized ")
        f.write(f"and {baseline_static_edge.get('f1', 0):.4f} for static edge.\n\n")
    
    print(f"Summary report saved to {report_file}")


def main():
    """Main function to generate all figures and tables"""
    print("=" * 60)
    print("GENERATING FIGURES AND TABLES")
    print("=" * 60)
    
    results = load_results()
    
    if not results:
        print("No results found. Run experiments first.")
        return
    
    generate_benchmark_table(results)
    generate_performance_comparison_plot(results)
    generate_ablation_table(results)
    generate_summary_report(results)
    
    print("\n" + "=" * 60)
    print("FIGURES AND TABLES GENERATION COMPLETE")
    print("=" * 60)


if __name__ == '__main__':
    main()
