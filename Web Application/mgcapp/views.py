
# GenRec - The Smash Group
    # Music Genre Recommender and Classifier
    # Project during Data Science 2
    # WiSe 2022/2023
    # TU Darmstadt

# File views.py
    # Description: 
        # Main Page of the Webserver --> Here are the functions of each webpage defined. 
        # The file uses redirects and renders to navigate through the pages and display html pages
        # The assignment of the urls to the function is done in the urls.py

#Import of Django-Libraries
from mgcapp.forms import DocumentForm
from mgcapp.models import Document
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.images import ImageFile
from django.core.files.storage import FileSystemStorage


# Import GenRec specific functions for recommendation and Classification/prediction
from mgcapp.prediction import *
from mgcapp.recommender import *
from mgcapp.tasks import extraction_async



# Function used to display the home page
    # Description: The home-page displays the welcome text and the last predicted songs. 
    # Each Song can be listened to and with a click on a button predicted/last prediction displayed
    # returns: html page with songs from the database or render to prediction.html
def home(request):
    # Check if Button is clicked to view a prediction of a song
    if request.method == 'POST':
        data = request.POST
        if "document" in data:
            # Song name is coded into the value of the button to know what song is desired
            action = data.get("document")
            if action != "":
                documents = Document.objects.filter(name__icontains=action)
                documents = documents[0]
                # if there is no prediction is the database, repredict the song
                if documents.prediction == "":
                    documents, genre_info=repredict(documents)
                    return render(request, 'mgcapp/prediction.html', {
                    'document': documents,
                    'genre_info': genre_info,
                    'old_pred':True})      
                else: # Prediction is already done and only needs to be displayed
                    genre_info = get_genre_info(documents.prediction)
                    return render(request, 'mgcapp/prediction.html', {
                        'document': documents,
                        'genre_info': genre_info, 
                        'old_pred': True})
        else:
            return redirect("home")
    else: # Normal HTTP-GET of home-page return the last 10 uploaded songs with their prediction
        documents = Document.objects.order_by('-uploaded_at').all()[:10]
        return render(request, 'mgcapp/home.html', { 'documents': documents })

# Function used to display the upload-page
    # Description: The upload-function checks if the HTTP-POST contains a file and uploads it to the database
    # If the file is uploaded it redirects the user to the prediction-page
    # returns: html page with file upload input or with button to prediction page
def simple_upload(request):
    if request.method == 'POST':
        data = request.POST
        action = data.get("type")
        # Checks if button to prediction is activated and redirects
        if action == "genre":        
            return redirect('prediction')
        # Checks for uploaded file and saves it in the database
        elif action == "file" and 'myfile' in request.FILES:
            myfile = request.FILES['myfile']
            # Only Wav- and mp3-files are supported currently...
            if (".mp3" in myfile.name) or (".wav" in myfile.name):
                qs = Document(name=myfile.name,document=myfile)
                qs.save()
                task = extraction_async.delay()
                # Start extraction here
                
                return render(request, 'mgcapp/upload.html',{
                    'uploaded_file_url':True,
                    'task_id' : task.task_id
                })                
            else:# Different formats results in an Format-Error
                return render(request, 'mgcapp/upload.html', {
                    'format_error': "Please use a valid song format for example .mp3 or .wav!"
                })
    return render(request, 'mgcapp/upload.html')

# Function used to display the prediction page
    # Description: The prediction page handles the feature extraction and displays the prediction text
    # 
    # Each Song can be listened to and with a click on a button predicted/last prediction displayed
    # returns: html page with songs from the database or render to prediction.html
def extraction_view(request):
    #if running_Extraction = False:
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
    
    pred, pred_text = get_binned_static(documents.extraction.path)
    genre_info = get_genre_info(pred)
    pred_time_series()
    with open('media/last_time_series.png', 'rb') as existing_file:
        django_image_file = ImageFile(file=existing_file, name='last_time_series.png')
        documents.timeSeries = django_image_file
        documents.save()
    documents = Document.objects.last()
    documents.prediction = pred
    documents.prediction_text = pred_text
    documents.save()
    
    return render(request, 'mgcapp/prediction.html', {
        'document': documents,
        'genre_info': genre_info
    })
    
def repredict(documents):
    pred, pred_text = get_binned_static(documents.extraction.path)
    genre_info = get_genre_info(pred)
    pred_time_series()
    with open('media/last_time_series.png', 'rb') as existing_file:
        django_image_file = ImageFile(file=existing_file, name='last_time_series.png')
        documents.timeSeries = django_image_file
        documents.save()
    documents.prediction = pred
    documents.prediction_text = pred_text
    documents.save()
    return documents, genre_info

    
    
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






