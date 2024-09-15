import streamlit as st
import pickle
import pandas as pd
import requests

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pd     .DataFrame(movies_dict)

def fetch_poster(id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=34b24e372c050b70e0d4d94c21694e1a&language=en-US'.format(id))
    data = response.json()

    return 'http://image.tmdb.org/t/p/w500/' + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse = True,key =lambda x:x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies_posters.append(fetch_poster(movie_id))
        recommended_movies.append(movies.iloc[i[0]].title)

    return recommended_movies, recommended_movies_posters

st.title('Movie Recommender System')

selected_movie = st.selectbox(
    "Select a movie",
    movies['title'].values,
)

if st.button("Recommend"):
    names, posters = recommend(selected_movie)

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.image(posters[i], use_column_width=True)  # Automatically adjust image size
            st.markdown(f"**{names[i]}**")  # Use bold text for movie names

