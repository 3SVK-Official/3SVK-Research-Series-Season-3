"""
System resource monitor
"""

import time
import psutil
import threading
from typing import Dict, Optional
from collections import deque
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SystemMonitor:
    """
    Monitors system resources (CPU, memory, network)
    """
    
    def __init__(self, window_size: int = 100):
        """
        Initialize system monitor
        
        Args:
            window_size: Size of the rolling window for metrics
        """
        self.window_size = window_size
        
        # Rolling windows for metrics
        self.cpu_history = deque(maxlen=window_size)
        self.memory_history = deque(maxlen=window_size)
        self.latency_history = deque(maxlen=window_size)
        
        # Network simulation
        self.simulated_latency = 0.0
        self.simulated_bandwidth = 100.0  # Mbps
        
        # Monitoring thread
        self.monitoring = False
        self.monitor_thread = None
        
    def start_monitoring(self, interval: float = 0.1):
        """
        Start monitoring in background thread
        
        Args:
            interval: Monitoring interval in seconds
        """
        if self.monitoring:
            logger.warning("Monitoring already started")
            return
        
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, args=(interval,))
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        logger.info("System monitoring started")
    
    def stop_monitoring(self):
        """Stop monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1.0)
        logger.info("System monitoring stopped")
    
    def _monitor_loop(self, interval: float):
        """Monitoring loop"""
        while self.monitoring:
            cpu = psutil.cpu_percent(interval=None)
            memory = psutil.virtual_memory().percent
            
            self.cpu_history.append(cpu)
            self.memory_history.append(memory)
            
            time.sleep(interval)
    
    def get_cpu_utilization(self) -> float:
        """
        Get current CPU utilization
        
        Returns:
            CPU utilization percentage
        """
        if self.cpu_history:
            return self.cpu_history[-1]
        return psutil.cpu_percent(interval=None)
    
    def get_memory_utilization(self) -> float:
        """
        Get current memory utilization
        
        Returns:
            Memory utilization percentage
        """
        if self.memory_history:
            return self.memory_history[-1]
        return psutil.virtual_memory().percent
    
    def get_average_cpu(self, n_samples: int = 10) -> float:
        """
        Get average CPU over last n samples
        
        Args:
            n_samples: Number of samples to average
            
        Returns:
            Average CPU utilization
        """
        if len(self.cpu_history) >= n_samples:
            return sum(list(self.cpu_history)[-n_samples:]) / n_samples
        elif self.cpu_history:
            return sum(self.cpu_history) / len(self.cpu_history)
        return 0.0
    
    def get_average_memory(self, n_samples: int = 10) -> float:
        """
        Get average memory over last n samples
        
        Args:
            n_samples: Number of samples to average
            
        Returns:
            Average memory utilization
        """
        if len(self.memory_history) >= n_samples:
            return sum(list(self.memory_history)[-n_samples:]) / n_samples
        elif self.memory_history:
            return sum(self.memory_history) / len(self.memory_history)
        return 0.0
    
    def set_simulated_network_conditions(self, latency: float, bandwidth: float):
        """
        Set simulated network conditions (for testing)
        
        Args:
            latency: Simulated latency in ms
            bandwidth: Simulated bandwidth in Mbps
        """
        self.simulated_latency = latency
        self.simulated_bandwidth = bandwidth
    
    def get_network_latency(self) -> float:
        """
        Get network latency (simulated or measured)
        
        Returns:
            Latency in ms
        """
        return self.simulated_latency
    
    def get_bandwidth(self) -> float:
        """
        Get available bandwidth (simulated)
        
        Returns:
            Bandwidth in Mbps
        """
        return self.simulated_bandwidth
    
    def record_latency(self, latency: float):
        """
        Record a latency measurement
        
        Args:
            latency: Latency in ms
        """
        self.latency_history.append(latency)
    
    def get_current_state(self) -> Dict[str, float]:
        """
        Get current system state
        
        Returns:
            Dictionary of current metrics
        """
        return {
            'cpu_util': self.get_cpu_utilization(),
            'mem_util': self.get_memory_utilization(),
            'net_latency': self.get_network_latency(),
            'bandwidth': self.get_bandwidth()
        }
    
    def reset(self):
        """Reset all histories"""
        self.cpu_history.clear()
        self.memory_history.clear()
        self.latency_history.clear()
