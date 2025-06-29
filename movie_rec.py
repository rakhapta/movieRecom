# -*- coding: utf-8 -*-
"""Movie_Rec.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1bzUtOSlVoWYl9irh2i4nKLbwvkPC_WXL

## Import library
"""

!pip install pandas scikit-learn matplotlib seaborn

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style='whitegrid')
plt.rcParams['figure.figsize'] = (12, 8)

"""## Data loading

download latest version of the dataset from kaggle using kagglehub
"""

import kagglehub

path = kagglehub.dataset_download("amirmotefaker/movielens-10m-dataset-latest-version")

print("Path to dataset files:", path)

"""
Load the data from "movies.csv" and "ratings.csv" into dataframes, starting from adding movies_path and ratings_path

"""

movies_path = f"{path}/ml-10M100K/movies.dat"
ratings_path = f"{path}/ml-10M100K/ratings.dat"

"""Read movies.dat, the file is tab-separated and has three columns: movie_id, title, and genres"""

movies = pd.read_csv(movies_path, sep='::', engine='python', header=None, names=['movie_id', 'title', 'genres'])

"""Read ratings.dat, the file is tab-separated and has four columns: user_id, movie_id, rating, and timestamp"""

ratings = pd.read_csv(ratings_path, sep='::', engine='python', header=None, names=['user_id', 'movie_id', 'rating', 'timestamp'])

"""Display the head of movies dataframes to verify"""

print("Movies DataFrame:")
movies.head()

"""Display the head of ratings dataframes to verify"""

print("\nRatings DataFrame:")
ratings.head()

"""## Exploratory Data Analysis"""

print("\n--- Basic Stats for Ratings ---")
display(ratings.describe())

"""Get information about the data types and non-null values"""

print("\nMovies Info:")
movies.info()

print("\nRatings Info:")
ratings.info()

"""Get a count of unique users and movies"""

n_users = ratings['user_id'].nunique()
n_movies = ratings['movie_id'].nunique()
print(f"\nNumber of unique users: {n_users}")
print(f"Number of unique movies: {n_movies}")

genre_set = set()
for genre_string in movies['genres'].dropna():
    genres = genre_string.split('|')
    genre_set.update(genres)

print("Total of unique genre:", len(genre_set))
print("list of unique genre:")
for genre in sorted(genre_set):
    print("-", genre)

"""

Distribution of Ratings"""

plt.figure(figsize=(10, 6))
sns.countplot(x='rating', data=ratings, palette='viridis')
plt.title('Distribution of Movie Ratings', fontsize=16)
plt.xlabel('Rating')
plt.ylabel('Count')
plt.show()

"""This graph shows two clear user behaviors:

1. Ratings are mostly positive: The most frequent scores are 4, 3, and 5 stars, meaning our model learns more from what users like than what they dislike.
2. Users prefer whole numbers: Whole-star ratings (like 4.0) are far more common than half-star ratings (like 4.5).  

This distribution also validates our strategy of defining a "liked" movie as one rated 4 stars or higher, as this is clearly a common way for users to show enjoyment.

Top 10 Most Common Genres
"""

plt.figure(figsize=(12, 7))

genre_counts = movies['genres'].str.split('|').explode().value_counts()

top_10_genres = genre_counts.head(10)

sns.barplot(x=top_10_genres.values, y=top_10_genres.index, palette='mako')
plt.title('Top 10 Most Common Movie Genres', fontsize=16)
plt.xlabel('Number of Movies')
plt.ylabel('Genre')
plt.show()

"""This graph reveals that Drama and Comedy are the most common genres in the dataset by a large margin.

This creates a 'popularity bias,' meaning the model is trained on far more data for these genres than for niche ones like Sci-Fi or Fantasy.

Consequently, the recommendation system will likely favor mainstream films and may struggle to provide diverse or unexpected suggestions for users who prefer less common genres.

## Data Preprocessing
"""

ratings = ratings.drop('timestamp', axis=1)
print("\nRatings DataFrame after dropping timestamp:")
ratings.head()

"""People often drop the timestamp column from a DataFrame like `ratings` when working on recommendation systems or collaborative filtering tasks if the time at which a rating was given is not relevant to the specific analysis or model we are building.

In this context of building a model that predicts a user's rating based on user and movie features, the exact moment the rating was given might not contribute to the core problem of understanding user preferences or movie characteristics. The rating itself (`rating`), the user who gave it (`user_id`), and the movie it was given to (`movie_id`) are usually the key pieces of information.

Dropping the timestamp simplifies the dataset, reduces memory usage, and potentially speeds up processing, as the model doesn't need to consider or process this extra dimension of data if it's not deemed necessary for the prediction task. If the task involved time-series analysis of ratings or understanding the evolution of user preferences over time, then keeping the timestamp would be crucial. But for a basic collaborative filtering approach, it's often discarded.

Sample active users for computational efficiency
We'll take users who have rated at least 500 movies
"""

