"""
Unit tests for data loading and streaming
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

import numpy as np
import pytest
from src.data.loader import DataLoader
from src.data.stream import DataStream


def test_data_loader_synthetic():
    """Test synthetic data loading"""
    config = {
        'data': {'data_path': 'data/'},
        'experiments': {'random_seed': 42}
    }
    
    loader = DataLoader(config)
    data, labels = loader.load_dataset('synthetic', n_samples=1000, anomaly_ratio=0.05)
    
    assert data.shape == (1000, 1)
    assert labels.shape == (1000,)
    assert np.sum(labels) > 0  # Should have some anomalies
    assert np.sum(labels) < 1000  # Should not all be anomalies


def test_train_test_split():
    """Test train/test split"""
    config = {
        'data': {'data_path': 'data/'},
        'experiments': {'random_seed': 42}
    }
    
    loader = DataLoader(config)
    data, labels = loader.load_dataset('synthetic', n_samples=1000, anomaly_ratio=0.05)
    
    train_data, test_data, train_labels, test_labels = loader.train_test_split(
        data, labels, test_ratio=0.2
    )
    
    assert len(train_data) == 800
    assert len(test_data) == 200
    assert len(train_labels) == 800
    assert len(test_labels) == 200


def test_data_stream():
    """Test data streaming"""
    data = np.random.randn(100, 1)
    labels = np.random.randint(0, 2, 100)
    
    stream = DataStream(data, labels, buffer_size=50)
    
    count = 0
    for sample, label, timestamp in stream:
        count += 1
        assert sample.shape == (1,)
        assert label in [0, 1]
        assert timestamp == count - 1
    
    assert count == 100


def test_data_stream_reset():
    """Test stream reset"""
    data = np.random.randn(100, 1)
    labels = np.random.randint(0, 2, 100)
    
    stream = DataStream(data, labels, buffer_size=50)
    
    # Consume some samples
    stream_iter = iter(stream)
    for _ in range(50):
        next(stream_iter)
    
    assert stream.index == 50
    
    # Reset
    stream.reset()
    assert stream.index == 0
    assert len(stream.buffer) == 0


def test_data_stream_batch():
    """Test batch retrieval"""
    data = np.random.randn(100, 1)
    labels = np.random.randint(0, 2, 100)
    
    stream = DataStream(data, labels, buffer_size=50)
    
    batch = stream.get_batch(20)
    assert batch is not None
    assert batch[0].shape == (20, 1)
    assert batch[1].shape == (20,)
    
    # Next batch
    batch = stream.get_batch(20)
    assert batch is not None
    assert batch[0].shape == (20, 1)
    
    # Exhaust stream
    for _ in range(3):
        stream.get_batch(20)
    
    batch = stream.get_batch(20)
    assert batch is None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
