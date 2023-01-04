## Skript zum Sortieren der FMA Pakete - eingestellt auf das medium Paket

import shutil
import os
import librosa
import soundfile as sf
import utils

AUDIO_DIR = 'fma_medium/'
tracks = utils.load('tracks.csv')

os.mkdir('fma_sortiert')

small = tracks['set', 'subset'] <= 'medium'

y_small = tracks.loc[small, ('track', 'genre_top')]

for track_id, genre in y_small.iteritems():
    if genre == 'Old-Time / Historic':
        genre = 'Historic'
    if not os.path.exists('fma_sortiert/'+genre):
        os.mkdir('fma_sortiert/'+genre)

    src = utils.get_audio_path(AUDIO_DIR, track_id)
    dst = 'fma_sortiert/'+genre+'/'+str(track_id)+'.mp3'
    shutil.copyfile(src, dst)