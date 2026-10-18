"""
Edge processor for local anomaly detection
"""

import numpy as np
import time
from typing import Tuple, Dict, Optional, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EdgeProcessor:
    """
    Processes data at the edge with adaptive model selection
    """
    
    def __init__(self, config: dict, controller, system_monitor):
        """
        Initialize edge processor
        
        Args:
            config: Configuration dictionary
            controller: Adaptive controller instance
            system_monitor: System monitor instance
        """
        self.config = config
        self.controller = controller
        self.system_monitor = system_monitor
        
        # Import models
        from src.models.isolation_forest import IsolationForestModel
        from src.models.autoencoder import AutoencoderModel
        from src.models.lstm_autoencoder import LSTMAutoencoderModel
        
        # Initialize models
        self.models = {
            'LIGHT': IsolationForestModel(config),
            'STANDARD': AutoencoderModel(config),
            'HEAVY': LSTMAutoencoderModel(config)
        }
        
        # Current active model
        self.current_mode = 'STANDARD'
        
        # Processing statistics
        self.stats = {
            'samples_processed': 0,
            'anomalies_detected': 0,
            'data_transmitted': 0,
            'latencies': [],
            'cpu_utils': [],
            'mem_utils': []
        }
        
        # Threshold (will be set by calibration)
        self.threshold = None
        self.calibrated = False
        
    def train_models(self, X_train: np.ndarray) -> None:
        """
        Train all models
        
        Args:
            X_train: Training data
        """
        logger.info("Training LIGHT model (Isolation Forest)...")
        self.models['LIGHT'].fit(X_train)
        
        logger.info("Training STANDARD model (Autoencoder)...")
        self.models['STANDARD'].fit(X_train)
        
        logger.info("Training HEAVY model (LSTM Autoencoder)...")
        self.models['HEAVY'].fit(X_train)
        
        logger.info("All models trained successfully")
    
    def process_sample(self, sample: np.ndarray, mode: str = 'STANDARD') -> Tuple[float, float]:
        """
        Process a single sample (returns score only)
        
        Args:
            sample: Input sample (window_size, n_features)
            mode: Processing mode
            
        Returns:
            Tuple of (anomaly_score, processing_time)
        """
        start_time = time.time()
        
        # Get model
        model = self.models[mode]
        
        # Reshape to 2D (1, flattened_features) for models
        # Autoencoder expects (n_samples, n_features) where n_features = window_size * n_features
        if len(sample.shape) == 2:
            sample = sample.reshape(1, -1)
        elif len(sample.shape) == 1:
            sample = sample.reshape(1, -1)
        
        # Predict scores only
        anomaly_score = model.predict_scores(sample)
        
        processing_time = (time.time() - start_time) * 1000  # Convert to ms
        
        return anomaly_score[0], processing_time
    
    def set_threshold(self, threshold: float):
        """
        Set calibrated threshold
        
        Args:
            threshold: Calibrated threshold value
        """
        self.threshold = threshold
        self.calibrated = True
        logger.info(f"Threshold set to {threshold:.6f}")
    
    def process_stream(self, data_stream, adaptive: bool = True, 
                      simulated_resources: Optional[list] = None) -> Dict:
        """
        Process a data stream
        
        Args:
            data_stream: Data stream iterator
            adaptive: Whether to use adaptive controller
            simulated_resources: Optional list of simulated resource states for testing
            
        Returns:
            Processing results dictionary
        """
        predictions = []
        labels = []
        scores = []
        latencies = []
        cpu_utils = []
        mem_utils = []
        transmissions = []
        
        for idx, (sample, label, timestamp) in enumerate(data_stream):
            # Get system state (use simulated if provided)
            if simulated_resources and idx < len(simulated_resources):
                cpu_util = simulated_resources[idx]['cpu']
                mem_util = simulated_resources[idx]['mem']
            else:
                cpu_util = self.system_monitor.get_cpu_utilization()
                mem_util = self.system_monitor.get_memory_utilization()
            
            net_latency = self.system_monitor.get_network_latency()
            bandwidth = self.system_monitor.get_bandwidth()
            
            # Update controller state
            self.controller.update_state(
                cpu_util=cpu_util,
                mem_util=mem_util,
                net_latency=net_latency,
                bandwidth=bandwidth,
                data_difficulty=0.5,  # Could be estimated from data
                anomaly_confidence=0.0  # Will be updated after prediction
            )
            
            # Make decision
            if adaptive:
                mode, transmit = self.controller.decide()
            else:
                mode, transmit = self.controller.decide_static(mode='STANDARD')
            
            # Process sample
            anomaly_score, processing_time = self.process_sample(sample, mode)
            
            # Apply threshold if calibrated
            if self.calibrated:
                anomaly_label = 1 if anomaly_score >= self.threshold else 0
            else:
                # Fallback: use model's internal threshold
                model = self.models[mode]
                _, anomaly_label = model.predict(sample.reshape(1, -1))
                anomaly_label = anomaly_label[0]
            
            # Update controller with confidence
            self.controller.update_state(
                cpu_util=cpu_util,
                mem_util=mem_util,
                net_latency=net_latency,
                bandwidth=bandwidth,
                data_difficulty=0.5,
                anomaly_confidence=anomaly_score
            )
            
            # Make local decision based on anomaly label
            if anomaly_label == 1:
                local_decision = 'ANOMALY'
                should_transmit = True  # Always transmit anomalies
            else:
                local_decision = 'NORMAL'
                should_transmit = transmit == 'TRANSMIT'  # Transmit based on controller decision
            
            # Record metrics
            predictions.append(anomaly_label)
            labels.append(label)
            scores.append(anomaly_score)
            latencies.append(processing_time)
            cpu_utils.append(cpu_util)
            mem_utils.append(mem_util)
            transmissions.append(1 if should_transmit else 0)
            
            # Update statistics
            self.stats['samples_processed'] += 1
            if anomaly_label == 1:
                self.stats['anomalies_detected'] += 1
            if should_transmit:
                self.stats['data_transmitted'] += sample.nbytes
            
            self.stats['latencies'].append(processing_time)
            self.stats['cpu_utils'].append(cpu_util)
            self.stats['mem_utils'].append(mem_util)
        
        return {
            'predictions': np.array(predictions),
            'labels': np.array(labels),
            'scores': np.array(scores),
            'latencies': latencies,
            'cpu_utils': cpu_utils,
            'mem_utils': mem_utils,
            'transmissions': transmissions
        }
    
    def get_statistics(self) -> Dict:
        """Get processing statistics"""
        return self.stats.copy()
    
    def reset_statistics(self):
        """Reset processing statistics"""
        self.stats = {
            'samples_processed': 0,
            'anomalies_detected': 0,
            'data_transmitted': 0,
            'latencies': [],
            'cpu_utils': [],
            'mem_utils': []
        }
