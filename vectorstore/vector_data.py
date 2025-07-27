# vectorstore/vector_data
import os
from vectorstore.numpy_store import NumPyVectorStore

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # vectorstore folder
_VECTOR_STORE_PATH = os.path.join(_BASE_DIR, "vectorstore.pkl")

_vector_store = None

def get_vector_store():
    global _vector_store
    if _vector_store is None:
        if not os.path.exists(_VECTOR_STORE_PATH):
            raise FileNotFoundError(f"Vector store not found at: {_VECTOR_STORE_PATH}")
        print(f"Loading vector store from {_VECTOR_STORE_PATH}")
        _vector_store = NumPyVectorStore.load(_VECTOR_STORE_PATH)
        print(f"Loaded vector store with {len(_vector_store.vector_data)} vectors")
    else:
        print(f"Loading vector store from {_VECTOR_STORE_PATH} failed.")
    return _vector_store
