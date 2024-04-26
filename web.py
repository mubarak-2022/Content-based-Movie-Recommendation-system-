import streamlit as st
import pickle
import pandas as pd
import requests
similarity = pickle.load(open('similartiy.pkl', 'rb'))

def fetch_poster(movie_id):
    api_key = "b2b175f546a0d4b3503677836dfc78e8"
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
    headers = {
        "accept": "application/json"
    }
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        if 'poster_path' in data:
            return 'https://image.tmdb.org/t/p/w500/' + data['poster_path']
        else:
            return "No poster found for this movie."
    else:
        return "Error fetching poster. Status code: {}".format(response.status_code)

def recommend(movie):
    movie_index = movies['title'][movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_lists = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_id = []
    for i in movies_lists:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_id.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_id

st.title('Movie Recommender System')

movies_list = pickle.load(open('movies_dict.pkl', 'rb'))


movies = pd.DataFrame(movies_list)

selected_movie = st.selectbox(
    'Please select a movie from the below list which you have watched recently-',
    movies['title'].values)

if st.button('Recommend Movies To Me'):
    recommendation, posters = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(recommendation[0])
        st.image(posters[0])

    with col2:
        st.text(recommendation[1])
        st.image(posters[1])
    with col3:
        st.text(recommendation[2])
        st.image(posters[2])

    with col4:
        st.text(recommendation[3])
        st.image(posters[3])

    with col5:
        st.text(recommendation[4])
        st.image(posters[4])

    st.text('You can watch these movies similar to that one')
