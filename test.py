from sentence_transformers import SentenceTransformer
from vectorstore.numpy_store import NumPyVectorStore  # Adjust import as needed

# Initialize vector store
vector_store = NumPyVectorStore()

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Example text passages (replace these with your own Bible passages or any text)
passages = [
    "In the beginning God created the heavens and the earth.",
    "For God so loved the world that he gave his one and only Son.",
    "The Lord is my shepherd; I shall not want.",
    "I can do all things through Christ who strengthens me.",
]

# Encode passages to vectors
embeddings = model.encode(passages)

# Add passages and their embeddings to the vector store
for passage, embedding in zip(passages, embeddings):
    metadata = {"source": "bible_app"}
    vector_store.add_vector(passage, embedding, metadata)

# Query to find similar passages
query_sentence = "God created the world in the beginning."
query_embedding = model.encode([query_sentence])[0]

# Retrieve top 3 similar passages
results = vector_store.find_similar_vectors(query_embedding, num_results=3)

# Display results
print(f"Query: {query_sentence}")
print("Top similar passages:")
for passage_id, similarity, meta in results:
    print(f"- Passage: {passage_id}")
    print(f"  Similarity: {similarity:.4f}")
    print(f"  Metadata: {meta}")

