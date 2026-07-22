from abc import ABC, abstractmethod
from typing import Mapping
import numpy as np

class StageInterface(ABC):
    
    @abstractmethod
    def connect(self) -> None:
        """Connect to the stage controller."""
        pass

    @abstractmethod
    def move(self, position: Mapping[str, float]) -> None:
        """Move one or more stage axes."""
        pass

    @abstractmethod
    def position(self) -> dict[str, float]:
        """Return the current stage position."""
        pass

    @abstractmethod
    def close(self) -> None:
        """Close the stage connection."""
        pass


class DetectorInterface(ABC):

    @abstractmethod
    def connect(self) -> None:
        """Connect to and initialize the detector."""
        pass

    @abstractmethod
    def poll_counts(self) -> np.ndarray:
        """Return the current count rate for each channel."""
        pass

    @abstractmethod
    def integrate_counts(self, acquisition_ms: int) -> np.ndarray:
        """Acquire integrated counts for a specified duration."""
        pass

    @abstractmethod
    def close(self) -> None:
        """Close the detector connection."""
        pass