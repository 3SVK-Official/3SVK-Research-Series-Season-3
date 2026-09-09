"""
Cloud coordinator for centralized processing
"""

import numpy as np
import time
from typing import Tuple, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CloudCoordinator:
    """
    Simulates cloud-based centralized anomaly detection
    """
    
    def __init__(self, config: dict, system_monitor):
        """
        Initialize cloud coordinator
        
        Args:
            config: Configuration dictionary
            system_monitor: System monitor instance
        """
        self.config = config
        self.system_monitor = system_monitor
        
        # Import heavy model for cloud processing
        from src.models.lstm_autoencoder import LSTMAutoencoderModel
        
        # Initialize cloud model (heavy model)
        self.model = LSTMAutoencoderModel(config)
        self.is_fitted = False
        
        # Threshold (will be set by calibration)
        self.threshold = None
        self.calibrated = False
        
        # Network simulation
        self.network_latency = 50.0  # ms
        self.bandwidth = 100.0  # Mbps
        
        # Processing statistics
        self.stats = {
            'samples_processed': 0,
            'anomalies_detected': 0,
            'total_data_transmitted': 0,
            'latencies': [],
            'network_latencies': []
        }
        
    def train_model(self, X_train: np.ndarray) -> None:
        """
        Train cloud model
        
        Args:
            X_train: Training data
        """
        logger.info("Training cloud model (LSTM Autoencoder)...")
        self.model.fit(X_train)
        self.is_fitted = True
        logger.info("Cloud model trained successfully")
    
    def set_threshold(self, threshold: float):
        """
        Set calibrated threshold
        
        Args:
            threshold: Calibrated threshold value
        """
        self.threshold = threshold
        self.calibrated = True
        logger.info(f"Cloud threshold set to {threshold:.6f}")
    
    def set_network_conditions(self, latency: float, bandwidth: float):
        """
        Set network conditions
        
        Args:
            latency: Network latency in ms
            bandwidth: Bandwidth in Mbps
        """
        self.network_latency = latency
        self.bandwidth = bandwidth
        self.system_monitor.set_simulated_network_conditions(latency, bandwidth)
    
    def process_sample(self, sample: np.ndarray) -> Tuple[float, int, float]:
        """
        Process a sample in the cloud
        
        Args:
            sample: Input sample
            
        Returns:
            Tuple of (anomaly_score, anomaly_label, total_latency)
        """
        if not self.is_fitted:
            raise ValueError("Cloud model not trained")
        
        # Simulate network transmission latency
        transmission_latency = self.network_latency
        
        # Simulate cloud processing (faster than edge due to more resources)
        start_time = time.time()
        
        # Reshape if needed
        if len(sample.shape) == 1:
            sample = sample.reshape(1, -1)
        
        # Get score only
        anomaly_score = self.model.predict_scores(sample)
        anomaly_score = anomaly_score[0]
        
        # Apply threshold if calibrated
        if self.calibrated:
            anomaly_label = 1 if anomaly_score >= self.threshold else 0
        else:
            # Fallback to model's internal threshold
            _, anomaly_label = self.model.predict(sample)
            anomaly_label = anomaly_label[0]
        
        processing_latency = (time.time() - start_time) * 1000  # Convert to ms
        
        # Total latency (transmit + process + return)
        total_latency = transmission_latency * 2 + processing_latency
        
        return anomaly_score, anomaly_label, total_latency
    
    def process_stream(self, data_stream) -> Dict:
        """
        Process a data stream in the cloud
        
        Args:
            data_stream: Data stream iterator
            
        Returns:
            Processing results dictionary
        """
        predictions = []
        labels = []
        scores = []
        latencies = []
        
        for sample, label, timestamp in data_stream:
            # Process in cloud
            anomaly_score, anomaly_label, total_latency = self.process_sample(sample)
            
            # Record metrics
            predictions.append(anomaly_label)
            labels.append(label)
            scores.append(anomaly_score)
            latencies.append(total_latency)
            
            # Update statistics
            self.stats['samples_processed'] += 1
            if anomaly_label == 1:
                self.stats['anomalies_detected'] += 1
            self.stats['total_data_transmitted'] += sample.nbytes
            self.stats['latencies'].append(total_latency)
            self.stats['network_latencies'].append(self.network_latency * 2)
        
        return {
            'predictions': np.array(predictions),
            'labels': np.array(labels),
            'scores': np.array(scores),
            'latencies': latencies
        }
    
    def get_statistics(self) -> Dict:
        """Get processing statistics"""
        return self.stats.copy()
    
    def reset_statistics(self):
        """Reset processing statistics"""
        self.stats = {
            'samples_processed': 0,
            'anomalies_detected': 0,
            'total_data_transmitted': 0,
            'latencies': [],
            'network_latencies': []
        }
