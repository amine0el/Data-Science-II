# Libraries
import IPython.display as ipd
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn import preprocessing
import os
import librosa
from mgcapp.models import Document
from MGC.settings import BASE_DIR


def read_features():
    documents = Document.objects.last()
    df = extract(documents.document.path, documents.name)
   
    return df

def extract_one_feature(y,sr):
    #________ chroma_stft _______
    chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
    chroma_stft_mean = np.mean(chroma_stft)
    chroma_stft_var = np.var(chroma_stft)
    #______rms _____
    rms =  librosa.feature.rms(y=y)
    rms_mean = np.mean(rms)
    rms_var = np.var(rms)
    #______spectral_centroid _____
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    spectral_centroid_mean = np.mean(spectral_centroid)
    spectral_centroid_var = np.var(spectral_centroid)
    #______spectral_bandwidth______
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    spectral_bandwidth_mean = np.mean(spectral_bandwidth)
    spectral_bandwidth_var = np.var(spectral_bandwidth)
    #_____rolloff_______
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    rolloff_mean = np.mean(rolloff)
    rolloff_var = np.var(rolloff)
    #_____zero_crossing_rate______
    zero_crossing_rate = librosa.feature.zero_crossing_rate(y)
    zero_crossing_rate_mean = np.mean(zero_crossing_rate)
    zero_crossing_rate_var = np.var(zero_crossing_rate)
    #_____harmony_____
    harmony = librosa.effects.harmonic(y)
    harmony_mean = np.mean(harmony)
    harmony_var = np.var(harmony)
    #_____perceptr____
    C = np.abs(librosa.cqt(y, sr=sr, fmin=librosa.note_to_hz('A1')))
    freqs = librosa.cqt_frequencies(C.shape[0], fmin=librosa.note_to_hz('A1'))
    perceptr = librosa.perceptual_weighting(C**2, freqs, ref=np.max)
    perceptr_mean = np.mean(perceptr)
    perceptr_var = np.var(perceptr)
    #_____tempo______
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr)[0]
    #_____mfcc______
    mfcc = librosa.feature.mfcc(y=y, sr=sr)
    mdict = {"chroma_stft_mean" : chroma_stft_mean,
            "chroma_stft_var":chroma_stft_var,
            "rms_mean": rms_mean,
            "rms_var":rms_var,
            "spectral_centroid_mean": spectral_centroid_mean,
            "spectral_centroid_var" : spectral_centroid_var,
            "spectral_bandwidth_mean":spectral_bandwidth_mean,
            "spectral_bandwidth_var": spectral_bandwidth_var, 
            "rolloff_mean" : rolloff_mean,
            "rolloff_var": rolloff_var ,
            "zero_crossing_rate_mean" : zero_crossing_rate_mean,
            "zero_crossing_rate_var":zero_crossing_rate_var,
            "harmony_mean":harmony_mean,
            "harmony_var":harmony_var,
            "perceptr_mean":perceptr_mean,
            "perceptr_var":perceptr_var,
            "tempo":tempo,}
    
    for index, a in enumerate(mfcc, start = 1):
        mdict["mfcc"+str(index)+"_mean"] = np.mean(a)
        mdict["mfcc"+str(index)+"_var"] = np.var(a)

    return mdict

def extract(filedir, name):
    y, sr = librosa.load(filedir)
    mdict_ = extract_one_feature(y,sr)
    mdict = {}
    mdict["filedir"] = filedir
    mdict["name"] = name
    mdict.update(mdict_)
    return pd.DataFrame([mdict])

def get_extraction_similarity():
    # Read data
    data = read_features()
    data = data.set_index('name')
    file = str(BASE_DIR) + '/mgcapp/features_30_sec.csv'
    df_extraction = pd.read_csv(file, index_col='filename')
    # Drop labels from original dataframe
    data = data.drop(columns=['filedir'])
    df_extraction = df_extraction.drop(columns=['length','label'])

    df_combined = pd.concat([data, df_extraction])
    names = df_combined[['tempo']]
    # Scale the data
    data_scaled=preprocessing.scale(df_combined)
   
    similarity = cosine_similarity(data_scaled)
    #print("Similarity shape:", similarity.shape)

    # Convert into a dataframe and then set the row index and column names as labels
    sim_df_labels = pd.DataFrame(similarity)
    sim_df_names = sim_df_labels.set_index(names.index)
    sim_df_names.columns = names.index

     # Find songs most similar to another song
    series = sim_df_names[data.index[0]].sort_values(ascending = False)
    
    
    # Remove cosine similarity == 1 (songs will always have the best match with themselves)
  
    series = series.drop(data.index[0])
    
   
    # Display the 5 top matches 
    #print("\n*******\nSimilar songs to ", name)
    print(series.head(5))
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