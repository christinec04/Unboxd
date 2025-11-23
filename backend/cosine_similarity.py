import numpy as np
from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine_similarity

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
    movie1_vector = np.concatenate(movie1)
    movie2_vector = np.concatenate(movie2)
    
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