from sklearn.model_selection import train_test_split

user_counts = ratings['user_id'].value_counts()
active_users = user_counts[user_counts >= 500].index
ratings_sample = ratings[ratings['user_id'].isin(active_users)]

"""Merge the ratings_sample data with movies (join key is 'movie_id')"""

df = pd.merge(ratings_sample, movies, on='movie_id')

"""Check the data after merging"""

print("Data after merging and sampling:")
display(df.head())
print(f"Number of records after sampling: {len(df)}")
print(f"Number of active users sampled: {df['user_id'].nunique()}")

"""Check for missing values"""

print("\nNumber of missing values:")
print(df.isnull().sum())

"""DATA SPLITTING

We split the data into training and test sets.
"""

train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

print(f"\nTraining data size: {len(train_df)}")
print(f"Test data size: {len(test_df)}")

"""## Content Based Filtering

### Modelling

Use 'movie_id' as the index
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

movies_df = movies.copy().drop_duplicates(subset='movie_id').set_index('movie_id')

"""Replace '|' with a space"""

movies_df['genres'] = movies_df['genres'].str.replace('|', ' ', regex=False)

"""Create TF-IDF and Cosine Similarity (logic remains the same)"""

tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies_df['genres'])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

"""Create a Series to map movie titles to their index"""

indices = pd.Series(movies_df.index, index=movies_df['title'])

"""Function to get recommendations (content based)"""

def get_content_based_recommendations(title, N=10):
    try:
        movie_index = indices[title]
        sim_matrix_idx = movies_df.index.get_loc(movie_index)
        sim_scores = list(enumerate(cosine_sim[sim_matrix_idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:N+1]
        movie_indices = [i[0] for i in sim_scores]
        return movies_df['title'].iloc[movie_indices]
    except KeyError:
        return f"The movie '{title}' was not found."

"""### Get Recomendations

Example 1: Action/Superhero Movie
"""

print("--- Recommendations for 'Iron Man (2008)' ---")
print(get_content_based_recommendations('Iron Man (2008)', N=5))

"""Example 2: Romantic Comedy Movie"""

print("\n--- Recommendations for 'Boomerang (1992)' ---")
print(get_content_based_recommendations('Boomerang (1992)', N=5))

"""Example 3: Comedy Movie"""

print("\n--- Recommendations for 'Father of the Bride Part II (1995)' ---")
print(get_content_based_recommendations('Father of the Bride Part II (1995)', N=5))

"""### Strengths and Weaknesses of Content-Based Filtering

This approach, which recommends movies based on genre similarity, has clear advantages and disadvantages.

**Strengths:**
* **User Independence:** The model doesn't need any data about other users. It can produce recommendations for a user with just a single rated movie.
* **Recommends Niche Items:** It can recommend obscure movies that have similar genres to a user's liked movies, even if those movies aren't popular among other users.
* **Explainable:** The recommendations are easy to understand. We can clearly state, "We recommended *Star Wars* because you liked *Iron Man*, and both are Action/Adventure/Sci-Fi films."

**Weaknesses:**
* **Limited Novelty (Overspecialization):** The model will never recommend something outside a user's existing interests. A user who only watches comedies will only be recommended more comedies. It struggles to create "serendipitous" or surprising discoveries.
* **Feature Dependent:** The quality of recommendations is entirely dependent on the quality of the features we use (in this case, only genre). If genres are missing or too broad, the recommendations will be poor. It doesn't capture subtle nuances that users might like.

### Evaluation Metrics for content Based Recomendations

Defines our "measuring sticks." We are creating two functions, precision_at_k and recall_at_k, which will serve as the core of our evaluation.

* precision_at_k: This function calculates how precise our recommendations are. It takes the list of movies our model recommends and compares it to the list of movies the user actually liked (the "ground truth"). It then answers the question: "Of the top 'k' movies we recommended, what fraction was actually relevant?"

* recall_at_k: This function calculates how complete our recommendations are. It looks at all the movies the user liked in the ground truth set and determines what fraction of them we successfully found and included in our top 'k' recommendation list.



