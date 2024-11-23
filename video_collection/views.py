from django.shortcuts import render, redirect, get_object_or_404
from .forms import VideoForm, SearchForm  # import to access views.py VideoForms object and SearchForm
from django.contrib import messages # this is for temporary messages ex. "Success adding video" when video is added
from .models import Video   # querying databases and work with the Video class
from django.core.exceptions import ValidationError # import validation error
from django.db import IntegrityError    # import integrity error for duplicate videos
from django.db.models.functions import Lower # lowers anything in the db to lower case

# Create your views here.

# homepage
def home(request):
    app_name = 'NFL Football Videos'  # name of the app to display on page

    # render homepage and return any variables you want to display on that page
    # defined above
    # for example link the variable name app_name with the html homepage variable name you want to name
    # for this instance, it will be app_name as well
    return render(request, 'video_collection/home.html', {'app_name': app_name})

# add a new video
def add(request):
    # if request.method (the add video button is clicked)
    if request.method == 'POST':
        new_video_form = VideoForm(request.POST) # then add a new video data in the VideoForm object with its data
        if new_video_form.is_valid():
            # try block to catch validation and integrity errors
            try:
                # if all appropriate fields are entered and valid
                new_video_form.save()   # save that object to the db
                # messages.info(request, 'New video saved!') # display a temporary message to tell user is saved
                return redirect('video_list')   # if new_video_form saves successfully redirect user to video_list page
            # this is caught if users enters anything in the url that isn't a youtube url
            except ValidationError:
                messages.warning(request, 'Invalid YouTube URL')
           # this is caught if user enters a video url that already exists
            except IntegrityError:
                messages.warning(request, 'You already added this video')

        # if fields entered are not valid
        messages.warning(request, 'Please check the data entered')   # display a temporary message to tell user video was not saved
        # display the same page but with the data that was already entered/ in the VideoForm object
        # so user can make changes and edits
        return render(request, 'video_collection/add.html',{'new_video_form': new_video_form})

    new_video_form = VideoForm()    # VideoForm object holds video name, url, and notes

    # render add.html with respective variables
    return render(request, 'video_collection/add.html', {'new_video_form': new_video_form})

# gets and display all videos
def video_list(request):
    search_form = SearchForm(request.GET) # build form from data user has sent to app

    if search_form.is_valid():
        search_term = search_form.cleaned_data['search_term']   # this is whatever user typed as a search
        videos = Video.objects.filter(name__icontains=search_term).order_by(Lower('name')) # looks for a match of search term in all videos/ Lower function lowercases name to make searches with same letters be next to each other and reverts any changes after wards

    else:   # form is not filled in or this is the first time user sees the page
        search_form = SearchForm()
        videos = Video.objects.all().order_by(Lower('name'))    # get all videos from the database

    # render video_list page with the list of videos
    return render(request, 'video_collection/video_list.html', {'videos': videos, 'search_form': search_form})


# gets the details of a video that when the video name link on video_list page is clicked
def video_details(request, video_pk):
    # when video name is clicked in video_list... get the primary key to find the Video object with that PK
    # if there is no PK that matches raise a 404 error
    video = get_object_or_404(Video, pk=video_pk)

    # render template with video object that matches primary key
    return render(request, 'video_collection/video_details.html', {'video': video})






