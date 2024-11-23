from django.contrib import admin

# Register your models here.
# add the video models that will be displayed to the admin site
# registering your models
from .models import Video
admin.site.register(Video)


# after registering models shown above.
# create superuser by going on the terminal and typing: python createsuperuser and following the prompts (email not needed)
# then:
# go to the terminal and type:
# python manage.py makemigrations... press enter
# then type: python manage.py migrate ... press enter

# this creates video models and builtin models related to creating users from the admin side