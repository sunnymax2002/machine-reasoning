import numpy as np

# Coside Similarity: https://datastax.medium.com/how-to-implement-cosine-similarity-in-python-505e8ec1d823
def cosine_similarity(A, B):
    dot_product = np.dot(A, B)
    magnitude_A = np.linalg.norm(A)
    magnitude_B = np.linalg.norm(B)

    cosine_similarity = dot_product / (magnitude_A * magnitude_B)
    # print(f"Cosine Similarity using NumPy: {cosine_similarity}")
    return cosine_similarity

def nearest_vector(vec, vec_list):
    """Uses cosine similarity to find index of closest vector in 'vec_list' to the provided vector 'vec'"""
    sims = []
    for v in vec_list:
        sims.append(cosine_similarity(vec, v))

    best_match = sims.index(max(sims))

    return best_match