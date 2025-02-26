import faiss
import numpy as np

class VectorStore:
    def __init__(self, dim=768):
        self.index = faiss.IndexFlatL2(dim)

    def add(self, vectors):
        self.index.add(np.array(vectors, dtype=np.float32))

    def search(self, query_vector, k=5):
        _, indices = self.index.search(np.array([query_vector], dtype=np.float32), k)
        return indices.tolist()

# Sử dụng:
# store = VectorStore()
# store.add([[0.1, 0.2, ..., 0.8]])
# result = store.search([0.1, 0.2, ..., 0.8])
