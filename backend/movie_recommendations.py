#!/usr/bin/env python
# coding: utf-8

# In[36]:


import pandas as pd

movies = pd.read_csv("../data/movies.csv")

# In[37]:


movies.head()

# In[3]:


import re


def clean_title(title):
    title = re.sub("[^a-zA-Z0-9 ]", "", title)
    return title


# In[4]:


movies["clean_title"] = movies["title"].apply(clean_title)

# In[5]:


movies

# In[6]:


# lib qui sert à calculer les mots en nombre en fonction de la recherche
from sklearn.feature_extraction.text import TfidfVectorizer

# lors de la recherche on va mettre les mots groupés par 2
vectorizer = TfidfVectorizer(ngram_range=(1, 2))

tfidf = vectorizer.fit_transform(movies["clean_title"])

# In[7]:


from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def search(title):
    title = clean_title(title)
    query_vec = vectorizer.transform([title])
    # donne la similitude du mot passé, 0.0, 0.439...
    similarity = cosine_similarity(query_vec, tfidf).flatten()
    indices = np.argpartition(similarity, -5)[-5:]
    results = movies.iloc[indices].iloc[::-1]

    return results


# In[8]:


# pip install ipywidgets
# jupyter labextension install @jupyter-widgets/jupyterlab-manager


# In[9]:


# import ipywidgets as widgets
# from IPython.display import display
#
# movie_input = widgets.Text(
#     value='Toy Story',
#     description='Movie Title:',
#     disabled=False
# )
# movie_list = widgets.Output()
#
# def on_type(data):
#     with movie_list:
#         movie_list.clear_output()
#         title = data["new"]
#         if len(title) > 5:
#             display(search(title))
#
# movie_input.observe(on_type, names='value')
#
#
# display(movie_input, movie_list)


# In[12]:


movie_id = 89745

# def find_similar_movies(movie_id):
movie = movies[movies["movieId"] == movie_id]

# In[38]:


ratings = pd.read_csv("../data/ratings.csv")

# In[39]:


ratings.dtypes

# In[15]:


# quelqu'un qui à regardé le film & qui l'aime à 5/5
similar_users = ratings[(ratings["movieId"] == movie_id) & (ratings["rating"] > 4)]["userId"].unique()

# In[16]:


# get les films des autres utilisateurs qui on été aimé comme nous / recommandation d'utilisateur similaire
similar_user_recs = ratings[(ratings["userId"].isin(similar_users)) & (ratings["rating"] > 4)]["movieId"]

# In[17]:


# trier pour avoir moins de résulats
# rechercher les films que 10% des utilisateurs qui nous ressemble on également aimés
similar_user_recs = similar_user_recs.value_counts() / len(similar_users)

similar_user_recs = similar_user_recs[similar_user_recs > .10]

# In[18]:


all_users = ratings[(ratings["movieId"].isin(similar_user_recs.index)) & (ratings["rating"] > 4)]

# In[19]:


all_user_recs = all_users["movieId"].value_counts() / len(all_users["userId"].unique())

# In[20]:


rec_percentages = pd.concat([similar_user_recs, all_user_recs], axis=1)
rec_percentages.columns = ["similar", "all"]

# In[21]:


rec_percentages

# In[22]:


rec_percentages["score"] = rec_percentages["similar"] / rec_percentages["all"]

# In[23]:


rec_percentages = rec_percentages.sort_values("score", ascending=False)

# In[24]:


rec_percentages.head(10).merge(movies, left_index=True, right_on="movieId")


# In[25]:


def find_similar_movies(movie_id):
    similar_users = ratings[(ratings["movieId"] == movie_id) & (ratings["rating"] > 4)]["userId"].unique()
    similar_user_recs = ratings[(ratings["userId"].isin(similar_users)) & (ratings["rating"] > 4)]["movieId"]
    similar_user_recs = similar_user_recs.value_counts() / len(similar_users)

    similar_user_recs = similar_user_recs[similar_user_recs > .10]
    all_users = ratings[(ratings["movieId"].isin(similar_user_recs.index)) & (ratings["rating"] > 4)]
    all_user_recs = all_users["movieId"].value_counts() / len(all_users["userId"].unique())
    rec_percentages = pd.concat([similar_user_recs, all_user_recs], axis=1)
    rec_percentages.columns = ["similar", "all"]

    rec_percentages["score"] = rec_percentages["similar"] / rec_percentages["all"]
    rec_percentages = rec_percentages.sort_values("score", ascending=False)
    return rec_percentages.head(10).merge(movies, left_index=True, right_on="movieId")[["score", "title", "genres"]]

# In[26]:


# import ipywidgets as widgets
# from IPython.display import display
#
# movie_name_input = widgets.Text(
#     value='Toy Story',
#     description='Movie Title:',
#     disabled=False
# )
# recommendation_list = widgets.Output()
#
# def on_type(data):
#     with recommendation_list:
#         recommendation_list.clear_output()
#         title = data["new"]
#         if len(title) > 5:
#             results = search(title)
#             movie_id = results.iloc[0]["movieId"]
#             display(find_similar_movies(movie_id))
#
# movie_name_input.observe(on_type, names='value')
#
# display(movie_name_input, recommendation_list)
#