The functions are designed to be robust, returning 0.0 if a calculation isn't possible (e.g., if there are no recommendations or no ground truth items).
"""

import numpy as np

def precision_at_k(recommended_items, ground_truth_items, k):
    if k == 0 or not recommended_items:
        return 0.0

    top_k = recommended_items[:k]
    relevant_count = len(set(top_k) & set(ground_truth_items))

    return relevant_count / k

def recall_at_k(recommended_items, ground_truth_items, k):
    if not ground_truth_items:
        return 0.0

    top_k = recommended_items[:k]
    relevant_count = len(set(top_k) & set(ground_truth_items))

    return relevant_count / len(ground_truth_items)

"""Preparing the Data for Evaluation

Before we can loop through users and score our model, we need helper functions to retrieve the necessary data for each user. This cell creates two such functions.

1. get_ground_truth(user_id, test_df, min_rating=4.0): This function gets our "correct answers." For any given user_id, it scans the test set (test_df) and returns a list of movies that the user rated highly (in this case, 4.0 stars or more). This list represents the items we hope our model can successfully recommend.

2. get_recommendations_for_user(user_id, train_df, N=10): This function gets our "predicted answers" from the content-based model. Since our content-based model recommends items similar to a given movie, we simulate a real-world scenario: we find a random movie that the user liked in their training history (train_df) and use it as a "seed" to generate N new recommendations. The function then returns the movie IDs of these recommendations.
"""

def get_ground_truth(user_id, test_df, min_rating=4.0):
    user_data = test_df[(test_df['user_id'] == user_id) & (test_df['rating'] >= min_rating)]
    return user_data['movie_id'].tolist()

def get_recommendations_for_user(user_id, train_df, N=10):
    user_train_data = train_df[train_df['user_id'] == user_id]
    if user_train_data.empty:
        return []

    try:
        seed_movie = user_train_data.sample(1).iloc[0]
        seed_movie_title = seed_movie['title']
    except ValueError:
        return []

    recommended_titles = get_content_based_recommendations(seed_movie_title, N=N)

    if isinstance(recommended_titles, str):
        return []

    recommended_ids = recommended_titles.index.tolist()

    return recommended_ids

"""Running the Evaluation Loop and Calculating Results

This final code block brings everything together. It executes the evaluation process:

First, we define our settings: k=10 for our metrics and a sample of 50 users from the test set to evaluate.

Then, we initiate the main loop. For each user in our sample, the loop will:

1. Call get_ground_truth to get the list of movies the user actually liked.
2. Call get_recommendations_for_user to get the list of movies our model recommended.
3. Check if a ground truth list exists for the user; if not, we skip them since we can't score them.
4. Use the precision_at_k and recall_at_k functions from Part 1 to calculate the scores.
5. Append these scores to our lists, precision_scores and recall_scores.

After the loop completes, we calculate the average of all the scores we collected and print the final, summary result.
"""

k = 10
users_to_evaluate = test_df['user_id'].unique()
sample_users = users_to_evaluate[:50]

precision_scores = []
recall_scores = []

print(f"--- Evaluating Precision and Recall for {len(sample_users)} users (k={k}) ---")

for user_id in sample_users:
    ground_truth = get_ground_truth(user_id, test_df)
    recommendations = get_recommendations_for_user(user_id, train_df, N=k)

    if not ground_truth:
        continue

    precision = precision_at_k(recommendations, ground_truth, k)
    recall = recall_at_k(recommendations, ground_truth, k)

    precision_scores.append(precision)
    recall_scores.append(recall)

if precision_scores and recall_scores:
    avg_precision = np.mean(precision_scores)
    avg_recall = np.mean(recall_scores)

    print(f"\nAverage Precision@{k}: {avg_precision:.4f}")
    print(f"Average Recall@{k}: {avg_recall:.4f}")
else:
    print("Could not calculate metrics. This might happen if none of the sample users had liked items in the test set.")

"""### Analysis of Evaluation Results

* **Average Precision@10: 0.0400**
* **Average Recall@10: 0.0018**

The results for both precision and recall are quite low, which is expected for this simple model.

* **A precision of 0.03** means that, on average, less than one movie (0.3) out of the 10 we recommended was actually a movie the user had rated highly in the test set.
* **A recall of 0.0042** is very low, indicating that our model only found a tiny fraction of all the movies the user would have liked.

**Conclusion:** These metrics demonstrate the limitations of a purely genre-based content model. While it can find similar movies, it is not powerful enough to accurately capture the full range of a user's preferences.

## Collaborative Filtering (with SVD)

Our second approach, Collaborative Filtering, works differently. Instead of looking at movie genres, it looks at the behavior of all users. The core idea is: "If User A and User B have similar rating patterns, then User A will probably like other movies that User B has liked." We will use a powerful matrix factorization technique called **Singular Value Decomposition (SVD)** to uncover these patterns.

