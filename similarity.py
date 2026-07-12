from sklearn.metrics.pairwise import cosine_similarity

def compare_embeddings(embedding1: list, embedding2: list) -> float:
    """
    Computes cosine similarity between two embeddings.

    Returns a value between -1 and 1.
    """

    similarity = cosine_similarity(
        [embedding1],
        [embedding2]
    )[0][0]

    return float(similarity)