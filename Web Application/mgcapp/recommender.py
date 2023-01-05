# Libraries
import IPython.display as ipd
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn import preprocessing
import os
general_path = './Data'

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