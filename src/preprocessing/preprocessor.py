"""
Data preprocessor for anomaly detection
"""

import numpy as np
from typing import Tuple, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Preprocessor:
    """
    Preprocesses time-series data for anomaly detection
    """
    
    def __init__(self, config: dict):
        """
        Initialize preprocessor
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.normalize = config.get('preprocessing', {}).get('normalize', True)
        self.method = config.get('preprocessing', {}).get('normalization_method', 'minmax')
        self.window_size = config.get('data', {}).get('window_size', 60)
        
        # Normalization parameters (fit during training)
        self.min_val = None
        self.max_val = None
        self.mean_val = None
        self.std_val = None
        
    def normalize_data(self, data: np.ndarray, fit: bool = True) -> np.ndarray:
        """
        Normalize data
        
        Args:
            data: Input data
            fit: Whether to fit normalization parameters
            
        Returns:
            Normalized data
        """
        if not self.normalize:
            return data
        
        if self.method == 'minmax':
            if fit:
                self.min_val = np.min(data, axis=0)
                self.max_val = np.max(data, axis=0)
            
            # Avoid division by zero
            range_val = self.max_val - self.min_val
            range_val[range_val == 0] = 1
            
            normalized = (data - self.min_val) / range_val
            return normalized
            
        elif self.method == 'zscore':
            if fit:
                self.mean_val = np.mean(data, axis=0)
                self.std_val = np.std(data, axis=0)
            
            # Avoid division by zero
            self.std_val[self.std_val == 0] = 1
            
            normalized = (data - self.mean_val) / self.std_val
            return normalized
        
        else:
            logger.warning(f"Unknown normalization method: {self.method}")
            return data
    
    def create_windows(self, data: np.ndarray) -> np.ndarray:
        """
        Create sliding windows from time-series data
        
        Args:
            data: Input time-series data (n_samples, n_features)
            
        Returns:
            Windowed data (n_windows, window_size, n_features)
        """
        n_samples, n_features = data.shape
        n_windows = n_samples - self.window_size + 1
        
        if n_windows <= 0:
            logger.warning(f"Data length ({n_samples}) < window size ({self.window_size})")
            return data.reshape(1, -1, n_features)
        
        windows = np.zeros((n_windows, self.window_size, n_features))
        
        for i in range(n_windows):
            windows[i] = data[i:i + self.window_size]
        
        return windows
    
    def fit_transform(self, data: np.ndarray) -> np.ndarray:
        """
        Fit preprocessor and transform data
        
        Args:
            data: Input data
            
        Returns:
            Preprocessed data
        """
        # Normalize
        normalized = self.normalize_data(data, fit=True)
        
        # Create windows
        windowed = self.create_windows(normalized)
        
        logger.info(f"Preprocessed data: {data.shape} -> {windowed.shape}")
        return windowed
    
    def transform(self, data: np.ndarray) -> np.ndarray:
        """
        Transform data using fitted parameters
        
        Args:
            data: Input data
            
        Returns:
            Preprocessed data
        """
        # Normalize using fitted parameters
        normalized = self.normalize_data(data, fit=False)
        
        # Create windows
        windowed = self.create_windows(normalized)
        
        return windowed
    
    def inverse_normalize(self, data: np.ndarray) -> np.ndarray:
        """
        Inverse normalization
        
        Args:
            data: Normalized data
            
        Returns:
            Denormalized data
        """
        if not self.normalize:
            return data
        
        if self.method == 'minmax':
            if self.min_val is None or self.max_val is None:
                raise ValueError("Preprocessor not fitted")
            
            range_val = self.max_val - self.min_val
            range_val[range_val == 0] = 1
            
            denormalized = data * range_val + self.min_val
            return denormalized
            
        elif self.method == 'zscore':
            if self.mean_val is None or self.std_val is None:
                raise ValueError("Preprocessor not fitted")
            
            denormalized = data * self.std_val + self.mean_val
            return denormalized
        
        return data
