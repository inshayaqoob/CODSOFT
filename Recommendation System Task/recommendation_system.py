import pandas as pd
from sklearn.neighbors import NearestNeighbors
import streamlit as st

# Load and preprocess the data
ratings = pd.read_csv('user.data', sep='\t', names=['userId', 'movieId', 'rating', 'timestamp'])
movies = pd.read_csv('user1.item', sep='|', encoding='latin1', header=None, names=['movieId', 'title'], usecols=[0, 1])
df = pd.merge(ratings, movies, on='movieId')
user_item_matrix = df.pivot_table(index='userId', columns='title', values='rating').fillna(0)

# Build the recommendation model
model = NearestNeighbors(n_neighbors=10, metric='cosine', algorithm='brute', n_jobs=-1)
model.fit(user_item_matrix)

# Create a Streamlit web app
st.title("Movie Recommendation System")

# User input for user selection
user_list = user_item_matrix.index.tolist()
selected_user = st.selectbox("Select a User", user_list)

# Number of recommendations
num_recommendations = st.slider("Number of Recommendations", min_value=1, max_value=10, value=5)

# Button to trigger recommendations
if st.button("Get Recommendations"):
    # Make recommendations for the user
    user_id = int(selected_user)
    user_ratings = user_item_matrix.loc[user_id]
    user_ratings = user_ratings.values.reshape(1, -1)

    distances, indices = model.kneighbors(user_ratings, n_neighbors=num_recommendations + 1)

    recommended_movie_indices = indices.flatten()[1:]
    recommended_movies = list(user_item_matrix.columns[recommended_movie_indices])

    st.header(f"Recommended movies for user {user_id}:")
    for i, movie in enumerate(recommended_movies):
        st.write(f"{i + 1}. {movie}")
