import streamlit as st
import pickle
import pandas as pd
import requests

# --- Function to load pickle files directly from Google Drive ---
def load_pickle_from_drive(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises error if download fails
        return pickle.loads(response.content)
    except Exception as e:
        st.error(f"❌ Failed to load data from: {url}\nError: {e}")
        return None

# --- Google Drive Direct Download Links ---
movie_dict_url = "https://drive.google.com/uc?export=download&id=1763CSrdwySbVIUn0QnG_FEdOtTq8qZ1V"
similarity_url = "https://drive.google.com/uc?export=download&id=1AZCwZedDeSRWc0y6rBdlEeHnQCtw3HBf"

# --- Load Data ---
st.write("⏳ Loading data, please wait...")

movies_dict = load_pickle_from_drive(movie_dict_url)
similarity = load_pickle_from_drive(similarity_url)

if movies_dict is not None and similarity is not None:
    movies = pd.DataFrame(movies_dict)

    # --- Debug Info ---
    st.success("✅ Data Loaded Successfully!")
    st.write("Movies loaded:", len(movies))
    st.write("Similarity matrix shape:", similarity.shape)
else:
    st.error("⚠️ Data failed to load. Please check your Google Drive file links or make them public.")
    st.stop()

# --- Movie Recommendation Function ---
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:6]
    recommended_movies = [movies.iloc[i[0]]['title'] for i in movie_list]
    return recommended_movies

# --- Streamlit UI ---
st.title("🎬 Movie Recommender System")
st.write("Get top 5 similar movies instantly!")

selected_movie = st.selectbox(
    "Select or search for a movie:",
    movies['title'].values
)

if st.button("🔍 Recommend"):
    try:
        recommendations = recommend(selected_movie)
        st.subheader("🎥 Top 5 Recommended Movies:")
        for i, title in enumerate(recommendations, start=1):
            st.write(f"{i}. {title}")
    except Exception as e:
        st.error(f"❌ An error occurred while generating recommendations: {e}")
