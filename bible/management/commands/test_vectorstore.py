from django.core.management.base import BaseCommand
from sentence_transformers import SentenceTransformer
from vectorstore.numpy_store import NumPyVectorStore
import os

class Command(BaseCommand):
    help = "Test the saved vector store"

    def handle(self, *args, **options):
        # Load vector store
        path = "vectorstore/vectorstore.pkl"  # Or provide full path if needed
        if not os.path.exists(path):
            self.stderr.write(f"Vector store file not found: {path}")
            return

        vector_store = NumPyVectorStore.load(path)
        self.stdout.write("Vector store loaded!")

        # Load embedding model
        model = SentenceTransformer('all-MiniLM-L6-v2')

        # Encode a query
        query = "God's love for humanity"
        query_vector = model.encode(query)

        # Search
        results = vector_store.find_similar_vectors(query_vector, num_results=5)

        # Display results
        self.stdout.write(f"\nTop results for query: '{query}'")
        for i, (vector_id, score, metadata) in enumerate(results, start=1):
            self.stdout.write(f"{i}. {vector_id} (score: {score:.4f})")
            self.stdout.write(f"   Meta: {metadata}")

