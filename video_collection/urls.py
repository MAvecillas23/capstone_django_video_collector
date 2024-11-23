""" this file is needed to be created  manually under the video_collection directory
this holds the urls that we create """

from django.urls import path    # describe url and relationship between text and code response of url
from . import views

urlpatterns = [
    # these url patterns act as pages in a webpage
    path('', views.home, name='home'), # views.home is calling the home function from views.py... the name param gives this path a name for reference
    path('add', views.add, name='add_video'), # adding a video from the add page
    path('video_list', views.video_list, name='video_list'), # display video list from the video_list page
    path('video_details/<int:video_pk>/', views.video_details, name='video_details') # this page will hold video details of the video based off of primary key
]