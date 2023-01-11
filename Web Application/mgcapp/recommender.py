# Libraries
import IPython.display as ipd
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn import preprocessing
import os
general_path = '../Data'

def get_extraction_data():
    # Read data
    data = pd.read_csv(f'{general_path}/extraction.csv', index_col='name_v')

    # Extract labels
    labels = data[['genre']]

    # Drop labels from original dataframe
    data = data.drop(columns=['length','genre', 'name', 'filedir'])
    data.head()

    # Scale the data
    data_scaled=preprocessing.scale(data)
    return data_scaled


def cosine_similarity():
    # Cosine similarity
    similarity = cosine_similarity(data_scaled)
    #print("Similarity shape:", similarity.shape)

    # Convert into a dataframe and then set the row index and column names as labels
    sim_df_labels = pd.DataFrame(similarity)
    sim_df_names = sim_df_labels.set_index(labels.index)
    sim_df_names.columns = labels.index
    sim_df_names.head()
    return similarity

def find_similar_songs(name,part):
    # Find songs most similar to another song
    series = sim_df_names[name+part].sort_values(ascending = False)
    
    
    # Remove cosine similarity == 1 (songs will always have the best match with themselves)
    for i in range(0,10):
        series = series.drop(name + "."+ str(i))
    
   
    # Display the 5 top matches 
    #print("\n*******\nSimilar songs to ", name)
    #print(series.head(5))
    return series.head(5)

def play_similar_song():
    #index = 1;
    #if(index > 5): 
    #return "Index out of bounds, please stay below 5!"
    return "Playing: " + similar_song.index[index -1]
    #song_genre = similar_song.index[index -1]
    #song_genre = song_genre.split('.')
    #songname = similar_song.index[0].split('.')
    #ipd.Audio(f'{general_path}/genres_original/' + song_genre[0] + '/' + song_genre[0] + "." + songname[1] + '.wav')