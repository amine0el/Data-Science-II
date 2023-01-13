from mgcapp.forms import DocumentForm
from mgcapp.models import Document
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from mgcapp.prediction import *
from mgcapp.recommender import *

def home(request):
    documents = Document.objects.order_by('-uploaded_at').all()
    
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
    extract_and_save(documents.document,documents.name)
    pred, pred_text = get_binned_static()
    pred_time_series()
    documents.prediction = pred
    documents.prediction_text = pred_text
    documents.save()
    
    return render(request, 'mgcapp/prediction.html', {
        'document': documents
    })
    

    
def recommender_view(request):
    string = str(get_extraction_similarity())
    #documents = Document.objects.last()
    #documents.recommender_text = get_extraction_similarity(df_combined, song_name, song_part)
    
    #df_input =
    #cosine_similarity = get_extraction_similarity(df_combined, name, part)
    #last_song = df['name_v'][0]
    # string = "Last Song is : " + df['name_v'][0]
    # df_db = load_csv("extraction.csv")
    # new_df= combine df and df_db
    # cosine similariry(new_df)
    # drop songs with which starts with name_v
    # sort df absteigend

    
    # for entries in df:
    #     recom = find_similar_songs(df['name_v'][entries], entries)
    #     biggest_val = recom[0]

    # string += "Similar is: " + biggest_val
    
    #documents.recommender = recom
    #documents.prediction_text = pred_text
    #documents.recommender_text = recom_text
    #documents.save()
    return render(request, 'mgcapp/recommender.html', {
        'recommendation' : string
    })



