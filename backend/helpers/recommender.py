import numpy as np
from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances
from operator import itemgetter

def cosine_similarity(movie1, movie2):
    """
    Calculate the cosine similarity between two movies based on their feature vectors.
    Args:
        movie1 (list): A list containing the feature vectors of the first movie.
        movie2 (list): A list containing the feature vectors of the second movie.
    Returns:
        float: The cosine similarity score between the two movies.
    """
    # Concatenate the feature vectors of each movie into a single vector
    movie1_vector = np.concatenate([np.array(f) for f in movie1])
    movie2_vector = np.concatenate([np.array(f) for f in movie2])
    
    similarity = sklearn_cosine_similarity(movie1_vector.reshape(1, -1),
                               movie2_vector.reshape(1, -1))
    
    return similarity[0][0]

def find_representative_movie(movies, weights):
    """
    Find the most representative movie from a list of movies based on weighted total cosine similarity.
    Args:
        movies (list): A list of lists, where each inner list contains the feature vectors of a movie.
        weights (list): A list of weights corresponding to the positive sentiment (compound) of each movie.
    Returns:
        int: The index of the most representative movie in the input list.
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

def recommend_movies(user_movies, weights, watched_ids, all_movies, k=10):
    """
    Generates k movie recommendations by first finding a representative movie
    from user activity and then performing a k-NN search against the 
    full movie database.
    Args:
        user_movies (list): Feature vectors for movies used to build the profile.
        weights (list): Sentiment weights used to bias the representative profile selection.
        all_movies (dict): Dictionary mapping movie_id to feature_vector (the full search space).
        k (int): The number of neighbors (recommendations) to return.
    Returns:
        list: A list of (movie_id, similarity_score) tuples for the top k recommendations.
    """
    representative_index = find_representative_movie(user_movies, weights)
    # Retrieve feature vector of the representative movie
    representative_vector = np.concatenate([np.array(f) for f in user_movies[representative_index]])

    all_movie_ids = list(all_movies.keys())
    # Retrieve feature vectors of all the movies from the dataset
    all_movie_vectors = np.array([
        np.concatenate([np.array(f) for f in v]) 
        for v in all_movies.values()
    ])

    # Reshape the representative movie's feature vector for sklearn's euclidian_distances function
    representative_vector_reshaped = representative_vector.reshape(1, -1)
    # Calculate Euclidian distance between the representative movie and all movie feature vectors
    distances = euclidean_distances(representative_vector_reshaped, all_movie_vectors)[0]

    # Combine movie ID and distance
    movie_distances = list(zip(all_movie_ids, distances))

    # Sort by distance (ascending)
    movie_distances.sort(key=itemgetter(1))

    print(f"DEBUG: Top 5 closest movies (ID, Distance): {movie_distances[:5]}")

    recommendations = []

    for movie_id, distance in movie_distances:
            # Translate Euclidian distance to a similarity score
            similarity_score = 1 / (1 + distance)

            # Ensure the movie hasn't been watched
            if movie_id not in watched_ids:
                 recommendations.append((movie_id, similarity_score))

                 if len(recommendations) >= k:
                      break
    return recommendations