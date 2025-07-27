import numpy as np
import pickle

from vectorstore.base import BaseVectorStore

class NumPyVectorStore(BaseVectorStore):
    def __init__(self):
        self.vector_data = {}

    def _normalize(self, vector):
        norm = np.linalg.norm(vector)
        return vector / norm if norm > 0 else vector

    def add_vector(self, vector_id, vector, metadata=None):
        norm_vector = self._normalize(vector)
        self.vector_data[vector_id] = {
                "vector":norm_vector,
                "meta":metadata or {}
        }

    def get_vector(self, vector_id):
        entry = self.vector_data.get(vector_id)
        return entry["vector"] if entry else None

    def find_similar_vectors(self, query_vector, num_results=5):
        query_vector = self._normalize(query_vector)
        results = []
        for vector_id, entry in self.vector_data.items():
            similarity = np.dot(query_vector, entry["vector"])
            results.append((vector_id, similarity, entry["meta"]))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:num_results]

    def delete_vector(self, vector_id):
        self.vector_data.pop(vector_id, None)

    def save(self, filepath):
        with open(filepath, "wb") as f:
            pickle.dump(self.vector_data, f)

    @classmethod
    def load(cls, filepath):
        with open(filepath, "rb") as f:
            vector_data = pickle.load(f)
        store = cls()
        store.vector_data = vector_data
        return store
