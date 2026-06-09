from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

model = SentenceTransformer('all-MiniLM-L6-v2')

with open('data/bennettuni_info.txt', 'r') as f:
    text = f.read()

chunks = [chunk.strip() for chunk in text.split('\n\n') if chunk.strip()]

print(f"Total chunks: {len(chunks)}")
for i, chunk in enumerate(chunks):
    print(f"\nChunk {i}: {chunk[:60]}...")

embeddings = model.encode(chunks)
print(f"\nEmbedding shape: {embeddings.shape}")

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

faiss.write_index(index, 'bennett.index')
with open('chunks.pkl', 'wb') as f:
    pickle.dump(chunks, f)

print("\nIndex saved successfully!")