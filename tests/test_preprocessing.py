"""
Unit tests for preprocessing
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

import numpy as np
import pytest
from src.preprocessing.preprocessor import Preprocessor
from src.preprocessing.feature_engineering import FeatureEngineer


def test_preprocessor_minmax():
    """Test min-max normalization"""
    config = {
        'preprocessing': {'normalize': True, 'normalization_method': 'minmax'},
        'data': {'window_size': 10}
    }
    
    preprocessor = Preprocessor(config)
    data = np.random.randn(100, 1) * 10 + 5
    
    normalized = preprocessor.normalize_data(data, fit=True)
    
    assert normalized.min() >= 0
    assert normalized.max() <= 1
    assert preprocessor.min_val is not None
    assert preprocessor.max_val is not None


def test_preprocessor_zscore():
    """Test z-score normalization"""
    config = {
        'preprocessing': {'normalize': True, 'normalization_method': 'zscore'},
        'data': {'window_size': 10}
    }
    
    preprocessor = Preprocessor(config)
    data = np.random.randn(100, 1) * 10 + 5
    
    normalized = preprocessor.normalize_data(data, fit=True)
    
    assert abs(normalized.mean()) < 0.1  # Should be close to 0
    assert abs(normalized.std() - 1.0) < 0.1  # Should be close to 1


def test_preprocessor_windows():
    """Test window creation"""
    config = {
        'preprocessing': {'normalize': False},
        'data': {'window_size': 10}
    }
    
    preprocessor = Preprocessor(config)
    data = np.random.randn(100, 1)
    
    windows = preprocessor.create_windows(data)
    
    assert windows.shape == (91, 10, 1)  # 100 - 10 + 1 = 91 windows


def test_preprocessor_fit_transform():
    """Test fit_transform"""
    config = {
        'preprocessing': {'normalize': True, 'normalization_method': 'minmax'},
        'data': {'window_size': 10}
    }
    
    preprocessor = Preprocessor(config)
    data = np.random.randn(100, 1)
    
    result = preprocessor.fit_transform(data)
    
    assert len(result.shape) == 3
    assert result.shape[1] == 10


def test_preprocessor_inverse_normalize():
    """Test inverse normalization"""
    config = {
        'preprocessing': {'normalize': True, 'normalization_method': 'minmax'},
        'data': {'window_size': 10}
    }
    
    preprocessor = Preprocessor(config)
    original = np.random.randn(100, 1) * 10 + 5
    
    normalized = preprocessor.normalize_data(original, fit=True)
    denormalized = preprocessor.inverse_normalize(normalized)
    
    np.testing.assert_array_almost_equal(original, denormalized, decimal=5)


def test_feature_engineer_disabled():
    """Test feature engineer when disabled"""
    config = {
        'preprocessing': {'feature_engineering': False},
        'data': {'window_size': 10}
    }
    
    engineer = FeatureEngineer(config)
    data = np.random.randn(100, 1)
    
    result = engineer.fit_transform(data)
    
    assert result.shape == data.shape


def test_feature_engineer_rolling():
    """Test rolling features"""
    config = {
        'preprocessing': {
            'feature_engineering': True,
            'rolling_features': ['mean', 'std']
        },
        'data': {'window_size': 10}
    }
    
    engineer = FeatureEngineer(config)
    data = np.random.randn(100, 1)
    
    result = engineer.fit_transform(data)
    
    # Original + mean + std + diff1 + diff2 = 5 features (feature engineer adds diff features by default)
    # Actually the implementation adds both rolling AND diff features
    # Original (1) + rolling mean (1) + rolling std (1) + diff1 (1) + diff2 (1) = 5
    # But diff features are applied to all features, so:
    # Original (1) + rolling mean (1) + rolling std (1) = 3
    # Then diff features applied to all 3: diff1 (3) + diff2 (3) = 6
    # Total = 3 + 6 = 9
    assert result.shape[1] == 9


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
