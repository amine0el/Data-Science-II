from mgcapp.models import Document
from celery import shared_task
from celery_progress.backend import ProgressRecorder
from django.core.files import File
from MGC.settings import RUNNING_EXTRACTION
from time import sleep
from mgcapp.prediction import *
from mgcapp.recommender import *

@shared_task(bind=True)
def extraction_async(self):
    documents = Document.objects.last()
    progress_recorder = ProgressRecorder(self)
    path = extract_and_save(documents.document.path,documents.name, progress_recorder)
    RUNNING_EXTRACTION = False
    with open(path, 'r') as existing_file:
        django_file = File(existing_file)
        documents.extraction = django_file
        documents.save()
    
    #progress_recorder.set_progress(i + 1, 100, f'On iteration {i}')
    return 'Done'



@shared_task(bind=True)
def extraction_full_async(self):
    documents = Document.objects.last()
    progress_recorder = ProgressRecorder(self)
    path = str(BASE_DIR) + '/mgcapp/'
    data = read_features(progress_recorder)
    data.to_csv(path + "features_last_full_song.csv")
    return 'Done'