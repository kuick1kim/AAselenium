from django.urls import path

from posts.views import *

app_name = "posts"
urlpatterns = [
    path("feeds/", feeds, name="feeds"),



    path('button/', button_view, name='button_view'),
    path('upload/', upload_excel, name='upload_excel'),
    path('download/', download_file, name='download_file'),
     path('download_result/', download_result, name='download_result'),

]
