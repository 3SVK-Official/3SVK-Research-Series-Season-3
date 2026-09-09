"""
Metrics calculator for evaluation
"""

import numpy as np
from typing import Dict, List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MetricsCalculator:
    """
    Calculates detection and system metrics
    """
    
    def __init__(self, config: dict):
        """
        Initialize metrics calculator
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.metrics_config = config.get('evaluation', {}).get('metrics', [])
        
    def calculate_detection_metrics(self, y_true: np.ndarray, y_pred: np.ndarray, 
                                     y_scores: Optional[np.ndarray] = None) -> Dict[str, float]:
        """
        Calculate detection metrics (implemented manually to avoid sklearn dependency)
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            y_scores: Predicted scores (for AUC calculations)
            
        Returns:
            Dictionary of metrics
        """
        metrics = {}
        
        # Confusion matrix components
        tp = np.sum((y_true == 1) & (y_pred == 1))
        tn = np.sum((y_true == 0) & (y_pred == 0))
        fp = np.sum((y_true == 0) & (y_pred == 1))
        fn = np.sum((y_true == 1) & (y_pred == 0))
        
        metrics['true_positive'] = int(tp)
        metrics['true_negative'] = int(tn)
        metrics['false_positive'] = int(fp)
        metrics['false_negative'] = int(fn)
        
        # Basic metrics
        total = tp + tn + fp + fn
        metrics['accuracy'] = float((tp + tn) / total if total > 0 else 0.0)
        
        metrics['precision'] = float(tp / (tp + fp) if (tp + fp) > 0 else 0.0)
        metrics['recall'] = float(tp / (tp + fn) if (tp + fn) > 0 else 0.0)
        
        if metrics['precision'] + metrics['recall'] > 0:
            metrics['f1'] = float(2 * (metrics['precision'] * metrics['recall']) / (metrics['precision'] + metrics['recall']))
        else:
            metrics['f1'] = 0.0
        
        # Rates
        metrics['false_positive_rate'] = float(fp / (fp + tn) if (fp + tn) > 0 else 0.0)
        metrics['false_negative_rate'] = float(fn / (fn + tp) if (fn + tp) > 0 else 0.0)
        
        # AUC metrics (simplified implementation)
        if y_scores is not None:
            try:
                metrics['roc_auc'] = float(self._calculate_roc_auc(y_true, y_scores))
            except:
                metrics['roc_auc'] = 0.0
            
            try:
                metrics['pr_auc'] = float(self._calculate_pr_auc(y_true, y_scores))
            except:
                metrics['pr_auc'] = 0.0
        
        return metrics
    
    def _calculate_roc_auc(self, y_true: np.ndarray, y_scores: np.ndarray) -> float:
        """Calculate ROC AUC manually"""
        # Sort by scores
        indices = np.argsort(y_scores)[::-1]
        y_true_sorted = y_true[indices]
        
        # Calculate TPR and FPR at each threshold
        n_pos = np.sum(y_true == 1)
        n_neg = np.sum(y_true == 0)
        
        if n_pos == 0 or n_neg == 0:
            return 0.0
        
        tp = 0
        fp = 0
        auc = 0.0
        prev_fpr = 0.0
        prev_tpr = 0.0
        
        for i in range(len(y_true_sorted)):
            if y_true_sorted[i] == 1:
                tp += 1
            else:
                fp += 1
            
            tpr = tp / n_pos
            fpr = fp / n_neg
            
            # Trapezoidal integration
            auc += (fpr - prev_fpr) * (tpr + prev_tpr) / 2
            prev_fpr = fpr
            prev_tpr = tpr
        
        return auc
    
    def _calculate_pr_auc(self, y_true: np.ndarray, y_scores: np.ndarray) -> float:
        """Calculate PR AUC manually"""
        # Sort by scores
        indices = np.argsort(y_scores)[::-1]
        y_true_sorted = y_true[indices]
        
        # Calculate precision and recall at each threshold
        n_pos = np.sum(y_true == 1)
        
        if n_pos == 0:
            return 0.0
        
        tp = 0
        fp = 0
        auc = 0.0
        prev_recall = 0.0
        prev_precision = 1.0
        
        for i in range(len(y_true_sorted)):
            if y_true_sorted[i] == 1:
                tp += 1
            else:
                fp += 1
            
            recall = tp / n_pos
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
            
            # Trapezoidal integration
            auc += (recall - prev_recall) * (precision + prev_precision) / 2
            prev_recall = recall
            prev_precision = precision
        
        return auc
    
    def calculate_system_metrics(self, latencies: List[float], cpu_utils: List[float],
                                   mem_utils: List[float], data_transmitted: int,
                                   processing_times: List[float]) -> Dict[str, float]:
        """
        Calculate system metrics
        
        Args:
            latencies: List of inference latencies (ms)
            cpu_utils: List of CPU utilizations (%)
            mem_utils: List of memory utilizations (%)
            data_transmitted: Total data transmitted (bytes)
            processing_times: List of processing times (ms)
            
        Returns:
            Dictionary of system metrics
        """
        metrics = {}
        
        # Latency metrics
        if latencies:
            metrics['inference_latency_mean'] = float(np.mean(latencies))
            metrics['inference_latency_std'] = float(np.std(latencies))
            metrics['inference_latency_min'] = float(np.min(latencies))
            metrics['inference_latency_max'] = float(np.max(latencies))
            metrics['inference_latency_p50'] = float(np.percentile(latencies, 50))
            metrics['inference_latency_p95'] = float(np.percentile(latencies, 95))
            metrics['inference_latency_p99'] = float(np.percentile(latencies, 99))
        else:
            metrics['inference_latency_mean'] = 0.0
            metrics['inference_latency_std'] = 0.0
            metrics['inference_latency_min'] = 0.0
            metrics['inference_latency_max'] = 0.0
            metrics['inference_latency_p50'] = 0.0
            metrics['inference_latency_p95'] = 0.0
            metrics['inference_latency_p99'] = 0.0
        
        # CPU metrics
        if cpu_utils:
            metrics['cpu_utilization_mean'] = float(np.mean(cpu_utils))
            metrics['cpu_utilization_std'] = float(np.std(cpu_utils))
            metrics['cpu_utilization_min'] = float(np.min(cpu_utils))
            metrics['cpu_utilization_max'] = float(np.max(cpu_utils))
        else:
            metrics['cpu_utilization_mean'] = 0.0
            metrics['cpu_utilization_std'] = 0.0
            metrics['cpu_utilization_min'] = 0.0
            metrics['cpu_utilization_max'] = 0.0
        
        # Memory metrics
        if mem_utils:
            metrics['memory_utilization_mean'] = float(np.mean(mem_utils))
            metrics['memory_utilization_std'] = float(np.std(mem_utils))
            metrics['memory_utilization_min'] = float(np.min(mem_utils))
            metrics['memory_utilization_max'] = float(np.max(mem_utils))
        else:
            metrics['memory_utilization_mean'] = 0.0
            metrics['memory_utilization_std'] = 0.0
            metrics['memory_utilization_min'] = 0.0
            metrics['memory_utilization_max'] = 0.0
        
        # Data transmission
        metrics['data_transmitted'] = int(data_transmitted)
        
        # Processing time metrics
        if processing_times:
            metrics['processing_time_mean'] = float(np.mean(processing_times))
            metrics['processing_time_total'] = float(np.sum(processing_times))
        else:
            metrics['processing_time_mean'] = 0.0
            metrics['processing_time_total'] = 0.0
        
        return metrics
    
    def calculate_improvement(self, baseline_metrics: Dict, proposed_metrics: Dict) -> Dict[str, float]:
        """
        Calculate percentage improvement over baseline
        
        Args:
            baseline_metrics: Baseline metrics dictionary
            proposed_metrics: Proposed metrics dictionary
            
        Returns:
            Dictionary of percentage improvements
        """
        improvements = {}
        
        for key in baseline_metrics:
            if key in proposed_metrics:
                baseline_val = baseline_metrics[key]
                proposed_val = proposed_metrics[key]
                
                if baseline_val > 0:
                    # For metrics where lower is better (latency, CPU, memory, etc.)
                    if 'latency' in key or 'cpu' in key or 'memory' in key or 'data' in key or 'time' in key or 'error' in key:
                        improvement = ((baseline_val - proposed_val) / baseline_val) * 100
                    else:
                        # For metrics where higher is better (accuracy, F1, etc.)
                        improvement = ((proposed_val - baseline_val) / baseline_val) * 100
                    
                    improvements[key] = improvement
        
        return improvements
    
    def aggregate_metrics(self, metrics_list: List[Dict]) -> Dict[str, Dict]:
        """
        Aggregate metrics across multiple runs
        
        Args:
            metrics_list: List of metrics dictionaries from multiple runs
            
        Returns:
            Dictionary with mean and std for each metric
        """
        if not metrics_list:
            return {}
        
        aggregated = {}
        
        # Get all metric keys
        all_keys = set()
        for metrics in metrics_list:
            all_keys.update(metrics.keys())
        
        # Calculate mean and std for each metric
        for key in all_keys:
            values = [m.get(key, 0) for m in metrics_list if key in m]
            if values:
                aggregated[key] = {
                    'mean': np.mean(values),
                    'std': np.std(values),
                    'min': np.min(values),
                    'max': np.max(values)
                }
        
        return aggregated
