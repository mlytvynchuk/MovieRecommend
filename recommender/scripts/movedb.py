# from movies.models import Movie
import pandas as pd

def move_to_db(filename):
    df = pd.read_csv(filename, skiprows=1, names=['id','title','original','genres','keywords','timestamp','country','rating','director','image','actors','description'])
    print(df.head)
    
    for index, row in df.iterrows():
        
        title = row['title']
        original = row['original']
        genres = str(row['genres']).replace('|', ',')
        keywords = str(row['keywords']).replace('|', ',')
        country = str(row['country'])
        timestamp = row['timestamp']
        rating=row['rating']
        director=row['director']
        image=row['image']
        actors=str(row['actors']).replace('|', ',')
        description=row['description']
        print(actors)
        if index > 10:
            break

move_to_db('movies_data.csv')
