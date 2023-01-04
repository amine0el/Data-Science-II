from mgcapp.forms import DocumentForm
from mgcapp.models import Document
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from mgcapp.prediction import *

def home(request):
    documents = Document.objects.order_by('-uploaded_at').all()
    
    return render(request, 'mgcapp/home.html', { 'documents': documents })


def simple_upload(request):
    if request.method == 'POST':
        data = request.POST
        action = data.get("type")
        if action == "genre":
            
            
            return redirect('prediction')
        elif action == "statistic":
            pred_time_series()
            return render(request, 'mgcapp/upload.html', {
                    'more_stat': "Here are your Statistics:"
                })
        elif action == "file" and 'myfile' in request.FILES:
            myfile = request.FILES['myfile']
            if (".mp3" or ".wav") in myfile.name:
                
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                uploaded_file_url = fs.url(filename)
                qs = Document(name=myfile.name,document=myfile)
                qs.save()
                return render(request, 'mgcapp/upload.html', {
                    'uploaded_file_url': uploaded_file_url,
                })
            else:
                return render(request, 'mgcapp/upload.html', {
                    'format_error': "Please use a valid song format for example .mp3 or .wav!"
                })
            
   
    return render(request, 'mgcapp/upload.html')

def extraction_view(request):
    documents = Document.objects.last()
    extract_and_save(documents.document,documents.name)
    pred, pred_text = get_binned_static()
    pred_time_series()
    documents.prediction = pred
    documents.prediction_text = pred_text
    documents.save()
    return render(request, 'mgcapp/prediction.html', {
        'document': documents
    })
    

