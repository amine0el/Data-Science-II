# Import Libraries:
import xgboost
import matplotlib
matplotlib.use('agg')
from matplotlib import dates as mdates
from matplotlib import pyplot as plt
from mutagen.easyid3 import EasyID3
import pandas as pd
import numpy as np
import librosa
import warnings
warnings.filterwarnings('ignore')


# GLobal Info Text:
genres_info = {"blues": "Blues is a music genre that developed in the United States in the early 20th century. It has its roots in African-American spirituals, work and field songs. Blues is characterized by emotional lyrics that often deal with themes such as heartbreak, poverty and oppression. The music itself is characterized by the use of blues chords, a melancholy rhythm and improvised guitar and harmonica solos. Blues has also influenced many other music genres, including rock and roll, jazz, and country. Today, there are many different subgenres of blues, such as Chicago blues, Delta blues, and Texas blues.",
               "classical": "Classical music is a genre of music that encompasses a wide range of styles and periods, dating back to the 9th century. It is typically characterized by its complexity, formal structure and the use of orchestras, choirs, and solo performers. It often features a wide range of dynamic expressions, intricate melodies and harmonies. Classical music has its origins in the Western musical tradition and it is usually written by composers with formal training. The classical period is also divided into different eras like Baroque, classical, romantic and contemporary. Classical music is also associated with formal concert performances, and is often heard in concert halls, opera houses, and ballet performances. It's considered as a serious and demanding art form which requires dedicated listening.",
               "country": "Country music is known for its ballads and dance tunes with simple form, folk lyrics, and harmonies accompanied by string instruments such as electric and acoustic guitars, steel guitars (such as pedal steels and dobros), banjos, fiddles, and harmonicas. Though it is primarily rooted in various forms of American folk music, such as old-time music and Appalachian music, many other traditions, including African-American, Mexican, Irish, and Hawaiian music, have also had a formative influence on the genre.[8] Blues modes have been used extensively throughout its recorded history.",
               "disco": "Disco is a genre of music that emerged in the 1970s and was especially popular in the mid to late 1970s and early 1980s. It's characterized by its upbeat tempo, repetitive rhythms, and catchy melodies. Disco music is typically played in dance clubs and is known for its emphasis on rhythm, and for its heavy use of synthesizers, horns, and electric bass. Disco music is often associated with the disco culture, which was characterized by the fashion, dancing and social scene of the time. Disco music had a significant impact on the development of other genres such as funk, house and techno. Even though disco was largely pushed out by the rise of punk and new wave in the early 1980s, it has recently seen a resurgence in popularity, with many contemporary artists incorporating disco elements into their music.",
               "hiphop": "Hip-hop is a genre of music that emerged in the 1970s in the African American community, primarily in the Bronx, New York City. It's characterized by its use of rapping (a vocal style in which the artist speaks rhythmically and in rhyme), beats produced by drum machines or samples and often includes elements of funk, soul and R&B. Hip-hop is also known for its use of turntablism, where DJs use turntables to create new sounds and beats. It's a genre that reflects the culture and experiences of urban, often marginalized communities. Hip-hop has grown to be one of the most popular and influential genres in music today, with many subgenres and variations, including rap, trap, and conscious rap. Hip-hop has also had a significant impact on fashion, film, television and other aspects of popular culture.",
               "jazz": "Jazz is a genre of music that originated in African American communities in the late 19th and early 20th centuries, particularly in New Orleans, Louisiana. It's characterized by its improvisational nature, syncopated rhythms, and a fusion of different musical elements such as blues, gospel and European harmony. Jazz is known for its use of complex harmonies, syncopated rhythms, and the use of various musical forms such as the blues and swing. Jazz has evolved over time, giving birth to many subgenres such as bebop, swing, and fusion. Jazz music has been considered as an art form and has been associated with intellectual and cultural movements. It has been influential in the development of other genres of music such as blues, rock and roll, and hip-hop. Today, jazz music is still widely appreciated and played, and it's still an important part of American culture.",
               "metal": "Metal is a genre of music that emerged in the late 1960s and early 1970s, characterized by its heavy use of electric guitar, bass, drums, and vocals. It's known for its aggressive and powerful sound, often featuring distorted guitar riffs, fast-paced drumming and powerful vocals. Metal music is also known for its use of various sub-genres and sub-cultures such as thrash metal, black metal, death metal, and power metal. Metal music has also been associated with a particular lifestyle and fashion, including leather and denim clothing, long hair, and tattoos. Metal music has its roots in blues-rock and classical music but it has evolved over time to become more extreme and diverse, with many subgenres and variations. Metal music has a dedicated fan base and continues to be an important part of the music scene.",
               "pop": "Pop music is a genre of music that emerged in the late 1950s and early 1960s, characterized by its commercial melodies, light lyrics and catchy drums, bass, guitar and vocals. It's known for its accessible and commercial melodies, as well as its widespread popularity in charts and radio shows. Pop music has its roots in rock and folk music, but has evolved over time to incorporate elements of R&B, hip-hop, and electronic music. Pop music reaches a wide audience and is one of the most widespread music genres in the world.",
               "reggae": "Reggae is a genre of music that originated in Jamaica in the 1960s and is characterized by its distinct rhythm, political and social messages, and use of guitar, bass, drums and keyboard. It has its roots in ska and rocksteady music and later incorporated influences from R&B, soul and dub music. Reggae music also has a strong connection to Rastafarianism and its message often includes spiritual and religious themes. Reggae music also had a strong impact on other music genres such as hip-hop and dancehall.",
               "rock": "Rock is a genre of music that emerged in the 1950s and is characterized by its powerful and energetic sound. It's primarily played with guitar, bass, drums, and vocals and has roots in blues music. Over the years, rock has evolved into many subgenres such as classic rock, hard rock, punk rock, grunge and alternative rock. Rock music often has a rebellious and provocative nature and addresses themes such as love, rebellion and social injustice. Rock music has also had a strong impact on other music genres and cultures worldwide."}


def get_genre_dict():
    genres = ["blues", "classical", "country", "disco",
              "hiphop", "jazz", "metal", "pop", "reggae", "rock"]
    # Create Dictionary to map genres to numbers of the algorithm
    my_dict = dict(zip(range(len(genres)), genres))
    return my_dict

# Extract Features and saves as dataframe


def extract_extern(filedir, filename,progress_recorder):
    offset = 0
    duration = 3
    go = True
    i = 0
    csv = []
    length = 0
    if(".mp3" in filename):
        audio = EasyID3(filedir)
        audio.delete()
        audio.save()
    length_audio = int(librosa.get_duration(filename=filedir))
    start = int(length_audio/4)
    offset = start
    end = int(length_audio*3/4)
    while (go):
        y, sr = librosa.load(filedir, offset=offset, duration=duration)
        if (length != len(y) and length != 0) or (offset + duration) >= end:
            i = 0
            break
        length = len(y)
        offset += duration
        progress_recorder.set_progress(round(i/((end-start)/duration)*100,1), 100)
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


def extract_and_save(filedir, filename, progress_recorder):
    path = "features_last_song.csv"
    df = pd.DataFrame(extract_extern(filedir, filename,progress_recorder))
    df.to_csv(path)
    return path



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


def get_binned_static(path):
    text = ""
    preds, proba, name = predict_last(path)
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
