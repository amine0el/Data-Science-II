# Libraries
import IPython.display as ipd
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn import preprocessing
import os

def read_features():
    df = pd.read_csv('../features_last_song.csv')
    return df

def get_extraction_similarity(dataframe, name, part):
    # Read data
    data = dataframe

    # Extract labels
    labels = data[['genre']]

    # Drop labels from original dataframe
    data = data.drop(columns=['length','genre', 'name', 'filedir'])
    data.head()

    # Scale the data
    data_scaled=preprocessing.scale(data)
   
    similarity = cosine_similarity(data)
    #print("Similarity shape:", similarity.shape)

    # Convert into a dataframe and then set the row index and column names as labels
    sim_df_labels = pd.DataFrame(similarity)
    sim_df_names = sim_df_labels.set_index(labels.index)
    sim_df_names.columns = labels.index
    sim_df_names.head()
     # Find songs most similar to another song
    series = sim_df_names[name+part].sort_values(ascending = False)
    
    
    # Remove cosine similarity == 1 (songs will always have the best match with themselves)
    for i in range(0,10):
        series = series.drop(name + "."+ str(i))
    
   
    # Display the 5 top matches 
    #print("\n*******\nSimilar songs to ", name)
    #print(series.head(5))
    return series.head(5)

# def play_similar_song():
#     #index = 1;
#     #if(index > 5): 
#     #return "Index out of bounds, please stay below 5!"
#     return "Playing: " + similar_song.index[index -1]
#     #song_genre = similar_song.index[index -1]
#     #song_genre = song_genre.split('.')
#     #songname = similar_song.index[0].split('.')
#     #ipd.Audio(f'{general_path}/genres_original/' + song_genre[0] + '/' + song_genre[0] + "." + songname[1] + '.wav')