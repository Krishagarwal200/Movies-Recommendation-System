import streamlit as st
import pickle
import joblib
import os
import pandas as pd
import gdown

st.set_page_config(page_title="Movie Recommender", layout="centered")

st.title("🎬 Movie Recommendation System")

# ---------------- LOAD FILES SAFELY ---------------- #

@st.cache_resource
def load_data():
    file_path = "similarity.joblib"

    # Download if not present
    if not os.path.exists(file_path):
        with st.spinner("Downloading similarity file..."):
            url = "https://drive.google.com/uc?id=1oZSOJBcmcDpN31UTOZMr9uvkLIt_MoNC"
            gdown.download(url, file_path, quiet=False)

    # Load files
    similarities = joblib.load(file_path)

    with open("movies.pickle", "rb") as f:
        movies = pickle.load(f)

    return similarities, movies


similarities, movies = load_data()

# Stop app if loading failed
if similarities is None or movies is None:
    st.stop()

# ---------------- RECOMMEND FUNCTION ---------------- #

def recommend(movie_name):
    try:
        movie_index = movies[movies['title'] == movie_name].index[0]
    except:
        return ["Movie not found"]

    distances = similarities[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        key=lambda x: x[1],
        reverse=True
    )

    recommended_movies = [
        movies.iloc[i[0]].title for i in movie_list[1:6]
    ]

    return recommended_movies


# ---------------- UI ---------------- #

movie_titles = movies['title'].values
selected_movie = st.selectbox("🎥 Select a movie", movie_titles)

if st.button("Recommend"):
    recommendations = recommend(selected_movie)

    st.subheader("✨ Recommended Movies:")

    for movie in recommendations:
        st.write(f"👉 {movie}")