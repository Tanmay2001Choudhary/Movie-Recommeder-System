import streamlit as st
import pickle as pi
import pandas as pd
import requests

st.set_page_config(
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=7b44d1459bd775f85981053de1f9cfe5'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def fetch_overview(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=7b44d1459bd775f85981053de1f9cfe5'.format(movie_id))
    data = response.json()
    return data['overview']


def fetch_releaseDate(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=7b44d1459bd775f85981053de1f9cfe5'.format(movie_id))
    data = response.json()
    return data['release_date']


def fetch_rating(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=7b44d1459bd775f85981053de1f9cfe5'.format(movie_id))
    data = response.json()
    return data['vote_average']


def fetch_budget(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=7b44d1459bd775f85981053de1f9cfe5'.format(movie_id))
    data = response.json()
    return data['budget']


def fetch_BoxOffice(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=7b44d1459bd775f85981053de1f9cfe5'.format(movie_id))
    data = response.json()
    return data['revenue']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[0:6]

    recommended_movies = []
    posters = []
    overview = []
    release_date = []
    ratings = []
    budget = []
    boxOffice = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        # fetch poster from API
        recommended_movies.append(movies.iloc[i[0]].title)
        posters.append(fetch_poster(movie_id))
        overview.append(fetch_overview(movie_id))
        release_date.append(fetch_releaseDate(movie_id))
        a = fetch_rating(movie_id)
        b = round(a, 1)
        ratings.append(b)
        budget.append(round(fetch_budget(movie_id) / 1000000))
        boxOffice.append(round(fetch_BoxOffice(movie_id) / 1000000, 1))
    return recommended_movies, posters, overview, release_date, ratings, budget, boxOffice


movies_dict = pi.load(open('movie.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pi.load(open('similarity.pkl', 'rb'))
st.title('Movie Recommender System')
Search_Here = pd.DataFrame({'title': 'Search Here'}, index=[0])
movies = pd.concat([Search_Here, movies]).reset_index(drop=True)

selected_movie_name = st.selectbox("Enter a movie Name", movies['title'].values)

if st.button('Recommend'):
    if (selected_movie_name == "Search Here"):
        st.markdown("""<p style=font-size:30px;font-weight:bold;text-align:center> Please Select a Movie First!!!<p>""",
                    unsafe_allow_html=True)
    else:
        names, posters, overview, release_date, ratings, budget, boxOffice = recommend(selected_movie_name)
        for i in range(0, 6):
            col1, col2 = st.columns(2)

            with col1:
                st.image(posters[i], width=300)
                hide_img_fs = '''
                <style>
                button[title="View fullscreen"]{
                    visibility: hidden;}
                </style>
                '''

                st.markdown(hide_img_fs, unsafe_allow_html=True)
            with col2:
                st.markdown(
                    """
                    <style>
                        div[data-testid="column"]:nth-of-type(2)
                        {
                            margin-left:-700px;
                        } 
                    </style>
                    """, unsafe_allow_html=True
                )
                st.markdown(""" <style> @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:wght@500&display=swap'); .font {
                  width:1000px; font-size: 34px;
                              font-weight: bold;
                              border: 2px solid #a09d9d;
                              text-shadow: 0px 3px -30px #a09d9d;
                              border-top: 0px;
                              border-right: 0px;
                              border-left: 0px;
                              font-family: 'EB Garamond', serif;}
                  </style> """, unsafe_allow_html=True)
                st.markdown(f"""
                <p class="font"> {names[i]}</p>""", unsafe_allow_html=True)
                # st.markdown("-")
                st.markdown(f"""<p style=font-size:20px;;text-align:justify> {overview[i]}</p>""",
                            unsafe_allow_html=True)
                st.markdown(f"""<p style=font-size:20px;;text-align:justify> Release Date : {release_date[i]}</p>""",
                            unsafe_allow_html=True)
                st.markdown(f"""<p style=font-size:20px;;text-align:justify > IMDB Rating : {ratings[i]}</p>""",
                            unsafe_allow_html=True)
                st.markdown(f"""<p style=font-size:20px;;text-align:justify> Budget : ${budget[i]} Million</p>""",
                            unsafe_allow_html=True)
                st.markdown(
                    f"""<p style=font-size:20px;;text-align:justify> Box Office : ${boxOffice[i]} Million</p>""",
                    unsafe_allow_html=True)
            i += 1
