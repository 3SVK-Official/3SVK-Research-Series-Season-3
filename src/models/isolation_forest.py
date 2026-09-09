"""
Statistical Anomaly Detector (Z-score based) for lightweight anomaly detection
Replaces Isolation Forest to avoid sklearn dependency
"""

import numpy as np
from typing import Tuple, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IsolationForestModel:
    """
    Statistical anomaly detector using Z-score method
    Lightweight alternative to Isolation Forest
    """
    
    def __init__(self, config: dict):
        """
        Initialize statistical anomaly detector
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        model_config = config.get('models', {}).get('light', {})
        
        self.contamination = model_config.get('contamination', 0.1)
        self.random_state = model_config.get('random_state', 42)
        
        self.mean = None
        self.std = None
        self.threshold = None
        self.is_fitted = False
        
    def fit(self, X_train: np.ndarray) -> None:
        """
        Fit the statistical anomaly detector
        
        Args:
            X_train: Training data (n_samples, n_features)
        """
        # Flatten if 3D (windows)
        if len(X_train.shape) == 3:
            X_train = X_train.reshape(X_train.shape[0], -1)
        
        # Calculate mean and std
        self.mean = np.mean(X_train, axis=0)
        self.std = np.std(X_train, axis=0)
        
        # Avoid division by zero
        self.std[self.std == 0] = 1
        
        # Calculate z-scores for training data
        z_scores = np.abs((X_train - self.mean) / self.std)
        max_z_scores = np.max(z_scores, axis=1)
        
        # Set threshold based on contamination
        # Store raw threshold for reference, but will use external calibration
        self.raw_threshold = np.percentile(max_z_scores, (1 - self.contamination) * 100)
        self.threshold = self.raw_threshold  # Default for backward compatibility
        
        self.is_fitted = True
        
        logger.info(f"Statistical anomaly detector fitted on {X_train.shape}, threshold={self.threshold:.3f}")
    
    def predict_scores(self, X: np.ndarray) -> np.ndarray:
        """
        Predict anomaly scores only (no thresholding)
        
        Args:
            X: Input data (n_samples, n_features)
            
        Returns:
            Anomaly scores (higher = more anomalous)
        """
        if not self.is_fitted:
            raise ValueError("Model not fitted")
        
        # Flatten if 3D (windows)
        if len(X.shape) == 3:
            X = X.reshape(X.shape[0], -1)
        
        # Calculate z-scores
        z_scores = np.abs((X - self.mean) / self.std)
        max_z_scores = np.max(z_scores, axis=1)
        
        # Normalize scores to [0, 1]
        min_score = np.min(max_z_scores)
        max_score = np.max(max_z_scores)
        if max_score - min_score > 0:
            anomaly_scores = (max_z_scores - min_score) / (max_score - min_score)
        else:
            anomaly_scores = np.zeros_like(max_z_scores)
        
        logger.info(f"Predicted {len(anomaly_scores)} samples")
        return anomaly_scores
    
    def predict(self, X: np.ndarray, threshold: Optional[float] = None) -> Tuple[np.ndarray, np.ndarray]:
        """
        Predict anomalies with threshold (for backward compatibility)
        
        Args:
            X: Input data (n_samples, n_features)
            threshold: Threshold for binary classification (uses fitted threshold if None)
            
        Returns:
            Tuple of (anomaly_scores, anomaly_labels)
        """
        anomaly_scores = self.predict_scores(X)
        
        if threshold is None:
            threshold = self.threshold
        
        anomaly_labels = (anomaly_scores >= threshold).astype(int)
        return anomaly_scores, anomaly_labels
    
    def get_params(self) -> dict:
        """Get model parameters"""
        return {
            'contamination': self.contamination,
            'random_state': self.random_state,
            'threshold': self.threshold
        }
