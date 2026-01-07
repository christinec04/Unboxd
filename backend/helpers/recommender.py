import numpy as np
from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances

def cosine_similarity(movie1: np.ndarray, movie2: np.ndarray) -> float:
    """
    Calculate the cosine similarity between two movies based on their feature vectors.
    Args:
        `movie1`: Feature vectors of the first movie.
        `movie2`: Feature vectors of the second movie.
    Returns:
        The cosine similarity score between the two movies.
    """
    similarity = sklearn_cosine_similarity(movie1.reshape(1, -1), movie2.reshape(1, -1))    
    return similarity[0][0]

def precompute_similarity_matrix(all_movies: np.ndarray) ->np.ndarray:
     """
     Precompute the cosine similarity matrix for all movies.
     Args:
        `all_movies`: Feature vectors of all movies in the database.
    Returns:
        A matrix where element [i,j] contains the cosine similarity between movie i and movie j.
     """
     return sklearn_cosine_similarity(all_movies)

def find_representative_movie(movies: np.ndarray, weights: list[float]) -> int:
    """
    Find the most representative movie from a list of movies based on weighted total cosine similarity.
    Args:
        `movies`: Feature vectors of movies.
        `weights`: Weights corresponding to the sentiment (compound) and user rating of each movie.
    Returns:
        The index of the most representative movie in the input list.
    """
    n = len(movies)
    max_total_similarity = -1
    representative_index = -1
    
    # Iterate through each movie to calculate its weighted total cosine similarity with all other movies
    for i in range(n):
        total_similarity = 0
        for j in range(n):
            if i != j:
                similarity = cosine_similarity(movies[i], movies[j])
                weighted_similarity = similarity * weights[j]
                total_similarity += weighted_similarity
        
        # Update the representative movie if the current one has a higher total similarity
        if total_similarity > max_total_similarity:
            max_total_similarity = total_similarity
            representative_index = i    
            
    # Return the index of the most representative movie
    return representative_index

def recommend_movies(
        user_movies: np.ndarray, weights: list[float], user_movie_ids: set[str], 
        all_movies: np.ndarray, all_movie_ids: list[str], k: int = 10,
        similarity_matrix: np.ndarray = None
        ) -> dict[str, float]:
    """
    Generates up to `k` movie recommendations by first finding a representative movie
    from user activity and then performing a k-NN search against the 
    full movie database using cosine similarity.
    Args:
        `user_movies`: Feature vectors for movies used to build the profile.
        `weights`: Weights used to bias the representative profile selection.
        `user_movie_ids`: IDs of the movies rated and reviewd by the user.
        `all_movies`: Feature vectors of the full search space.
        `all_movies_ids`: IDs of the movies in the search space.
        `k`: The number of neighbors (recommendations) to return.
        `similarity_matrix`: Precomputed cosine similarity matrix
    Returns:
        A dictionary of {movie_id, similarity_score} for the top `k` recommendations.
    """
    # Find the representative movie from user's watched movies
    representative_index = find_representative_movie(user_movies, weights)
    representative_vector = user_movies[representative_index]

    # Calculate cosine similarities between representative movie and all movies
    if similarity_matrix is None:
         similarities = sklearn_cosine_similarity(representative_vector.reshape(1, -1), all_movies)[0]
    else:
         similarities = sklearn_cosine_similarity(representative_vector.reshape(1, -1), all_movies)[0]
    
    # Combine movie IDs with their similarity scores
    movie_similarities = list(zip(similarities, all_movie_ids))

    # Sort by similarity (descending - highest similarity first)
    movie_similarities.sort(reverse=True)

    # Build recommendations dictionary, excluding already-watched movies
    recommendations = {}
    for similarity_score, movie_id in movie_similarities:
        # Skip movies the user has already watched
        if movie_id not in user_movie_ids:
            recommendations[movie_id] = similarity_score
        
        # Stop once k is reached
        if len(recommendations) >= k:
            break
    
    return recommendations
