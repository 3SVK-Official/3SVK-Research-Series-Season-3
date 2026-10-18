"""
Unit tests for adaptive controller
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

import numpy as np
import pytest
from src.adaptive.controller import AdaptiveController


def test_controller_initialization():
    """Test controller initialization"""
    config = {
        'controller': {
            'weights': {
                'cpu': 0.3,
                'memory': 0.2,
                'latency': 0.2,
                'confidence': 0.2,
                'transmit_cost': 0.05,
                'complexity_cost': 0.05
            },
            'thresholds': {
                'cpu': 80.0,
                'memory': 80.0,
                'latency_max': 100.0
            }
        }
    }
    
    controller = AdaptiveController(config)
    
    assert controller.w_cpu == 0.3
    assert controller.cpu_threshold == 80.0
    assert controller.latency_max == 100.0


def test_controller_state_update():
    """Test state update"""
    config = {
        'controller': {
            'weights': {},
            'thresholds': {}
        }
    }
    
    controller = AdaptiveController(config)
    
    controller.update_state(
        cpu_util=50.0,
        mem_util=60.0,
        net_latency=30.0,
        bandwidth=100.0,
        data_difficulty=0.7,
        anomaly_confidence=0.8
    )
    
    state = controller.get_state()
    assert state['cpu_util'] == 50.0
    assert state['mem_util'] == 60.0
    assert state['net_latency'] == 30.0
    assert state['data_difficulty'] == 0.7
    assert state['anomaly_confidence'] == 0.8


def test_controller_utility_computation():
    """Test utility computation"""
    config = {
        'controller': {
            'weights': {
                'cpu': 0.25,
                'memory': 0.25,
                'latency': 0.25,
                'confidence': 0.25,
                'transmit_cost': 0.0,
                'complexity_cost': 0.0
            },
            'thresholds': {
                'cpu': 80.0,
                'memory': 80.0,
                'latency_max': 100.0
            }
        }
    }
    
    controller = AdaptiveController(config)
    controller.update_state(
        cpu_util=50.0,
        mem_util=50.0,
        net_latency=50.0,
        bandwidth=100.0,
        data_difficulty=0.5,
        anomaly_confidence=0.5
    )
    
    utility = controller.compute_utility('STANDARD', 'LOCAL_ONLY')
    
    # Utility should be between 0 and 1
    assert 0 <= utility <= 1


def test_controller_feasibility():
    """Test feasibility checking"""
    config = {
        'controller': {
            'weights': {},
            'thresholds': {
                'cpu': 90.0,
                'memory': 90.0,
                'latency_max': 100.0
            }
        }
    }
    
    controller = AdaptiveController(config)
    
    # Low resources - should be feasible for all modes
    controller.update_state(cpu_util=10.0, mem_util=10.0, net_latency=10.0, bandwidth=100.0)
    assert controller.check_feasibility('LIGHT', 'LOCAL_ONLY')
    assert controller.check_feasibility('STANDARD', 'LOCAL_ONLY')
    assert controller.check_feasibility('HEAVY', 'LOCAL_ONLY')
    
    # High CPU - HEAVY adds 6% overhead
    # complexity_cpu: LIGHT=1.0, STANDARD=3.0, HEAVY=6.0
    controller.update_state(cpu_util=85.0, mem_util=10.0, net_latency=10.0, bandwidth=100.0)
    assert controller.check_feasibility('LIGHT', 'LOCAL_ONLY')  # 85% + 1% = 86% < 90%
    assert not controller.check_feasibility('HEAVY', 'LOCAL_ONLY')  # 85% + 6% = 91% > 90%
    
    # Very high CPU - even LIGHT should not be feasible
    controller.update_state(cpu_util=89.5, mem_util=10.0, net_latency=10.0, bandwidth=100.0)
    assert not controller.check_feasibility('LIGHT', 'LOCAL_ONLY')  # 89.5% + 1% = 90.5% > 90%
    
    # High latency - TRANSMIT should not be feasible
    controller.update_state(cpu_util=10.0, mem_util=10.0, net_latency=150.0, bandwidth=100.0)
    assert controller.check_feasibility('LIGHT', 'LOCAL_ONLY')
    assert not controller.check_feasibility('LIGHT', 'TRANSMIT')


def test_controller_decision():
    """Test decision making"""
    config = {
        'controller': {
            'weights': {},
            'thresholds': {
                'cpu': 80.0,
                'memory': 80.0,
                'latency_max': 100.0
            }
        }
    }
    
    controller = AdaptiveController(config)
    controller.update_state(cpu_util=50.0, mem_util=50.0, net_latency=50.0, bandwidth=100.0)
    
    mode, transmit = controller.decide()
    
    assert mode in ['LIGHT', 'STANDARD', 'HEAVY']
    assert transmit in ['LOCAL_ONLY', 'TRANSMIT']


def test_controller_static_decision():
    """Test static decision"""
    config = {
        'controller': {
            'weights': {},
            'thresholds': {}
        }
    }
    
    controller = AdaptiveController(config)
    
    mode, transmit = controller.decide_static(mode='STANDARD')
    
    assert mode == 'STANDARD'
    assert transmit == 'LOCAL_ONLY'


def test_controller_centralized_decision():
    """Test centralized decision"""
    config = {
        'controller': {
            'weights': {},
            'thresholds': {}
        }
    }
    
    controller = AdaptiveController(config)
    
    mode, transmit = controller.decide_centralized()
    
    assert mode == 'LIGHT'
    assert transmit == 'TRANSMIT'


def test_controller_reset():
    """Test controller reset"""
    config = {
        'controller': {
            'weights': {},
            'thresholds': {}
        }
    }
    
    controller = AdaptiveController(config)
    controller.update_state(cpu_util=50.0, mem_util=50.0, net_latency=50.0, bandwidth=100.0)
    controller.decision_count = 100
    
    controller.reset()
    
    state = controller.get_state()
    assert state['cpu_util'] == 0.0
    assert state['mem_util'] == 0.0
    assert controller.decision_count == 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
