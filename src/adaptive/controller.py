"""
Adaptive resource/context controller
"""

import numpy as np
from typing import Dict, Tuple, Literal
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AdaptiveController:
    """
    Adaptive controller that makes resource-aware decisions
    """
    
    def __init__(self, config: dict):
        """
        Initialize adaptive controller
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        controller_config = config.get('controller', {})
        
        # Utility weights
        weights = controller_config.get('weights', {})
        self.w_cpu = weights.get('cpu', 0.3)
        self.w_mem = weights.get('memory', 0.2)
        self.w_lat = weights.get('latency', 0.2)
        self.w_conf = weights.get('confidence', 0.2)
        self.w_transmit = weights.get('transmit_cost', 0.05)
        self.w_complexity = weights.get('complexity_cost', 0.05)
        
        # Thresholds (adjusted to enable actual adaptive behavior)
        thresholds = controller_config.get('thresholds', {})
        self.cpu_threshold = thresholds.get('cpu', 90.0)  # Allow more headroom for model switching
        self.mem_threshold = thresholds.get('memory', 90.0)  # Allow more headroom for model switching
        self.latency_max = thresholds.get('latency_max', 200.0)  # Reasonable latency limit
        
        # Decision frequency
        self.decision_frequency = controller_config.get('decision_frequency', 1)
        
        # Processing modes
        self.modes = ['LIGHT', 'STANDARD', 'HEAVY']
        self.transmit_options = ['LOCAL_ONLY', 'TRANSMIT']
        
        # Complexity costs
        self.complexity_costs = {
            'LIGHT': 0.0,
            'STANDARD': 0.5,
            'HEAVY': 1.0
        }
        
        # CPU overhead per mode (reduced to enable actual switching)
        self.complexity_cpu = {
            'LIGHT': 1.0,
            'STANDARD': 3.0,
            'HEAVY': 6.0
        }
        
        # Memory overhead per mode (reduced to enable actual switching)
        self.complexity_mem = {
            'LIGHT': 1.0,
            'STANDARD': 2.0,
            'HEAVY': 4.0
        }
        
        # State
        self.current_state = {
            'cpu_util': 0.0,
            'mem_util': 0.0,
            'net_latency': 0.0,
            'bandwidth': 100.0,
            'data_difficulty': 0.5,
            'anomaly_confidence': 0.0
        }
        
        self.decision_count = 0
        
    def update_state(self, cpu_util: float, mem_util: float, net_latency: float,
                     bandwidth: float, data_difficulty: float = 0.5,
                     anomaly_confidence: float = 0.0) -> None:
        """
        Update controller state
        
        Args:
            cpu_util: CPU utilization percentage
            mem_util: Memory utilization percentage
            net_latency: Network latency in ms
            bandwidth: Available bandwidth in Mbps
            data_difficulty: Estimated data difficulty [0, 1]
            anomaly_confidence: Anomaly confidence from previous detection [0, 1]
        """
        self.current_state = {
            'cpu_util': cpu_util,
            'mem_util': mem_util,
            'net_latency': net_latency,
            'bandwidth': bandwidth,
            'data_difficulty': data_difficulty,
            'anomaly_confidence': anomaly_confidence
        }
    
    def compute_utility(self, mode: str, transmit: str) -> float:
        """
        Compute utility for a given action
        
        Args:
            mode: Processing mode ('LIGHT', 'STANDARD', 'HEAVY')
            transmit: Transmission decision ('LOCAL_ONLY', 'TRANSMIT')
            
        Returns:
            Utility score
        """
        state = self.current_state
        
        # Normalize resource values
        cpu_norm = state['cpu_util'] / 100.0
        mem_norm = state['mem_util'] / 100.0
        lat_norm = min(state['net_latency'], self.latency_max) / self.latency_max
        
        # Compute utility components
        utility_cpu = self.w_cpu * (1 - cpu_norm)
        utility_mem = self.w_mem * (1 - mem_norm)
        utility_lat = self.w_lat * (1 - lat_norm)
        utility_conf = self.w_conf * state['anomaly_confidence']
        
        # Costs
        cost_transmit = self.w_transmit if transmit == 'TRANSMIT' else 0.0
        cost_complexity = self.w_complexity * self.complexity_costs[mode]
        
        # Total utility
        total_utility = utility_cpu + utility_mem + utility_lat + utility_conf - cost_transmit - cost_complexity
        
        return total_utility
    
    def check_feasibility(self, mode: str, transmit: str) -> bool:
        """
        Check if an action is feasible given current state
        
        Args:
            mode: Processing mode
            transmit: Transmission decision
            
        Returns:
            True if feasible, False otherwise
        """
        state = self.current_state
        
        # Check CPU constraint
        if state['cpu_util'] + self.complexity_cpu[mode] > self.cpu_threshold:
            return False
        
        # Check memory constraint
        if state['mem_util'] + self.complexity_mem[mode] > self.mem_threshold:
            return False
        
        # Check latency constraint if transmitting
        if transmit == 'TRANSMIT' and state['net_latency'] > self.latency_max:
            return False
        
        return True
    
    def decide(self) -> Tuple[str, str]:
        """
        Make adaptive decision
        
        Returns:
            Tuple of (mode, transmit)
        """
        self.decision_count += 1
        
        # Evaluate all feasible actions
        best_utility = -float('inf')
        best_mode = 'STANDARD'
        best_transmit = 'LOCAL_ONLY'
        
        for mode in self.modes:
            for transmit in self.transmit_options:
                if self.check_feasibility(mode, transmit):
                    utility = self.compute_utility(mode, transmit)
                    if utility > best_utility:
                        best_utility = utility
                        best_mode = mode
                        best_transmit = transmit
        
        # If no feasible action, use STANDARD as fallback (better detection than LIGHT)
        if best_utility == -float('inf'):
            logger.warning("No feasible action, using fallback: STANDARD mode, LOCAL_ONLY")
            best_mode = 'STANDARD'
            best_transmit = 'LOCAL_ONLY'
        
        if self.decision_count % 100 == 0:
            logger.info(f"Decision #{self.decision_count}: mode={best_mode}, transmit={best_transmit}, utility={best_utility:.3f}")
        
        return best_mode, best_transmit
    
    def decide_static(self, mode: str = 'STANDARD') -> Tuple[str, str]:
        """
        Make static decision (for baseline comparison)
        
        Args:
            mode: Fixed processing mode
            
        Returns:
            Tuple of (mode, transmit)
        """
        return mode, 'LOCAL_ONLY'
    
    def decide_centralized(self) -> Tuple[str, str]:
        """
        Make centralized decision (transmit everything)
        
        Returns:
            Tuple of (mode, transmit)
        """
        return 'LIGHT', 'TRANSMIT'  # Minimal local processing, transmit all
    
    def get_state(self) -> Dict:
        """Get current state"""
        return self.current_state.copy()
    
    def reset(self) -> None:
        """Reset controller state"""
        self.current_state = {
            'cpu_util': 0.0,
            'mem_util': 0.0,
            'net_latency': 0.0,
            'bandwidth': 100.0,
            'data_difficulty': 0.5,
            'anomaly_confidence': 0.0
        }
        self.decision_count = 0
