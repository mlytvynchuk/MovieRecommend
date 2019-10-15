import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import time 

begin = time.time()
df = pd.read_csv("/Users/max22111/mydev/MovieRecommend/research/movie_data.csv")
features = ['keywords', 'cast', 'genres', 'director']

def combine_features(row):
    return row['keywords']+' '+row['cast']+" "+row['genres']+' '+row['director']


for feature in features:
    df[feature] = df[feature].fillna('') # replace none by emty string
df["combined_features"] = df.apply(combine_features,axis=1)


def get_title_from_index(index):
    try:
        return df[df.index == index]['title'].values[0]
    except:
        return "Movie is not found"


def get_index_from_title(title):
    try:
        return df[df.title == title]['index'].values[0] 
    except:
        print(title,"is not found in data base")
        return None


cv = CountVectorizer()
count_matrix = cv.fit_transform(df['combined_features'])
cosine_sim = cosine_similarity(count_matrix)

def find_simulars(movie_user_likes):
    titles = []
    movie_index = get_index_from_title(movie_user_likes)
    if movie_index:
        similar_movies =  list(enumerate(cosine_sim[movie_index]))
        sorted_similar_movies = sorted(similar_movies,key=lambda x:x[1],reverse=True)[1:]

        i=0
        print("Top 5 similar movies to "+movie_user_likes+" are:\n")
        for element in sorted_similar_movies:
            print(get_title_from_index(element[0]))
            titles.append(get_title_from_index(element[0]))
            i=i+1
            if i>=5:
                break
    return titles

find_simulars("Cars 2")
endtime = time.time() - begin
print(endtime)