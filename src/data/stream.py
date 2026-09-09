"""
Data stream for real-time processing simulation
"""

import numpy as np
from collections import deque
from typing import Iterator, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataStream:
    """
    Simulates streaming data for real-time processing
    """
    
    def __init__(self, data: np.ndarray, labels: np.ndarray, buffer_size: int = 1000):
        """
        Initialize data stream
        
        Args:
            data: Feature data
            labels: Label data
            buffer_size: Size of the circular buffer
        """
        self.data = data
        self.labels = labels
        self.buffer_size = buffer_size
        self.buffer = deque(maxlen=buffer_size)
        self.index = 0
        
    def __iter__(self) -> Iterator[tuple]:
        """
        Iterate over the data stream
        
        Yields:
            Tuple of (sample, label, timestamp)
        """
        while self.index < len(self.data):
            sample = self.data[self.index]
            label = self.labels[self.index]
            timestamp = self.index
            
            self.buffer.append((sample, label, timestamp))
            self.index += 1
            
            yield sample, label, timestamp
    
    def reset(self):
        """Reset the stream to the beginning"""
        self.index = 0
        self.buffer.clear()
    
    def get_batch(self, batch_size: int) -> Optional[tuple]:
        """
        Get a batch of samples
        
        Args:
            batch_size: Number of samples in the batch
            
        Returns:
            Tuple of (batch_data, batch_labels) or None if exhausted
        """
        if self.index >= len(self.data):
            return None
        
        end_idx = min(self.index + batch_size, len(self.data))
        batch_data = self.data[self.index:end_idx]
        batch_labels = self.labels[self.index:end_idx]
        
        self.index = end_idx
        return batch_data, batch_labels
    
    def peek(self, n: int = 1) -> Optional[np.ndarray]:
        """
        Peek at the next n samples without advancing
        
        Args:
            n: Number of samples to peek
            
        Returns:
            Array of samples or None if exhausted
        """
        if self.index + n > len(self.data):
            return None
        return self.data[self.index:self.index + n]
