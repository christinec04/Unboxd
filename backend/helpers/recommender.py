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

def find_representative_movie(movies: np.ndarray, weights: np.ndarray) -> int:
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
        user_movies: np.ndarray, weights: np.ndarray, user_movie_ids: set[str], 
        all_movies: np.ndarray, all_movie_ids: list[str], k: int = 10
        ) -> dict[str, float]:
    """
    Generates up to `k` movie recommendations by first finding a representative movie
    from user activity and then performing a k-NN search against the 
    full movie database.
    Args:
        `user_movies`: Feature vectors for movies used to build the profile.
        `weights`: Weights used to bias the representative profile selection.
        `user_movie_ids`: IDs of the movies rated and reviewd by the user.
        `all_movies`: Feature vectors of the full search space.
        `all_movies_ids`: IDs of the movies in the search space.
        `k`: The number of neighbors (recommendations) to return.
    Returns:
        A list of (movie id, similarity score) tuples for the top `k` recommendations.
    """
    representative_index = find_representative_movie(user_movies, weights)
    # Retrieve feature vector of the representative movie
    representative_vector = user_movies[representative_index]

    # Reshape the representative movie's feature vector for sklearn's euclidian_distances function
    representative_vector_reshaped = representative_vector.reshape(1, -1)
    # Calculate Euclidian distance between the representative movie and all movie feature vectors
    distances = euclidean_distances(representative_vector_reshaped, all_movies)[0]

    # Combine movie ID and distance
    movie_distances = list(zip(distances, all_movie_ids))

    # Sort by distance (ascending)
    movie_distances.sort()

    recommendations = {}
    for distance, movie_id in movie_distances:
            # Translate Euclidian distance to a similarity score
            similarity_score = 1 / (1 + distance)

            # Ensure the movie hasn't been watched
            if movie_id not in user_movie_ids:
                    recommendations[movie_id] = similarity_score

            if len(recommendations) >= k:
                    break
    return recommendations
