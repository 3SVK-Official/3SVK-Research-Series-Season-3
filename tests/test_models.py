"""
Unit tests for model implementations
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

import numpy as np
import pytest
import torch
from src.models.isolation_forest import IsolationForestModel
from src.models.autoencoder import AutoencoderModel
from src.models.lstm_autoencoder import LSTMAutoencoderModel


def test_isolation_forest():
    """Test Isolation Forest model"""
    config = {
        'models': {
            'light': {
                'n_estimators': 50,
                'contamination': 0.1,
                'random_state': 42
            }
        }
    }
    
    model = IsolationForestModel(config)
    
    # Create training data
    train_data = np.random.randn(100, 10)
    
    # Fit
    model.fit(train_data)
    assert model.is_fitted
    
    # Predict
    test_data = np.random.randn(20, 10)
    scores, labels = model.predict(test_data)
    
    assert len(scores) == 20
    assert len(labels) == 20
    assert all(0 <= s <= 1 for s in scores)
    assert all(l in [0, 1] for l in labels)


def test_autoencoder():
    """Test Autoencoder model"""
    config = {
        'models': {
            'standard': {
                'hidden_dims': [16, 8],
                'epochs': 5,
                'batch_size': 32,
                'random_state': 42
            }
        }
    }
    
    model = AutoencoderModel(config)
    
    # Create training data (already windowed)
    train_data = np.random.randn(100, 10, 5)
    
    # Fit
    model.fit(train_data)
    assert model.is_fitted
    
    # Predict
    test_data = np.random.randn(20, 10, 5)
    scores, labels = model.predict(test_data)
    
    assert len(scores) == 20
    assert len(labels) == 20
    assert all(0 <= s <= 1 for s in scores)
    assert all(l in [0, 1] for l in labels)


def test_lstm_autoencoder():
    """Test LSTM Autoencoder model"""
    config = {
        'models': {
            'heavy': {
                'hidden_dim': 32,
                'num_layers': 2,
                'epochs': 5,
                'batch_size': 32,
                'random_state': 42
            }
        }
    }
    
    model = LSTMAutoencoderModel(config)
    
    # Create training data (windowed time series)
    train_data = np.random.randn(100, 20, 5)
    
    # Fit
    model.fit(train_data)
    assert model.is_fitted
    
    # Predict
    test_data = np.random.randn(20, 20, 5)
    scores, labels = model.predict(test_data)
    
    assert len(scores) == 20
    assert len(labels) == 20
    assert all(0 <= s <= 1 for s in scores)
    assert all(l in [0, 1] for l in labels)


def test_isolation_forest_2d_input():
    """Test Isolation Forest with 2D input (flattened windows)"""
    config = {
        'models': {
            'light': {
                'n_estimators': 50,
                'contamination': 0.1,
                'random_state': 42
            }
        }
    }
    
    model = IsolationForestModel(config)
    
    # 3D training data
    train_data = np.random.randn(100, 10, 5)
    model.fit(train_data)
    
    # 3D test data
    test_data = np.random.randn(20, 10, 5)
    scores, labels = model.predict(test_data)
    
    assert len(scores) == 20
    assert len(labels) == 20


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
