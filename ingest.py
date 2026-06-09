from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
import os

model = SentenceTransformer('all-MiniLM-L6-v2')

all_chunks = []

for filename in os.listdir('data'):
    if filename.endswith('.txt'):
        with open(f'data/{filename}', 'r', encoding='utf-8') as f:
            text = f.read()
        lines = [l.strip() for l in text.splitlines() if len(l.strip()) > 0]
        chunks = []
        for i in range(0, len(lines), 10):
            chunk = ' '.join(lines[i:i+10])
            if len(chunk) > 50:
                chunks.append(chunk)
        print(f"{filename}: {len(chunks)} chunks")
        all_chunks.extend(chunks)

print(f"\nTotal chunks: {len(all_chunks)}")

embeddings = model.encode(all_chunks, show_progress_bar=True)
print(f"Embedding shape: {embeddings.shape}")

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

faiss.write_index(index, 'bennett.index')
with open('chunks.pkl', 'wb') as f:
    pickle.dump(all_chunks, f)

print("\nIndex saved successfully!")