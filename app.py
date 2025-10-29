

import streamlit as st
import pickle
import pandas as pd
import requests  #  Needed for API calls


#  Function to fetch movie poster from OMDb API
def fetch_poster(movie_title):
    api_key = "96875f83"  #  Replace with your activated OMDb API key
    clean_title = movie_title.split('(')[0].strip()  # removes extra brackets or year
    url = f"https://www.omdbapi.com/?t={clean_title}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    
    if data.get('Response') == 'True' and data.get('Poster') != "N/A":
        return data['Poster']
    else:
        return "https://via.placeholder.com/300x450.png?text=No+Poster+Found"


#  Recommendation function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(
        list(enumerate(distances)), key=lambda x: x[1], reverse=True
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_title = movies.iloc[i[0]].title
        poster_url = fetch_poster(movie_title)
        recommended_movies.append(movie_title)
        recommended_posters.append(poster_url)

    return recommended_movies, recommended_posters


#  Load data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))


#  Streamlit UI
st.title(" Movie Recommender System")

# Dropdown
selected_movie_name = st.selectbox(
    'Select a movie to get recommendations:',
    movies['title'].values
)

# Recommend button
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    st.write("### Recommended Movies:")
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.image(posters[idx], use_container_width=True)
            st.caption(names[idx])
