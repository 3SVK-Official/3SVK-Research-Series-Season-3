"""
Feature engineering for time-series data
"""

import numpy as np
import pandas as pd
from typing import List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FeatureEngineer:
    """
    Engineers features from time-series data
    """
    
    def __init__(self, config: dict):
        """
        Initialize feature engineer
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.enabled = config.get('preprocessing', {}).get('feature_engineering', True)
        self.features = config.get('preprocessing', {}).get('rolling_features', 
                                                             ['mean', 'std', 'min', 'max'])
        self.window_size = config.get('data', {}).get('window_size', 60)
        
    def add_rolling_features(self, data: np.ndarray, window: int = 10) -> np.ndarray:
        """
        Add rolling statistical features
        
        Args:
            data: Input data (n_samples, n_features)
            window: Rolling window size
            
        Returns:
            Data with additional features (n_samples, n_features * (1 + len(features)))
        """
        if not self.enabled:
            return data
        
        n_samples, n_features = data.shape
        df = pd.DataFrame(data)
        
        engineered_features = []
        
        for feat in self.features:
            if feat == 'mean':
                engineered_features.append(df.rolling(window=window, min_periods=1).mean().values)
            elif feat == 'std':
                engineered_features.append(df.rolling(window=window, min_periods=1).std().fillna(0).values)
            elif feat == 'min':
                engineered_features.append(df.rolling(window=window, min_periods=1).min().values)
            elif feat == 'max':
                engineered_features.append(df.rolling(window=window, min_periods=1).max().values)
            elif feat == 'median':
                engineered_features.append(df.rolling(window=window, min_periods=1).median().values)
            elif feat == 'skew':
                engineered_features.append(df.rolling(window=window, min_periods=1).skew().fillna(0).values)
            elif feat == 'kurt':
                engineered_features.append(df.rolling(window=window, min_periods=1).kurt().fillna(0).values)
        
        # Combine original and engineered features
        all_features = [data] + engineered_features
        combined = np.concatenate(all_features, axis=1)
        
        logger.info(f"Feature engineering: {data.shape} -> {combined.shape}")
        return combined
    
    def add_diff_features(self, data: np.ndarray) -> np.ndarray:
        """
        Add difference features (first and second order)
        
        Args:
            data: Input data
            
        Returns:
            Data with difference features
        """
        if not self.enabled:
            return data
        
        # First order difference
        diff1 = np.diff(data, axis=0)
        diff1 = np.vstack([np.zeros((1, data.shape[1])), diff1])
        
        # Second order difference
        diff2 = np.diff(diff1, axis=0)
        diff2 = np.vstack([np.zeros((1, data.shape[1])), diff2])
        
        combined = np.concatenate([data, diff1, diff2], axis=1)
        
        return combined
    
    def fit_transform(self, data: np.ndarray) -> np.ndarray:
        """
        Engineer features from data
        
        Args:
            data: Input data
            
        Returns:
            Data with engineered features
        """
        if not self.enabled:
            return data
        
        # Add rolling features
        engineered = self.add_rolling_features(data)
        
        # Add difference features
        engineered = self.add_diff_features(engineered)
        
        return engineered
    
    def transform(self, data: np.ndarray) -> np.ndarray:
        """
        Transform data (same as fit_transform for this implementation)
        
        Args:
            data: Input data
            
        Returns:
            Data with engineered features
        """
        return self.fit_transform(data)
