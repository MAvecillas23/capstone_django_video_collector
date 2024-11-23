# this code shows how to create a form to display on the webpage

# import these
from django import forms
from .models import Video

# holds the data that video name, url, notes inputs will be entered into
class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['name', 'url', 'notes']


# holds the search term that user enters when they want to search for similar videos
class SearchForm(forms.Form):
    search_term = forms.CharField()