
import streamlit as st
import pickle
import pandas as pd
import requests

# --- Function to load pickle files from Google Drive ---
def load_pickle_from_drive(url):
    response = requests.get(url)
    return pickle.loads(response.content)

# --- Google Drive Direct Download Links ---
movie_dict_url = "https://drive.google.com/uc?id=1763CSrdwySbVIUn0QnG_FEdOtTq8qZ1V"
similarity_url = "https://drive.google.com/uc?id=1AZCwZedDeSRWc0y6rBdlEeHnQCtw3HBf"

# --- Load Data ---
movies_dict = load_pickle_from_drive(movie_dict_url)
similarity = load_pickle_from_drive(similarity_url)
movies = pd.DataFrame(movies_dict)

# --- Function to fetch movie poster from OMDb API ---
def fetch_poster(movie_title):
    api_key = "96875f83"  # replace with your OMDb API key
    clean_title = movie_title.split('(')[0].strip()
    url = f"https://www.omdbapi.com/?t={clean_title}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    if data.get('Response') == 'True' and data.get('Poster') != "N/A":
        return data['Poster']
    else:
        return "https://via.placeholder.com/300x450.png?text=No+Poster+Found"

# --- Recommendation Logic ---
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []
    for i in movie_list:
        movie_title = movies.iloc[i[0]].title
        poster_url = fetch_poster(movie_title)
        recommended_movies.append(movie_title)
        recommended_posters.append(poster_url)
    return recommended_movies, recommended_posters

# --- Streamlit UI ---
st.title("🎬 Movie Recommender System")

selected_movie = st.selectbox(
    "Select or search for a movie:",
    movies['title'].values
)

if st.button("Recommend"):
    names, posters = recommend(selected_movie)
    st.subheader("✨ Top 5 Recommended Movies:")
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.image(posters[idx], use_container_width=True)
            st.caption(names[idx])
