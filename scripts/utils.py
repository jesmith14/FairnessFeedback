import numpy as np
import pandas as pd

ratings_df = pd.DataFrame.empty

def load_ratings(rating_path) :
    global ratings_df
    ratings_df = pd.read_csv(rating_path, names=['userId','movieId','rating'])

def softmax(vector):
    normalized_vector = np.array(vector) - np.max(vector)  # For numerical stability
    return np.exp(normalized_vector) / np.sum(np.exp(normalized_vector))

def get_average_previous(item):
    item_ratings = ratings_df[ratings_df['movieId']==item]
    mean_rating = item_ratings['rating'].mean()
    # draw from a normal dist centered around the mean, then round to nearest 0.5
    return round(np.random.normal(mean_rating, 0.5) * 2) / 2

def rate_item(user, recommendations, selection_type):
    ratings = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]

    items = [item for item, score in recommendations]
    logits = [score for item, score in recommendations]

    _scores = softmax(logits)
    distribution = _scores/np.sum(_scores)

    if selection_type == "best":
        # choose the first item (highest scored) in the recommendation list
        selection = items[0]

    elif selection_type == "random":
        # randomly choose one item from recommendation
        selection = np.random.choice(items)

    else:
        # use softmax distribution to explore items
        selection = np.random.choice(items, p=distribution)

    rating = get_average_previous(selection) #np.random.choice(ratings, p=distribution)


    return selection, rating
