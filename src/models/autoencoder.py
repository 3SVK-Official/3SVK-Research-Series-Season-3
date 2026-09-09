"""
Autoencoder model for anomaly detection
"""

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from typing import Tuple, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Autoencoder(nn.Module):
    """Autoencoder neural network"""
    
    def __init__(self, input_dim: int, hidden_dims: list, activation: str = 'relu'):
        """
        Initialize autoencoder
        
        Args:
            input_dim: Input dimension
            hidden_dims: List of hidden layer dimensions
            activation: Activation function
        """
        super(Autoencoder, self).__init__()
        
        self.hidden_dims = hidden_dims
        self.activation = activation
        
        # Encoder
        encoder_layers = []
        prev_dim = input_dim
        for dim in hidden_dims:
            encoder_layers.append(nn.Linear(prev_dim, dim))
            if activation == 'relu':
                encoder_layers.append(nn.ReLU())
            elif activation == 'tanh':
                encoder_layers.append(nn.Tanh())
            elif activation == 'sigmoid':
                encoder_layers.append(nn.Sigmoid())
            prev_dim = dim
        
        self.encoder = nn.Sequential(*encoder_layers)
        
        # Decoder (reverse of encoder)
        decoder_layers = []
        for dim in reversed(hidden_dims[:-1]):
            decoder_layers.append(nn.Linear(prev_dim, dim))
            if activation == 'relu':
                decoder_layers.append(nn.ReLU())
            elif activation == 'tanh':
                decoder_layers.append(nn.Tanh())
            elif activation == 'sigmoid':
                decoder_layers.append(nn.Sigmoid())
            prev_dim = dim
        
        decoder_layers.append(nn.Linear(prev_dim, input_dim))
        self.decoder = nn.Sequential(*decoder_layers)
    
    def forward(self, x):
        """Forward pass"""
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded


