
import streamlit as st
import pickle
import pandas as pd
import requests

# Google Drive direct download links
MOVIES_URL = "https://drive.google.com/uc?export=download&id=1763CSrdwySbVIUn0QnG_FEdOtTq8qZ1V"
SIMILARITY_URL = "https://drive.google.com/uc?export=download&id=1AZCwZedDeSRWc0y6rBd1EehnQCtw3HBf"

# Load the pickle files from Google Drive
@st.cache_data
def load_data():
    try:
        movies_df = pickle.loads(requests.get(MOVIES_URL).content)
        similarity = pickle.loads(requests.get(SIMILARITY_URL).content)
        return movies_df, similarity
    except Exception as e:
        st.error(f"❌ Failed to load data from Google Drive: {e}")
        return None, None

movies, similarity = load_data()

# Movie poster function
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=ee7b89b0cf7b7b8b3cb2e3ef869379c7&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return "https://via.placeholder.com/500x750?text=No+Image"

# Recommendation function
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies, posters = [], []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        posters.append(fetch_poster(movie_id))
    return recommended_movies, posters

# Streamlit UI
st.title("🎬 Movie Recommender System")

if movies is not None:
    selected_movie = st.selectbox("Select a movie to get recommendations:", movies['title'].values)

    if st.button("Recommend"):
        names, posters = recommend(selected_movie)
        cols = st.columns(5)
        for i, col in enumerate(cols):
            with col:
                st.text(names[i])
                st.image(posters[i])
else:
    st.warning("⚠️ Data failed to load. Please check your Google Drive file permissions or links.")
