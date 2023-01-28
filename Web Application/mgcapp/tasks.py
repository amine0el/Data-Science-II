from celery import shared_task
from celery_progress.backend import ProgressRecorder
from MGC.settings import RUNNING_EXTRACTION
from time import sleep
from mgcapp.prediction import *

@shared_task(bind=True)
def extraction_async(self, documents):
    progress_recorder = ProgressRecorder(self)
    extract_and_save(documents.document.path,documents.name, progress_recorder)
    RUNNING_EXTRACTION = False
    
    #progress_recorder.set_progress(i + 1, 100, f'On iteration {i}')
    return 'Done'