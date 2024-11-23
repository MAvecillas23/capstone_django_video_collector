from django.test import TestCase
from django.urls import reverse  # this converts the name of a url to the actual path
from .models import Video   # importing video objects
from django.db import IntegrityError
from django.core.exceptions import ValidationError


class TestHomePageMessage(TestCase):
    # test that the correct homepage title is displayed
    def test_app_title_message_shown_on_homepage(self):
        # generates the right url using the url name from urls.py
        url = reverse('home')
        # access the webpage using the url/ get webpage
        response = self.client.get(url)
        # check if the webpage contains this string
        self.assertContains(response, 'NFL Football Videos')


class TestAddVideos(TestCase):
    # test that valid videos are being added
    def test_add_video(self):
        # test data for a valid video
        valid_video = {
            'name': 'Vikings vs Chiefs',
            'url': 'https://www.youtube.com/watch?v=LluAI0f0N9s',
            'notes': 'Pretty fun game'
        }
        # get the video path
        url = reverse('add_video')
        # post request... as in adding a valid video
        # follow=True means that if request is successful then follow the redirect since after a video is added page is redirected to video list
        response = self.client.post(url, data=valid_video, follow=True)
        # check that the correct template is being used
        self.assertTemplateUsed('video_collection/video_list.html')

        # does the video list show the new video
        self.assertContains(response, 'Vikings vs Chiefs')
        self.assertContains(response, 'Pretty fun game')
        self.assertContains(response, 'https://www.youtube.com/watch?v=LluAI0f0N9s')

        # count the number of video objects in the db
        video_count = Video.objects.count()

        # were expecting 1 video object in the database
        self.assertEqual(1, video_count)

        # check that the first video object in the db names, url and notes match
        video = Video.objects.first()
        self.assertEqual('Vikings vs Chiefs', video.name)
        self.assertEqual('https://www.youtube.com/watch?v=LluAI0f0N9s', video.url)
        self.assertEqual('Pretty fun game', video.notes)
        self.assertEqual('LluAI0f0N9s', video.video_id) # check video_id from url matches


    def test_video_invalid_url_not_added(self):
        # test data for invalid urls
        invalid_video_urls = [
            'https://www.youtube.com/watch',
            'https://www.youtube.com/watch?',
            'https://www.youtube.com/watch?abc=123',
            'https://www.youtube.com/watch?v=',
            'https://www.github.com',
            'https://www.minneapolis.edu',
            'https://www.minneapolis.edu?v=21345'
        ]
        # loop through the invalid_urls list
        for invalid in invalid_video_urls:
            new_video = {
                'name': 'example',
                'url': invalid,
                'notes': 'example notes'
            }
            # get path from the add_video name
            url = reverse('add_video')
            # attempt to add videos
            response = self.client.post(url, new_video)

            # check that this template was not used
            self.assertTemplateNotUsed('video_collection/add.html')

            # get the messages that are shown to user when a video cannot be added
            messages = response.context['messages']

            # extract every message that was displayed
            message_texts = [ message.message for message in messages ]

            self.assertIn('Invalid YouTube URL', message_texts)
            self.assertIn('Please check the data entered', message_texts)

            # count video objects in db
            video_count = Video.objects.count()
            # because no videos are added, ensure there are 0 objects
            self.assertEqual(0, video_count)

class TestVideoList(TestCase):
    # test that videos are displayed in alphabetical order
    def test_all_videos_displayed_in_correct_order(self):
        # create video test objects
        v1 = Video.objects.create(name='XYZ', notes='example', url='https://www.youtube.com/watch?v=123')
        v2 = Video.objects.create(name='abc', notes='example', url='https://www.youtube.com/watch?v=124')
        v3 = Video.objects.create(name='AAA', notes='example', url='https://www.youtube.com/watch?v=125')
        v4 = Video.objects.create(name='lmn', notes='example', url='https://www.youtube.com/watch?v=126')

        # the order tha videos should be displayed
        expected_video_order = [v3, v2, v4, v1]

        url = reverse('video_list')
        response = self.client.get(url)

        videos_in_template = list(response.context['videos'])

        self.assertEqual(videos_in_template, expected_video_order)


    def test_no_video_list_message(self):
        url = reverse('video_list')
        response = self.client.get(url)
        # test that no videos is displayed when there are no videos
        self.assertContains(response, 'No videos')
        # test that there are 0 videos in the videos list
        self.assertEqual(0, len(response.context['videos']))

    def test_video_number_message_one_video(self):
        v1 = Video.objects.create(name='XYZ', notes='example', url='https://www.youtube.com/watch?v=123')

        url = reverse('video_list')
        response = self.client.get(url)

        # test video count is displayed correctly
        self.assertContains(response, '1 Video')
        # test that 1 videos is not displayed
        self.assertNotContains(response, '1 videos')

    # same as above... just test for 2 videos instead
    def test_video_number_message_two_videos(self):
        v1 = Video.objects.create(name='XYZ', notes='example', url='https://www.youtube.com/watch?v=123')
        v1 = Video.objects.create(name='ZXY', notes='example', url='https://www.youtube.com/watch?v=124')

        url = reverse('video_list')
        response = self.client.get(url)

        # test video count is displayed correctly
        self.assertContains(response, '2 Videos')


class TestVideoSearch(TestCase):
    pass


class TestVideoModel(TestCase):

    def test_invalid_url_raises_validation_error(self):
        # testing validation error is raised
        invalid_video_urls = [
            'https://www.youtube.com/watch',
            'https://www.youtube.com/watch?',
            'https://www.youtube.com/watch?abc=123',
            'https://www.youtube.com/watch?v=',
            'https://www.github.com',
            'https://www.minneapolis.edu',
            'https://www.minneapolis.edu?v=21345'
        ]

        for invalid_video_url in invalid_video_urls:
            with self.assertRaises(ValidationError):
                # attempt to save raise a validation error
                Video.objects.create(name='example', url=invalid_video_url, notes='example note' )

        self.assertEqual(0, Video.objects.count())

    def test_duplicate_video_raises_integrity_error(self):
        # test that a duplicate video isn't added

        v1 = Video.objects.create(name='XYZ', notes='example', url='https://www.youtube.com/watch?v=123')
        # raise integrity error if a duplicate is added
        with self.assertRaises(IntegrityError):
            Video.objects.create(name='XYZ', notes='example', url='https://www.youtube.com/watch?v=123')


class TestVideoDetails(TestCase):
    pass