class AutoencoderModel:
    """
    Autoencoder model for anomaly detection
    """
    
    def __init__(self, config: dict):
        """
        Initialize Autoencoder model
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        model_config = config.get('models', {}).get('standard', {})
        
        self.hidden_dims = config.get('models', {}).get('autoencoder', {}).get('hidden_dims', [32, 16, 32])
        self.activation = config.get('models', {}).get('autoencoder', {}).get('activation', 'relu')
        self.epochs = config.get('models', {}).get('autoencoder', {}).get('epochs', 50)
        self.batch_size = config.get('models', {}).get('autoencoder', {}).get('batch_size', 32)
        self.learning_rate = config.get('models', {}).get('autoencoder', {}).get('learning_rate', 0.001)
        self.contamination = config.get('models', {}).get('autoencoder', {}).get('contamination', 0.05)
        self.random_state = config.get('experiments', {}).get('random_seed', 42)
        
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = None
        self.threshold = None
        self.is_fitted = False
        
        # Store normalization parameters from training
        self.score_min = None
        self.score_max = None
        
        torch.manual_seed(self.random_state)
    
    def _get_activation(self, activation: str):
        """Get activation function"""
        if activation == 'relu':
            return nn.ReLU()
        elif activation == 'tanh':
            return nn.Tanh()
        elif activation == 'sigmoid':
            return nn.Sigmoid()
        else:
            return nn.ReLU()
        
    def _prepare_data(self, X: np.ndarray) -> torch.utils.data.DataLoader:
        """
        Prepare data for training
        
        Args:
            X: Input data
            
        Returns:
            DataLoader
        """
        # Flatten if 3D (windows)
        if len(X.shape) == 3:
            X = X.reshape(X.shape[0], -1)
        
        X_tensor = torch.FloatTensor(X).to(self.device)
        dataset = torch.utils.data.TensorDataset(X_tensor)
        dataloader = torch.utils.data.DataLoader(
            dataset, 
            batch_size=self.batch_size, 
            shuffle=True
        )
        return dataloader
    
    def fit(self, X_train: np.ndarray) -> None:
        """
        Fit the Autoencoder model
        
        Args:
            X_train: Training data (n_samples, window_size, n_features)
        """
        # Flatten if 3D (windows)
        if len(X_train.shape) == 3:
            X_train = X_train.reshape(X_train.shape[0], -1)
        
        input_dim = X_train.shape[1]
        
        # Build encoder layers
        encoder_layers = []
        prev_dim = input_dim
        for hidden_dim in self.hidden_dims:
            encoder_layers.append(nn.Linear(prev_dim, hidden_dim))
            encoder_layers.append(self._get_activation(self.activation))
            prev_dim = hidden_dim
        
        # Build decoder layers (reverse)
        decoder_layers = []
        for hidden_dim in reversed(self.hidden_dims[:-1]):
            decoder_layers.append(nn.Linear(prev_dim, hidden_dim))
            decoder_layers.append(self._get_activation(self.activation))
            prev_dim = hidden_dim
        decoder_layers.append(nn.Linear(prev_dim, input_dim))
        
        self.encoder = nn.Sequential(*encoder_layers)
        self.decoder = nn.Sequential(*decoder_layers)
        
        self.model = nn.Sequential(self.encoder, self.decoder)
        self.model.to(self.device)
        
        # Training
        optimizer = torch.optim.Adam(self.model.parameters(), lr=self.learning_rate)
        criterion = nn.MSELoss()
        
        for epoch in range(self.epochs):
            self.model.train()
            X_tensor = torch.FloatTensor(X_train).to(self.device)
            
            optimizer.zero_grad()
            reconstructed = self.model(X_tensor)
            loss = criterion(reconstructed, X_tensor)
            loss.backward()
            optimizer.step()
            
            if (epoch + 1) % 10 == 0:
                logger.info(f"Epoch {epoch + 1}/{self.epochs}, Loss: {loss.item():.6f}")
        
        # Calculate threshold for anomaly detection (will be overridden by calibration)
        self.model.eval()
        with torch.no_grad():
            X_tensor = torch.FloatTensor(X_train).to(self.device)
            reconstructed = self.model(X_tensor)
            reconstruction_error = torch.mean((X_tensor - reconstructed) ** 2, dim=1)
            reconstruction_error = reconstruction_error.cpu().numpy()
        
        # Store normalization parameters from training
        self.score_min = np.min(reconstruction_error)
        self.score_max = np.max(reconstruction_error)
        
        # Store raw threshold for reference
        self.raw_threshold = np.percentile(reconstruction_error, (1 - self.contamination) * 100)
        self.threshold = self.raw_threshold  # Default for backward compatibility
        self.is_fitted = True
        
        logger.info(f"Autoencoder fitted on {X_train.shape}, input_dim={input_dim}")
    
    def _compute_loss(self, X: np.ndarray) -> float:
        """Compute reconstruction loss"""
        self.model.eval()
        with torch.no_grad():
            if len(X.shape) == 3:
                X = X.reshape(X.shape[0], -1)
            X_tensor = torch.FloatTensor(X).to(self.device)
            reconstructed = self.model(X_tensor)
            loss = nn.MSELoss()(reconstructed, X_tensor)
        return loss.item()
    
    def predict_scores(self, X: np.ndarray) -> np.ndarray:
        """
        Predict anomaly scores only (no thresholding)
        
        Args:
            X: Input data (n_samples, window_size, n_features)
            
        Returns:
            Anomaly scores (higher = more anomalous)
        """
        if not self.is_fitted:
            raise ValueError("Model not fitted")
        
        # Flatten 3D input to 2D
        if len(X.shape) == 3:
            X = X.reshape(X.shape[0], -1)
        
        self.model.eval()
        
        with torch.no_grad():
            X_tensor = torch.FloatTensor(X).to(self.device)
            reconstructed = self.model(X_tensor)
            
            # Calculate reconstruction error
            reconstruction_error = torch.mean((X_tensor - reconstructed) ** 2, dim=1)
            reconstruction_error = reconstruction_error.cpu().numpy()
        
        # Normalize scores to [0, 1] using training parameters
        if self.score_max - self.score_min > 0:
            anomaly_scores = (reconstruction_error - self.score_min) / (self.score_max - self.score_min)
        else:
            anomaly_scores = np.zeros_like(reconstruction_error)
        
        logger.info(f"Predicted {len(anomaly_scores)} samples")
        return anomaly_scores
    
    def predict(self, X: np.ndarray, threshold: Optional[float] = None) -> Tuple[np.ndarray, np.ndarray]:
        """
        Predict anomalies with threshold (for backward compatibility)
        
        Args:
            X: Input data (n_samples, window_size, n_features)
            threshold: Threshold for binary classification (uses fitted threshold if None)
            
        Returns:
            Tuple of (anomaly_scores, anomaly_labels)
        """
        anomaly_scores = self.predict_scores(X)
        
        if threshold is None:
            threshold = self.threshold
        
        # Convert normalized threshold back to reconstruction error space if needed
        # For simplicity, we apply threshold to normalized scores
        anomaly_labels = (anomaly_scores >= threshold).astype(int)
        return anomaly_scores, anomaly_labels
    
    def get_params(self) -> dict:
        """Get model parameters"""
        return {
            'hidden_dims': self.hidden_dims,
            'activation': self.activation,
            'epochs': self.epochs,
            'batch_size': self.batch_size,
            'learning_rate': self.learning_rate
        }
