from mgcapp.forms import DocumentForm
from mgcapp.models import Document
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from mgcapp.prediction import *
from mgcapp.recommender import *

def home(request):
    documents = Document.objects.order_by('-uploaded_at').all()[:10]
    
    return render(request, 'mgcapp/home.html', { 'documents': documents })


def simple_upload(request):
    if request.method == 'POST':
        data = request.POST
        action = data.get("type")
        if action == "genre":
            
            
            return redirect('prediction')
        elif action == "file" and 'myfile' in request.FILES:
            myfile = request.FILES['myfile']
            if (".mp3" or ".wav") in myfile.name:
                qs = Document(name=myfile.name,document=myfile)
                qs.save()
                return render(request, 'mgcapp/upload.html',{
                    'uploaded_file_url':True
                })
            else:
                return render(request, 'mgcapp/upload.html', {
                    'format_error': "Please use a valid song format for example .mp3 or .wav!"
                })
            
   
    return render(request, 'mgcapp/upload.html')

def extraction_view(request):
    if request.method == 'POST':
        data = request.POST
        action = data.get("type")
        if action == "recommender":
            
            
            return redirect('recommender')
        else: 
            return render(request, 'mgcapp/recommender.html', {
                    'format_error': "Something went wrong! :)"
                })
    documents = Document.objects.last()
    extract_and_save(documents.document.path,documents.name)
    pred, pred_text = get_binned_static()
    genre_info = get_genre_info(pred)
    pred_time_series()
    documents.prediction = pred
    documents.prediction_text = pred_text
    documents.save()
    
    return render(request, 'mgcapp/prediction.html', {
        'document': documents,
        'genre_info': genre_info
    })
    

    
def recommender_view_worst(request):
    recom_series = get_extraction_similarity("worst")
    documents = Document.objects.last()
    print(documents.document.url)
    path = path = '/media/fma_medium_unsortiert/'

    output = "Take a look at these songs, they are completely different!\n\n"
    output += "Songname \t\t\t\t Similarity\n"
    songfiles =[]
    
    for i in range(len(recom_series)):
        song_data=[]
        song_data.append(str(recom_series.keys()[i][0]) + " \t\t\t\t " + str(round(recom_series[i]*100,1)) +"% \n")
        song_data.append(path + str(recom_series.keys()[i][1]) + ".mp3")
        songfiles.append(song_data)
        
    return render(request, 'mgcapp/recommender.html', {
        'recommendation_text' : output,
        'songfiles': songfiles,
        'document': documents,
        'media_path': path,
        'discommender': True
    })

def recommender_view(request):
    if request.method == 'POST':
        data = request.POST
        action = data.get("type")
        if action == "get-worst":
            
            
            return redirect('recommender-worst')
        else: 
            return render(request, 'mgcapp/recommender.html', {
                    'format_error': "Something went wrong! :)"
                })
    recom_series = get_extraction_similarity("best")
    documents = Document.objects.last()
    print(documents.document.url)
    path = '/media/fma_medium_unsortiert/'

    output = "Here are five similiar songs to the Song \"" + str(documents.name) + "\" :\n\n"
    output += "Songname \t\t\t\t Similarity\n"
    songfiles =[]
   
    for i in range(len(recom_series)):
        song_data=[]
        song_data.append(str(recom_series.keys()[i][0]) + " \t\t\t\t " + str(round(recom_series[i]*100,1)) +"% \n")
        song_data.append(path + str(recom_series.keys()[i][1]) + ".mp3")
        songfiles.append(song_data)
        
    return render(request, 'mgcapp/recommender.html', {
        'recommendation_text' : output,
        'songfiles': songfiles,
        'document': documents,
        'media_path': path
    })



