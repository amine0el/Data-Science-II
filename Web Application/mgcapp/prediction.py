# Import Libraries:
import xgboost
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import dates as mdates
from matplotlib import pyplot as plt

import pandas as pd
import numpy as np
import librosa
import warnings
warnings.filterwarnings('ignore')
<<<<<<< Updated upstream


# GLobal Info Text:
genres_info = {"blues": "Blues_Info", "classical": "Classical_Info", "country": "Country music is known for its ballads and dance tunes with simple form, folk lyrics, and harmonies accompanied by string instruments such as electric and acoustic guitars, steel guitars (such as pedal steels and dobros), banjos, fiddles, and harmonicas. Though it is primarily rooted in various forms of American folk music, such as old-time music and Appalachian music, many other traditions, including African-American, Mexican, Irish, and Hawaiian music, have also had a formative influence on the genre.[8] Blues modes have been used extensively throughout its recorded history.", "disco": "Disco_Info",
               "hiphop": "Hiphop_Info", "jazz": "Jazz_Info", "metal": "Metal_Info", "pop": "Pop_Info", "reggae": "Reggae_Info", "rock": "Rock_Info"}

=======
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
matplotlib.use('agg')
import xgboost
>>>>>>> Stashed changes

def get_genre_dict():
    genres = ["blues", "classical", "country", "disco",
              "hiphop", "jazz", "metal", "pop", "reggae", "rock"]
    # Create Dictionary to map genres to numbers of the algorithm
    my_dict = dict(zip(range(len(genres)), genres))
    return my_dict

# Extract Features and saves as dataframe


