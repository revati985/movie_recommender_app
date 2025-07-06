import streamlit as st
import pickle
import pandas as pd
import requests

import os
import gdown

# File info
SIM_FILE = "similarity.pkl"
FILE_ID = "1GlEMrEKcwZG5fl4K6vpEPEHsDRIA-xyn"  # your Google Drive file ID

# Download only if file doesn't exist (on Streamlit Cloud)
if not os.path.exists(SIM_FILE):
    print("Downloading similarity.pkl from Google Drive...")
    gdown.download(f"https://drive.google.com/uc?id={FILE_ID}", SIM_FILE, quiet=False)

# Now load it (local or downloaded)
with open(SIM_FILE, 'rb') as f:
    similarity = pickle.load(f)



def fetch_poster(movie_id):
    response= requests.get('https://api.themoviedb.org/3/movie/{}?api_key=4c4570bd3ff777178a892a644df09e78'.format(movie_id))
    data= response.json()
    return 'https://image.tmdb.org/t/p/w500/'+ data['poster_path']

def recommend(movie):
    movie_i= movies[movies['title']==movie].index[0]
    dist= similarity[movie_i]
    movie_list= sorted(list(enumerate(dist)),reverse=True,key=lambda x:x[1])[1:6]

    recom_L=[]
    recom_ps=[]
    # movies.iloc[i[0]]: gives if of movie, where i[0] gives index of pos in list

    for i in movie_list:
        movie_id= movies.iloc[i[0]].movie_id

        recom_L.append(movies.iloc[i[0]].title)
        # fetch poster from API  (tmdb)
        recom_ps.append(fetch_poster(movie_id))
    return recom_L,recom_ps


st.title('Movie Recommender System')
movies_dict= pickle.load(open('movies_dict.pkl','rb'))
movies= pd.DataFrame(movies_dict)



selected_movie_name = st.selectbox(
    "How would you like to be contacted?",
    movies['title'].values)

if st.button("Recommend"):
    names,posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])
