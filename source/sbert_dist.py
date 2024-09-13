#REF: https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2

from sentence_transformers import SentenceTransformer
sentences = ["This is an example sentence", "Each sentence is converted"]

def sbert_embeddings(sentences):
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    embeddings = model.encode(sentences)

    return embeddings
    # print(embeddings)

# Coside Similarity: https://datastax.medium.com/how-to-implement-cosine-similarity-in-python-505e8ec1d823
import numpy as np

def cosine_similarity(A, B):
    dot_product = np.dot(A, B)
    magnitude_A = np.linalg.norm(A)
    magnitude_B = np.linalg.norm(B)

    cosine_similarity = dot_product / (magnitude_A * magnitude_B)
    # print(f"Cosine Similarity using NumPy: {cosine_similarity}")
    return cosine_similarity