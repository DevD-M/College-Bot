from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

model = SentenceTransformer('all-MiniLM-L6-v2')

index = faiss.read_index('bennett.index')
with open('chunks.pkl', 'rb') as f:
    chunks = pickle.load(f)

def retrieve(query, top_k=2):
    query_vector = model.encode([query])
    distances, indices = index.search(np.array(query_vector), top_k)
    results = []
    for i in indices[0]:
        results.append(chunks[i])
    return results

if __name__ == "__main__":
    query = "What are the fees at Bennett University?"
    results = retrieve(query)
    print(f"Query: {query}\n")
    for i, chunk in enumerate(results):
        print(f"Result {i+1}:\n{chunk}\n")