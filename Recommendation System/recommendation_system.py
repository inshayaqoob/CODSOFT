import pandas as pd
from sklearn.neighbors import NearestNeighbors
import streamlit as st

# Step 1: Load and preprocess the data
ratings = pd.read_csv('u.data', sep='\t', names=['userId', 'movieId', 'rating', 'timestamp'])
movies = pd.read_csv('u.item', sep='|', encoding='latin1', header=None, names=['movieId', 'title'], usecols=[0, 1])
df = pd.merge(ratings, movies, on='movieId')
user_item_matrix = df.pivot_table(index='userId', columns='title', values='rating').fillna(0)

# Step 2: Build the recommendation model
model = NearestNeighbors(n_neighbors=10, metric='cosine', algorithm='brute', n_jobs=-1)
model.fit(user_item_matrix)

# Create a Streamlit web app
st.title("Movie Recommendation System")

# User input for user ID
user_id = st.number_input("Enter User ID", min_value=1, max_value=user_item_matrix.index.max(), value=1, step=1)

# Button to trigger recommendations
if st.button("Get Recommendations"):
    # Step 3: Make recommendations for the user
    def get_recommendations(user_id, num_recommendations=5):
        user_ratings = user_item_matrix.loc[user_id]
        user_ratings = user_ratings.values.reshape(1, -1)

        distances, indices = model.kneighbors(user_ratings, n_neighbors=num_recommendations + 1)

        recommended_movie_indices = indices.flatten()[1:]
        recommended_movies = list(user_item_matrix.columns[recommended_movie_indices])

        return recommended_movies

    # Get recommendations
    recommendations = get_recommendations(user_id, num_recommendations=5)
    st.header(f"Recommended movies for user {user_id}:")
    for i, movie in enumerate(recommendations):
        st.write(f"{i + 1}. {movie}")
