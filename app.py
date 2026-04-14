import streamlit as st
import pickle
import joblib
import os
import pandas as pd

st.set_page_config(page_title="Movie Recommender", layout="centered")

st.title("🎬 Movie Recommendation System")

# ---------------- LOAD FILES SAFELY ---------------- #

@st.cache_resource
def load_data():
    try:
        # Load similarity
        if not os.path.exists("similarity.joblib"):
            st.error("❌ similarity.joblib not found. Please generate it locally.")
            return None, None

        similarities = joblib.load("similarity.joblib")

        # Load movies
        if not os.path.exists("movies.pickle"):
            st.error("❌ movies.pickle not found.")
            return None, None

        with open("movies.pickle", "rb") as f:
            movies = pickle.load(f)

        return similarities, movies

    except Exception as e:
        st.error(f"❌ Error loading files: {e}")
        return None, None


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