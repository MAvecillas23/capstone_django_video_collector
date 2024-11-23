from urllib import parse    # import this to be able to get the id from an url
from django.db import models
from django.core.exceptions import ValidationError  # import validation error


# Create your models here.
class Video(models.Model):
    # fields that will be in the video objects that map to database columns in
    # the video table of a database

    name = models.CharField(max_length=200) # name of video/ user must enter this field
    url = models.CharField(max_length=400)  # url of video/ user must enter this field
    notes = models.TextField(blank=True, null=True) # notes for video/ optional
    video_id = models.CharField(max_length=40, unique=True) # holds the video url's ID to be able to display videos on our app.
                                                            # constraint is unique to avoid duplicate videos

    def save(self, *args, **kwargs):
        # extract video id from a youtube url

        # raise validation error if url doesn't start with the youtube url
        if not self.url.startswith('https://www.youtube.com/watch'):
            raise ValidationError(f'Not a Youtube url {self.url}')

        url_components = parse.urlparse(self.url)
        query_string = url_components.query     # ex. v=2424lkjk
        if not query_string:
            raise ValidationError(f'Invalid Youtube URL {self.url}')
        parameters = parse.parse_qs(query_string, strict_parsing=True)  # dictionary
        v_parameters_list = parameters.get('v') # return none if no key found
        if not v_parameters_list: # checking if None or empty list
            raise ValidationError(f'Invalid Youtube URL, missing parameters {self.url}')
        self.video_id = v_parameters_list[0] # string

        super().save(*args, **kwargs) # because we overrode djangos save() method this ensures
                                            # djangos original save() method is called


    # string function returns ID, Name, URL, and Notes-the first 200 characters as shown below
    def __str__(self):
        return f'ID: {self.pk}, Name: {self.name}, URL: {self.url}, Video ID: {self.video_id}, Notes: {self.notes[:200]}'