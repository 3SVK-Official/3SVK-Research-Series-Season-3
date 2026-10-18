"""
LSTM Autoencoder model for anomaly detection
"""

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from typing import Tuple, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LSTMAutoencoder(nn.Module):
    """LSTM Autoencoder neural network"""
    
    def __init__(self, input_dim: int, hidden_dim: int, num_layers: int = 2, dropout: float = 0.2):
        """
        Initialize LSTM Autoencoder
        
        Args:
            input_dim: Input feature dimension
            hidden_dim: Hidden dimension
            num_layers: Number of LSTM layers
            dropout: Dropout rate
        """
        super(LSTMAutoencoder, self).__init__()
        
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        
        # Encoder LSTM
        self.encoder_lstm = nn.LSTM(
            input_dim, 
            hidden_dim, 
            num_layers=num_layers, 
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0
        )
        
        # Decoder LSTM
        self.decoder_lstm = nn.LSTM(
            hidden_dim, 
            hidden_dim, 
            num_layers=num_layers, 
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0
        )
        
        # Output layer
        self.output_layer = nn.Linear(hidden_dim, input_dim)
    
    def forward(self, x):
        """Forward pass"""
        # Encode
        encoder_outputs, (hidden, cell) = self.encoder_lstm(x)
        
        # Decode
        decoder_outputs, _ = self.decoder_lstm(encoder_outputs, (hidden, cell))
        
        # Output
        reconstructed = self.output_layer(decoder_outputs)
        
        return reconstructed


class LSTMAutoencoderModel:
    """
    LSTM Autoencoder model for anomaly detection
    """
    
    def __init__(self, config: dict):
        """
        Initialize LSTM Autoencoder model
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        model_config = config.get('models', {}).get('heavy', {})
        
        self.hidden_dim = model_config.get('hidden_dim', 64)
        self.num_layers = model_config.get('num_layers', 2)
        self.dropout = model_config.get('dropout', 0.2)
        self.epochs = model_config.get('epochs', 100)
        self.batch_size = model_config.get('batch_size', 32)
        self.learning_rate = model_config.get('learning_rate', 0.001)
        self.early_stopping_patience = model_config.get('early_stopping_patience', 10)
        self.random_state = model_config.get('random_state', 42)
        
        self.model = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.is_fitted = False
        
        torch.manual_seed(self.random_state)
        
    def _prepare_data(self, X: np.ndarray) -> torch.utils.data.DataLoader:
        """
        Prepare data for training
        
        Args:
            X: Input data (n_samples, window_size, n_features)
            
        Returns:
            DataLoader
        """
        # Ensure 3D shape
        if len(X.shape) == 2:
            X = X.reshape(X.shape[0], -1, 1)
        
        X_tensor = torch.FloatTensor(X).to(self.device)
        dataset = torch.utils.data.TensorDataset(X_tensor)
        dataloader = torch.utils.data.DataLoader(
            dataset, 
            batch_size=self.batch_size, 
            shuffle=True
        )
        return dataloader
    
    def fit(self, X_train: np.ndarray, validation_data: Optional[np.ndarray] = None) -> None:
        """
        Fit the LSTM Autoencoder model
        
        Args:
            X_train: Training data (n_samples, window_size, n_features)
            validation_data: Optional validation data
        """
        # Ensure 3D shape
        if len(X_train.shape) == 2:
            X_train = X_train.reshape(X_train.shape[0], -1, 1)
        
        _, seq_len, input_dim = X_train.shape
        self.model = LSTMAutoencoder(input_dim, self.hidden_dim, self.num_layers, self.dropout).to(self.device)
        
        criterion = nn.MSELoss()
        optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)
        
        train_loader = self._prepare_data(X_train)
        
        best_loss = float('inf')
        patience_counter = 0
        
        for epoch in range(self.epochs):
            self.model.train()
            epoch_loss = 0
            
            for batch in train_loader:
                x_batch = batch[0]
                
                optimizer.zero_grad()
                reconstructed = self.model(x_batch)
                loss = criterion(reconstructed, x_batch)
                loss.backward()
                optimizer.step()
                
                epoch_loss += loss.item()
            
            avg_loss = epoch_loss / len(train_loader)
            
            # Early stopping
            if validation_data is not None:
                val_loss = self._compute_loss(validation_data)
                if val_loss < best_loss:
                    best_loss = val_loss
                    patience_counter = 0
                else:
                    patience_counter += 1
                    if patience_counter >= self.early_stopping_patience:
                        logger.info(f"Early stopping at epoch {epoch}")
                        break
            
            if (epoch + 1) % 10 == 0:
                logger.info(f"Epoch {epoch + 1}/{self.epochs}, Loss: {avg_loss:.6f}")
        
        self.is_fitted = True
        logger.info(f"LSTM Autoencoder fitted on {X_train.shape}")
    
    def _compute_loss(self, X: np.ndarray) -> float:
        """Compute reconstruction loss"""
        self.model.eval()
        with torch.no_grad():
            if len(X.shape) == 2:
                X = X.reshape(X.shape[0], -1, 1)
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
        
        self.model.eval()
        
        # Ensure 3D shape
        if len(X.shape) == 2:
            X = X.reshape(X.shape[0], -1, 1)
        
        with torch.no_grad():
            X_tensor = torch.FloatTensor(X).to(self.device)
            reconstructed = self.model(X_tensor)
            
            # Compute reconstruction error per time step, then average
            reconstruction_errors = torch.mean((X_tensor - reconstructed) ** 2, dim=(1, 2))
            anomaly_scores = reconstruction_errors.cpu().numpy()
        
        # Normalize scores to [0, 1]
        min_score = np.min(anomaly_scores)
        max_score = np.max(anomaly_scores)
        if max_score - min_score > 0:
            anomaly_scores_normalized = (anomaly_scores - min_score) / (max_score - min_score)
        else:
            anomaly_scores_normalized = np.zeros_like(anomaly_scores)
        
        logger.info(f"Predicted {len(anomaly_scores_normalized)} samples")
        return anomaly_scores_normalized
    
    def predict(self, X: np.ndarray, threshold: Optional[float] = None) -> Tuple[np.ndarray, np.ndarray]:
        """
        Predict anomalies with threshold (for backward compatibility)
        
        Args:
            X: Input data (n_samples, window_size, n_features)
            threshold: Threshold for binary classification (uses median if None)
            
        Returns:
            Tuple of (anomaly_scores, anomaly_labels)
        """
        anomaly_scores = self.predict_scores(X)
        
        if threshold is None:
            threshold = np.median(anomaly_scores)
        
        anomaly_labels = (anomaly_scores >= threshold).astype(int)
        return anomaly_scores, anomaly_labels
    
    def get_params(self) -> dict:
        """Get model parameters"""
        return {
            'hidden_dim': self.hidden_dim,
            'num_layers': self.num_layers,
            'dropout': self.dropout,
            'epochs': self.epochs,
            'batch_size': self.batch_size,
            'learning_rate': self.learning_rate
        }