### Strengths and Weaknesses of SVDBased Collaborative Filtering

**Strengths:**
* **Finds Surprising Recommendations:** SVD can uncover latent (hidden) features in the data. This means it can recommend a movie that seems unrelated by genre but is often liked by similar users, leading to novel discoveries.
* **No Item Features Needed:** The model works purely on the rating matrix. It doesn't need genres, actors, or any other metadata about the movies.

**Weaknesses:**
* **The "Cold Start" Problem:** This is the biggest weakness. The model cannot make recommendations for new users (who have no ratings) or for new movies (that have never been rated).
* **Popularity Bias:** The model tends to recommend popular items more frequently because they have more ratings, as we saw in our EDA.
* **Computationally Expensive:** SVD on a very large user-item matrix can require significant memory and processing power.

Create User-Movie Matrix from TRAINING DATA (with new columns)
"""

from scipy.sparse.linalg import svds
from sklearn.metrics import mean_squared_error

user_movie_matrix_train = train_df.pivot_table(index='user_id', columns='movie_id', values='rating').fillna(0) # <-- Updated
R_train = user_movie_matrix_train.values

"""SVD process"""

R_mean_train = np.mean(R_train, axis=1).reshape(-1, 1)
R_demeaned_train = R_train - R_mean_train
U, sigma, Vt = svds(R_demeaned_train, k=50)
sigma = np.diag(sigma)

"""Reconstruct the predicted ratings matrix"""

R_predicted = np.dot(np.dot(U, sigma), Vt) + R_mean_train
predicted_ratings = pd.DataFrame(R_predicted, index=user_movie_matrix_train.index, columns=user_movie_matrix_train.columns)

print("Predicted ratings matrix created successfully from training data.")
display(predicted_ratings.head())

"""Get movie_info for mapping movie_id to title"""

movie_info = df[['movie_id', 'title']].drop_duplicates()

"""Recommend movies function using SVD"""

def recommend_movies_svd(user_id, num_recommendations=10):
    if user_id not in predicted_ratings.index:
        return f"User ID {user_id} not found in the model."

    user_row = predicted_ratings.loc[user_id].sort_values(ascending=False)

    rated_movies = df[df['user_id'] == user_id]['movie_id'].tolist()

    recommendations = user_row.drop(rated_movies, errors='ignore').head(num_recommendations)

    recs_df = pd.DataFrame(recommendations).reset_index()
    recs_df.columns = ['movie_id', 'predicted_rating']
    recs_df = pd.merge(recs_df, movie_info, on='movie_id')

    return recs_df

"""Example usage, sample a random user_id from the sampled data"""

USER_ID_TARGET = df['user_id'].sample(1).iloc[0]
print(f"\n--- Top Movie Recommendations for User ID {USER_ID_TARGET} ---")
final_recommendations = recommend_movies_svd(USER_ID_TARGET)
display(final_recommendations)

"""### Quantitative Evaluation of SVD with RMSE

Loop through each row in the test data (with new columns)
"""

actuals = []
predictions = []

for _, row in test_df.iterrows():
    user_id = row['user_id']
    movie_id = row['movie_id']
    actual_rating = row['rating']

    if user_id in predicted_ratings.index and movie_id in predicted_ratings.columns:
        predicted_rating = predicted_ratings.loc[user_id, movie_id]
        actuals.append(actual_rating)
        predictions.append(predicted_rating)

"""Calculate RMSE"""

if len(actuals) > 0:
    rmse = np.sqrt(mean_squared_error(actuals, predictions))
    print(f"\n==============================================")
    print(f"SVD Model Evaluation Results")
    print(f"RMSE on Test Data: {rmse:.4f}")
    print(f"==============================================")
else:
    print("No test data could be evaluated (perhaps users/movies in test set were not in training set).")

"""### Analysis of SVD Evaluation (RMSE)

**RMSE on Test Data: 2.2440**

The Root Mean Squared Error (RMSE) measures the average magnitude of the error between our model's predicted ratings and the users' actual ratings.

An RMSE of **2.24** on a rating scale of 1 to 5 is very high. It indicates that, on average, our model's rating predictions are off by more than 2 stars. For example, if a user rated a movie 4 stars, our model might predict a rating of 1.76 or something similarly far off.

**Conclusion:** While this SVD model can generate a ranked list of interesting recommendations, it is not accurate at predicting the *exact rating* a user would give. This suggests its strength is in identifying movies a user *might like*, rather than forecasting the specific score.
"""