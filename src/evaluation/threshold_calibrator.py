"""
Threshold calibration module for anomaly detection
Calibrates thresholds on validation data to prevent test-set leakage
"""

import numpy as np
from typing import Tuple, Optional, Literal
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ThresholdCalibrator:
    """
    Calibrates anomaly detection thresholds on validation data
    """
    
    def __init__(self, method: Literal['percentile', 'f1_optimize', 'precision_constrained', 'recall_constrained'] = 'f1_optimize'):
        """
        Initialize threshold calibrator
        
        Args:
            method: Calibration method
                - 'percentile': Use fixed percentile (e.g., 95th)
                - 'f1_optimize': Maximize F1 on validation data
                - 'precision_constrained': Maximize recall subject to precision constraint
                - 'recall_constrained': Maximize precision subject to recall constraint
        """
        self.method = method
        self.calibrated_threshold = None
        self.validation_f1 = None
        
    def calibrate(self, y_true: np.ndarray, y_scores: np.ndarray, 
                 constraint: Optional[float] = None) -> float:
        """
        Calibrate threshold on validation data
        
        Args:
            y_true: True labels (0=normal, 1=anomaly)
            y_scores: Anomaly scores (higher = more anomalous)
            constraint: Constraint value for precision/recall methods
            
        Returns:
            Calibrated threshold
        """
        if len(y_true) != len(y_scores):
            raise ValueError("y_true and y_scores must have same length")
        
        if np.sum(y_true) == 0:
            logger.warning("No anomalies in validation data, using median threshold")
            self.calibrated_threshold = np.median(y_scores)
            return self.calibrated_threshold
        
        if self.method == 'percentile':
            self.calibrated_threshold = self._calibrate_percentile(y_scores, constraint)
        elif self.method == 'f1_optimize':
            self.calibrated_threshold = self._calibrate_f1_optimize(y_true, y_scores)
        elif self.method == 'precision_constrained':
            self.calibrated_threshold = self._calibrate_precision_constrained(y_true, y_scores, constraint)
        elif self.method == 'recall_constrained':
            self.calibrated_threshold = self._calibrate_recall_constrained(y_true, y_scores, constraint)
        else:
            raise ValueError(f"Unknown calibration method: {self.method}")
        
        # Calculate validation F1 for reporting
        y_pred = (y_scores >= self.calibrated_threshold).astype(int)
        tp = np.sum((y_true == 1) & (y_pred == 1))
        fp = np.sum((y_true == 0) & (y_pred == 1))
        fn = np.sum((y_true == 1) & (y_pred == 0))
        
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        self.validation_f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
        
        logger.info(f"Calibrated threshold: {self.calibrated_threshold:.6f} (method={self.method}, val_f1={self.validation_f1:.4f})")
        return self.calibrated_threshold
    
    def _calibrate_percentile(self, y_scores: np.ndarray, percentile: Optional[float] = None) -> float:
        """Calibrate using percentile (default 95th)"""
        if percentile is None:
            percentile = 95.0
        threshold = np.percentile(y_scores, percentile)
        logger.info(f"Percentile calibration: {percentile}th percentile = {threshold:.6f}")
        return threshold
    
    def _calibrate_f1_optimize(self, y_true: np.ndarray, y_scores: np.ndarray) -> float:
        """Calibrate by maximizing F1 on validation data"""
        # Sort unique scores
        unique_scores = np.unique(y_scores)
        
        best_threshold = 0.5
        best_f1 = 0.0
        
        for threshold in unique_scores:
            y_pred = (y_scores >= threshold).astype(int)
            
            tp = np.sum((y_true == 1) & (y_pred == 1))
            fp = np.sum((y_true == 0) & (y_pred == 1))
            fn = np.sum((y_true == 1) & (y_pred == 0))
            
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
            f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
            
            if f1 > best_f1:
                best_f1 = f1
                best_threshold = threshold
        
        logger.info(f"F1 optimization: best threshold = {best_threshold:.6f}, best F1 = {best_f1:.4f}")
        return best_threshold
    
    def _calibrate_precision_constrained(self, y_true: np.ndarray, y_scores: np.ndarray, 
                                         min_precision: Optional[float] = None) -> float:
        """Calibrate by maximizing recall subject to minimum precision constraint"""
        if min_precision is None:
            min_precision = 0.5
        
        # Sort unique scores in descending order (higher threshold = higher precision)
        unique_scores = np.unique(y_scores)[::-1]
        
        best_threshold = 0.5
        best_recall = 0.0
        
        for threshold in unique_scores:
            y_pred = (y_scores >= threshold).astype(int)
            
            tp = np.sum((y_true == 1) & (y_pred == 1))
            fp = np.sum((y_true == 0) & (y_pred == 1))
            fn = np.sum((y_true == 1) & (y_pred == 0))
            
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
            
            if precision >= min_precision and recall > best_recall:
                best_recall = recall
                best_threshold = threshold
        
        logger.info(f"Precision-constrained: threshold = {best_threshold:.6f}, recall = {best_recall:.4f} (min_precision={min_precision})")
        return best_threshold
    
    def _calibrate_recall_constrained(self, y_true: np.ndarray, y_scores: np.ndarray, 
                                     min_recall: Optional[float] = None) -> float:
        """Calibrate by maximizing precision subject to minimum recall constraint"""
        if min_recall is None:
            min_recall = 0.5
        
        # Sort unique scores in ascending order (lower threshold = higher recall)
        unique_scores = np.unique(y_scores)
        
        best_threshold = 0.5
        best_precision = 0.0
        
        for threshold in unique_scores:
            y_pred = (y_scores >= threshold).astype(int)
            
            tp = np.sum((y_true == 1) & (y_pred == 1))
            fp = np.sum((y_true == 0) & (y_pred == 1))
            fn = np.sum((y_true == 1) & (y_pred == 0))
            
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
            
            if recall >= min_recall and precision > best_precision:
                best_precision = precision
                best_threshold = threshold
        
        logger.info(f"Recall-constrained: threshold = {best_threshold:.6f}, precision = {best_precision:.4f} (min_recall={min_recall})")
        return best_threshold
    
    def get_threshold(self) -> float:
        """Get calibrated threshold"""
        if self.calibrated_threshold is None:
            raise ValueError("Threshold not calibrated. Call calibrate() first.")
        return self.calibrated_threshold
    
    def get_validation_f1(self) -> float:
        """Get validation F1 score"""
        if self.validation_f1 is None:
            raise ValueError("Threshold not calibrated. Call calibrate() first.")
        return self.validation_f1
    
    def apply(self, y_scores: np.ndarray) -> np.ndarray:
        """
        Apply calibrated threshold to scores
        
        Args:
            y_scores: Anomaly scores
            
        Returns:
            Binary predictions (0=normal, 1=anomaly)
        """
        if self.calibrated_threshold is None:
            raise ValueError("Threshold not calibrated. Call calibrate() first.")
        return (y_scores >= self.calibrated_threshold).astype(int)
    
    def reset(self):
        """Reset calibrator state"""
        self.calibrated_threshold = None
        self.validation_f1 = None
