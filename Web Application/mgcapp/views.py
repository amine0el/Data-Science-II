from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage

def home(request):
    return render(request, 'mgcapp/home.html')


def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage(location='mgcapp/music')
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'mgcapp/upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'mgcapp/upload.html')