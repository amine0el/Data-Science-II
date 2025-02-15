
# GenRec - The Smash Group
    # Music Genre Recommender and Classifier
    # Project during Data Science 2
    # WiSe 2022/2023
    # TU Darmstadt

# File recommender.py
    # Description: 
        # Main Page of the Recommender Logic behind GenRec. 
        # The recommender is based on the cosine similarity. During the prediction side the full song is extracted and a button to the recommender page is displayed.
        # This file imports the features from the FMA Database and combines it with the new song.
        # After running the cosine similarity the 5 similiar/non-similar songs are returned to the user.

# Import Libraries
import IPython.display as ipd
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn import preprocessing
import os
import librosa
from mgcapp.models import Document
from MGC.settings import BASE_DIR
from mutagen.easyid3 import EasyID3

# Function used to extract the features of a saved full song in the background
    # returns: dataframe with features
def read_features(name):
    documents = Document.objects.filter(name__icontains=name)
    documents = documents[0]
    if(".mp3" in documents.name):
        audio = EasyID3(documents.document.path)
        audio.delete()
        audio.save()
   
    length = librosa.get_duration(filename=documents.document.path)
    df = extract(documents.document.path, documents.name, length)
    return df

# Function extract all features of one Song
def extract_one_feature(y, sr):
    # ________ chroma_stft _______
    chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
    chroma_stft_mean = np.mean(chroma_stft)
    chroma_stft_var = np.var(chroma_stft)
    # ______rms _____
    rms = librosa.feature.rms(y=y)
    rms_mean = np.mean(rms)
    rms_var = np.var(rms)
    # ______spectral_centroid _____
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    spectral_centroid_mean = np.mean(spectral_centroid)
    spectral_centroid_var = np.var(spectral_centroid)
    # ______spectral_bandwidth______
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    spectral_bandwidth_mean = np.mean(spectral_bandwidth)
    spectral_bandwidth_var = np.var(spectral_bandwidth)
    # _____rolloff_______
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    rolloff_mean = np.mean(rolloff)
    rolloff_var = np.var(rolloff)
    # _____zero_crossing_rate______
    zero_crossing_rate = librosa.feature.zero_crossing_rate(y)
    zero_crossing_rate_mean = np.mean(zero_crossing_rate)
    zero_crossing_rate_var = np.var(zero_crossing_rate)
    # _____harmony_____
    harmony = librosa.effects.harmonic(y)
    harmony_mean = np.mean(harmony)
    harmony_var = np.var(harmony)
    # _____perceptr____
    C = np.abs(librosa.cqt(y, sr=sr, fmin=librosa.note_to_hz('A1')))
    freqs = librosa.cqt_frequencies(C.shape[0], fmin=librosa.note_to_hz('A1'))
    perceptr = librosa.perceptual_weighting(C**2, freqs, ref=np.max)
    perceptr_mean = np.mean(perceptr)
    perceptr_var = np.var(perceptr)
    # _____tempo______
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr)[0]
    # _____mfcc______
    mfcc = librosa.feature.mfcc(y=y, sr=sr)
    mdict = {"chroma_stft_mean": chroma_stft_mean,
             "chroma_stft_var": chroma_stft_var,
             "rms_mean": rms_mean,
             "rms_var": rms_var,
             "spectral_centroid_mean": spectral_centroid_mean,
             "spectral_centroid_var": spectral_centroid_var,
             "spectral_bandwidth_mean": spectral_bandwidth_mean,
             "spectral_bandwidth_var": spectral_bandwidth_var,
             "rolloff_mean": rolloff_mean,
             "rolloff_var": rolloff_var,
             "zero_crossing_rate_mean": zero_crossing_rate_mean,
             "zero_crossing_rate_var": zero_crossing_rate_var,
             "harmony_mean": harmony_mean,
             "harmony_var": harmony_var,
             "perceptr_mean": perceptr_mean,
             "perceptr_var": perceptr_var,
             "tempo": tempo, }

    for index, a in enumerate(mfcc, start=1):
        mdict["mfcc"+str(index)+"_mean"] = np.mean(a)
        mdict["mfcc"+str(index)+"_var"] = np.var(a)

    return mdict

# Function uses the extract_one_feature-Function and adds name column to it
    # returns dataframe with features
def extract(filedir, name, length):
    y, sr = librosa.load(filedir, duration=length-1)
    mdict_ = extract_one_feature(y, sr)
    mdict = {}
    mdict["filedir"] = filedir
    mdict["name"] = name
    mdict.update(mdict_)
    return pd.DataFrame([mdict])

# Main Function of the recommender:
    # Description: Reads in the FMA database features and combines it with the extracted features. 
    # The cosine simlarity matrix is filtered and sorted
    # returns the five top entries in the list
def get_extraction_similarity(type,name):
    
    # Read data from FMA database and last full song
    path = str(BASE_DIR) + '/mgcapp/'
    if type == "best":
        data = read_features(name)
        data.to_csv(path + "features_last_full_song.csv")
        data = data.set_index('name')
        data = data.drop(columns=['filedir'])
    else:
        data = pd.read_csv(path + "features_last_full_song.csv", index_col='name')
        data = data.drop(columns=['filedir', 'Unnamed: 0'])
    
    df_extraction = pd.read_csv(path +'extraction_fma_full.csv', index_col=['name', 'filename'])

    # Drop labels from original dataframe
    df_extraction = df_extraction.drop(
        columns=['Unnamed: 0', 'filedir', 'genre', 'length'])

    df_combined = pd.concat([data, df_extraction])
    names = df_combined[['tempo']]
    # Scale the data
    data_scaled = preprocessing.scale(df_combined)

    similarity = cosine_similarity(data_scaled)

    # Convert into a dataframe and then set the row index and column names as labels
    sim_df_labels = pd.DataFrame(similarity)
    sim_df_names = sim_df_labels.set_index(names.index)
    sim_df_names.columns = names.index

    # Find songs most similar to another song
    if type == "best":
        series = sim_df_names[data.index[0]].sort_values(ascending=False)
        series = series.drop(data.index[0])
    else:
        series = sim_df_names[data.index[0]].sort_values(ascending=True)

    # Display the 5 top matches
    return series.head(5)