def extract_extern(filedir, filename):
    offset = 0
    duration = 3
    go = True
    i = 0
    csv = []
    length = 0
    length_audio = librosa.get_duration(filename=filedir)
    offset = length_audio/4
    end = length_audio*3/4

    while (go):
        y, sr = librosa.load(filedir, offset=offset, duration=duration)
        if (length != len(y) and length != 0) or (offset + duration) >= end:
            i = 0
            break
        length = len(y)
        offset += duration

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
        freqs = librosa.cqt_frequencies(
            C.shape[0], fmin=librosa.note_to_hz('A1'))
        perceptr = librosa.perceptual_weighting(C**2, freqs, ref=np.max)
        perceptr_mean = np.mean(perceptr)
        perceptr_var = np.var(perceptr)
        # _____tempo______
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr)[0]
        # _____mfcc______
        mfcc = librosa.feature.mfcc(y=y, sr=sr)
        mdict = {"name": filename,
                 "name_v": filename+"."+str(i),
                 "filedir": filedir,
                 "start": offset-duration,
                 "length": length,
                 "chroma_stft_mean": chroma_stft_mean,
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

        csv.append(mdict)
        i += 1
    return csv


def extract_and_save(filedir, filename):
    df = pd.DataFrame(extract_extern(filedir, filename))
    df.to_csv("features_last_song.csv")


def predict_last(features_csv):
    xgb = xgboost.XGBClassifier()
    xgb.load_model("./Trained_Models/xgb_model.txt")
    df = pd.read_csv(features_csv)
    name = df['name']
    data = df.iloc[0:, 5:]
    preds = xgb.predict(data)  # Make Prediction
    proba = xgb.predict_proba(data)  # get Probabilities
    return preds, proba, name


def pred_time_series():
    # Sort time and prediction
    preds, proba, name = predict_last("features_last_song.csv")
    df = pd.read_csv("features_last_song.csv")
    start = df['start']  # Get start time from dataframe
    my_dict = get_genre_dict()
    genres = my_dict.values()
# Remove Predictions where the probability is less than then setted percentage
    percentage = 0.50
    i = 1
    list = []
    while i < len(preds):
        if proba[i][proba[i].argmax()] < percentage:
            list.append(i)
        i += 1
# Delete the elements and resize the list
    proba = np.delete(proba, list, axis=0)
    preds = np.delete(preds, list, axis=0)
    start = start.drop(list)

# Plot the genres to the time series of the start times !!Attention: Plot does not show empty points!!
    fig, ax = plt.subplots()
    fig.set_size_inches(8, 5)
    plt.title("Predictions over Time")
    plt.ylabel("Genres")
    prediction_label = []
    for i in range(len(preds)):
        prediction_label.append(my_dict[preds[i]])
    time = pd.to_datetime(start, unit='s').dt.strftime('%M:%S')
    plt.xticks(rotation=-90)
    ax.scatter(time, prediction_label, linewidth=2.0)
    plt.xlabel("Time [min]")
    plt.savefig("media/last_time_series.png")
    #plt.close('all')
   

# Show the Probabilities of every prediction (two main classes):


def get_first_preds_proba(no_proba):
    preds_small = ""
    my_dict = get_genre_dict()
    genres = my_dict.values()
    preds, proba = predict_last("features_last_song.csv")
    for i in range(len(preds)):
        preds_small += "Prediction " + \
            str(i) + ": " + my_dict[preds[i]] + " with Probabilities: "
        first = proba[i].argmax()
        temp = proba[i].copy()
        temp[first] = 0
        second = temp.argmax()
        preds_small += str(round(proba[i][first]*100, 1)
                           ) + "% (" + my_dict[first] + ")"
        if no_proba == 2:
            preds_small += ", " + \
                str(round(proba[i][second]*100, 1)) + \
                "% (" + my_dict[second] + ")\n"
        else:
            preds_small += "\n"
    return preds_small


def get_genre_info(pred):
    return genres_info[pred]

# Show the Probabilities of every prediction (all classes):


def get_preds_all_proba():
    my_dict = get_genre_dict()
    temp = ""
    temp += str(my_dict.values()) + "\n"
    preds, proba = predict_last("features_last_song.csv")
    for i in range(len(preds)):
        temp += "Prediction " + str(i) + ": " + \
            my_dict[preds[i]] + " with Probabilities: "
        for k in range(len(proba[i])):
            temp += str(round(proba[i][k]*100, 1)) + "%, "
        temp += "\n"
    return temp

# Not ready: Should be the mean of every probability in every bin (so average proba over all metal predictions)


def avg_algorithm_probability():
    preds, proba = predict_last("features_last_song.csv")
    my_dict = get_genre_dict()
    av_proba = np.zeros(len(my_dict.values()), dtype=float)
    laenge = np.zeros(len(my_dict.values()), dtype=int)
    threshold = 0.5
    string = "Average Probability of Algorithm Prediction which where over " + \
        str(threshold*100) + " % \n"
    for genre in range(len(my_dict.values())):
        for prob in range(len(proba)):
            if proba[prob][genre] > threshold:
                av_proba[genre] += proba[prob][genre]
                laenge[genre] += 1
            if prob == len(proba)-1 and laenge[genre] > 0:
                av_proba[genre] = av_proba[genre]/laenge[genre]
                string += my_dict[genre] + ": " + \
                    str(np.round(av_proba[genre]*100, 1)) + " % \n"

    return string

# Print Binned Statistics


def get_binned_static():
    text = ""
    preds, proba, name = predict_last("features_last_song.csv")
    my_dict = get_genre_dict()
    average_proba = []
    text += repr(len(preds))+" single parts of the song \"" + \
        str(name[0]) + \
        "\" predicted. \n\nHere are the Predictions grouped by Genres: \n"

    # Print all predictions binned on the gernes
    for i in range(len(my_dict)):
        if i < len(np.bincount(preds)):
            text = text + my_dict[i] + ": " + repr(np.bincount(preds)[i]) + " (" + repr(
                round(np.bincount(preds)[i]/len(preds)*100, 1)) + "%) \n"

    # Use the frequent value as main prediction:
    prediction = my_dict[np.bincount(preds).argmax()]
    text += "\nThe most predicted genre is:    " + prediction + \
        " (" + repr(round(np.bincount(preds)
                          [np.bincount(preds).argmax()]/len(preds)*100, 1)) + "% of the samples)"
    return prediction, text
