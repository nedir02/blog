from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def home_view(request):  # request isleg  diymegi anladyar. funksiya doredemizde hokman parametr gorkezmeli meselem request
    if request.user.is_authenticated:
        context = {
            'isim': "Guwanch",
            "detail": 'mashennik'
        }
    else:
        context = {
            'isim': "misafir",

        }
    return render(request, 'home.html', context)