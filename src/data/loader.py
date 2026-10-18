"""
Data loader for anomaly detection datasets
"""

import numpy as np
import pandas as pd
from typing import Tuple, Optional
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataLoader:
    """
    Loads and prepares anomaly detection datasets
    """
    
    def __init__(self, config: dict):
        """
        Initialize data loader
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.data_path = Path(config.get('data', {}).get('data_path', 'data/'))
        self.dataset_name = config.get('data', {}).get('dataset', 'nab')
        
    def load_nab_dataset(self, file_path: str) -> Tuple[np.ndarray, np.ndarray]:
        """
        Load Numenta Anomaly Benchmark dataset
        
        Args:
            file_path: Path to the CSV file
            
        Returns:
            Tuple of (features, labels)
        """
        try:
            df = pd.read_csv(file_path)
            
            # NAB format: timestamp, value
            if 'timestamp' in df.columns:
                df = df.set_index('timestamp')
            
            # Extract values
            values = df['value'].values if 'value' in df.columns else df.iloc[:, 0].values
            
            # For NAB, anomalies are typically labeled separately
            # For now, we'll assume no labels and use unsupervised detection
            # Labels will be generated during evaluation if ground truth exists
            labels = np.zeros(len(values), dtype=np.int32)
            
            logger.info(f"Loaded {len(values)} samples from {file_path}")
            return values.reshape(-1, 1), labels
            
        except Exception as e:
            logger.error(f"Error loading NAB dataset: {e}")
            raise
    
    def load_synthetic_dataset(self, n_samples: int = 10000, 
                               anomaly_ratio: float = 0.05) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate synthetic time-series data with anomalies
        Improved to have more detectable anomaly patterns
        
        Args:
            n_samples: Number of samples to generate
            anomaly_ratio: Ratio of anomalies in the data
            
        Returns:
            Tuple of (features, labels)
        """
        np.random.seed(self.config.get('experiments', {}).get('random_seed', 42))
        
        # Generate normal data (sinusoidal with noise)
        t = np.linspace(0, 100, n_samples)
        normal_data = np.sin(t) + 0.1 * np.random.randn(n_samples)
        
        # Add anomalies with stronger signals
        n_anomalies = int(n_samples * anomaly_ratio)
        anomaly_indices = np.random.choice(n_samples, n_anomalies, replace=False)
        
        data = normal_data.copy()
        labels = np.zeros(n_samples, dtype=np.int32)
        
        for idx in anomaly_indices:
            # Stronger anomaly patterns
            anomaly_type = np.random.rand()
            
            if anomaly_type < 0.4:
                # Large spike (more detectable)
                data[idx] += np.random.uniform(5, 10)
            elif anomaly_type < 0.7:
                # Large dip (more detectable)
                data[idx] += np.random.uniform(-10, -5)
            elif anomaly_type < 0.85:
                # Sustained shift (affects multiple consecutive points)
                duration = np.random.randint(3, 8)
                shift = np.random.uniform(3, 6) * (1 if np.random.rand() > 0.5 else -1)
                end_idx = min(idx + duration, n_samples)
                data[idx:end_idx] += shift
                labels[idx:end_idx] = 1
            else:
                # Amplitude spike (multiply by factor)
                data[idx] *= np.random.uniform(3, 5)
            
            labels[idx] = 1
        
        logger.info(f"Generated synthetic dataset: {n_samples} samples, {n_anomalies} anomalies")
        logger.info(f"Anomaly patterns: spikes, dips, sustained shifts, amplitude changes")
        return data.reshape(-1, 1), labels
    
    def load_dataset(self, dataset_type: str = 'synthetic', **kwargs) -> Tuple[np.ndarray, np.ndarray]:
        """
        Load dataset based on type
        
        Args:
            dataset_type: Type of dataset ('synthetic', 'nab', 'custom')
            **kwargs: Additional arguments for specific loaders
            
        Returns:
            Tuple of (features, labels)
        """
        if dataset_type == 'synthetic':
            return self.load_synthetic_dataset(**kwargs)
        elif dataset_type == 'nab':
            file_path = kwargs.get('file_path')
            if not file_path:
                raise ValueError("file_path required for NAB dataset")
            return self.load_nab_dataset(file_path)
        else:
            raise ValueError(f"Unknown dataset type: {dataset_type}")
    
    def train_test_split(self, data: np.ndarray, labels: np.ndarray, 
                        test_ratio: float = 0.2) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Split data into train and test sets
        
        Args:
            data: Feature data
            labels: Label data
            test_ratio: Ratio of test data
            
        Returns:
            Tuple of (train_data, test_data, train_labels, test_labels)
        """
        split_idx = int(len(data) * (1 - test_ratio))
        
        train_data = data[:split_idx]
        test_data = data[split_idx:]
        train_labels = labels[:split_idx]
        test_labels = labels[split_idx:]
        
        logger.info(f"Train size: {len(train_data)}, Test size: {len(test_data)}")
        return train_data, test_data, train_labels, test_labels
    
    def train_val_test_split(self, data: np.ndarray, labels: np.ndarray,
                            train_ratio: float = 0.7, val_ratio: float = 0.15) -> Tuple[
                                np.ndarray, np.ndarray, np.ndarray, 
                                np.ndarray, np.ndarray, np.ndarray]:
        """
        Split data into train, validation, and test sets
        
        Args:
            data: Feature data
            labels: Label data
            train_ratio: Ratio of training data
            val_ratio: Ratio of validation data (test ratio = 1 - train_ratio - val_ratio)
            
        Returns:
            Tuple of (train_data, val_data, test_data, train_labels, val_labels, test_labels)
        """
        n = len(data)
        train_end = int(n * train_ratio)
        val_end = int(n * (train_ratio + val_ratio))
        
        train_data = data[:train_end]
        val_data = data[train_end:val_end]
        test_data = data[val_end:]
        
        train_labels = labels[:train_end]
        val_labels = labels[train_end:val_end]
        test_labels = labels[val_end:]
        
        logger.info(f"Train size: {len(train_data)}, Val size: {len(val_data)}, Test size: {len(test_data)}")
        logger.info(f"Train anomalies: {np.sum(train_labels)}, Val anomalies: {np.sum(val_labels)}, Test anomalies: {np.sum(test_labels)}")
        
        return train_data, val_data, test_data, train_labels, val_labels, test_labels
