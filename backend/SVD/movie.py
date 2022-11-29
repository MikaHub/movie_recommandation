#!/usr/bin/env python
# coding: utf-8

# In[37]:


import numpy as np 
import pandas as pd
from scipy.sparse.linalg import svds



# In[7]:


ratings = pd.read_csv('/Users/micaeldossantos/WorkSpace/IA/movie_recommandation_system/data/ratings_small.csv')
ratings.head()


# In[8]:


user_item = ratings.groupby(['userId', 'movieId'])['rating'].first().unstack(fill_value=0.0)
# first(offset) Select initial periods of time series data based on a date offset.
#unstack([level, fill_value]) Pivot a level of the (necessarily hierarchical) index labels.

# In[9]:


user_item.shape


# In[35]:


user_item.describe


# In[10]:


user_item.loc[42].sort_values(ascending=False).head()


# In[40]:


U, sigma, Vt = svds(user_item.to_numpy(), k=50)


# In[41]:


U.shape


# In[42]:


Vt.shape


# In[43]:


sigma_diag_matrix=np.diag(sigma)


# In[44]:


all_user_predicted_ratings = np.dot(np.dot(U, sigma_diag_matrix), Vt)
preds_df = pd.DataFrame(all_user_predicted_ratings, columns = user_item.columns, index=user_item.index)


# In[45]:


preds_df.shape


# In[46]:


preds_df.head()


# In[47]:


user_item.loc[42].sort_values(ascending=False).head(10)


# In[48]:


movies_user_42 = user_item.loc[42]


# In[49]:


high_rated_movies_42 = movies_user_42[movies_user_42 > 3].index


# In[50]:


high_rated_movies_42


# In[51]:


movies_recommended_for_42 = preds_df.loc[42]


# In[52]:


movies_high_recommend_for_42 = movies_recommended_for_42[movies_recommended_for_42 > 3].index


# In[53]:


movies_high_recommend_for_42


# In[54]:


set(movies_high_recommend_for_42) - set(high_rated_movies_42)


# In[55]:


def get_high_recommended_movies(userId):
    movies_rated_by_user = user_item.loc[userId]
    movies_high_rated_by_user =  movies_rated_by_user[movies_rated_by_user > 3].index
    movies_recommended_for_user = preds_df.loc[userId]
    movies_high_recommend_for_user = movies_recommended_for_user[movies_recommended_for_user > 3].index
    res = dict()
    res["movieId"] = set(movies_high_recommend_for_user) - set(movies_high_rated_by_user)
    res["rating"] = preds_df.loc[userId, set(movies_high_recommend_for_user) - set(movies_high_rated_by_user)]
    return res


# In[56]:


get_high_recommended_movies(42)


# In[57]:


get_high_recommended_movies(314)


# In[58]:


get_high_recommended_movies(217)


# In[59]:


preds_df.loc[217, 1198]

