from abc import ABC, abstractmethod
import numpy as np

class BaseVectorStore(ABC):
    @abstractmethod
    def add_vector(self, vector_id: str, vector: np.ndarray, metadata: dict = None):
        pass

    @abstractmethod
    def find_similar_vectors(self, query_vector: np.ndarray, num_results: int = 5):
        pass

    @abstractmethod
    def get_vector(self, vector_id: str) -> np.ndarray:
        pass

    @abstractmethod
    def delete_vector(self, vector_id: str):
        pass

