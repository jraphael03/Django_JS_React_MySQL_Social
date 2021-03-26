from django.contrib import admin
from django.urls import path, re_path   # url()

from tweets.views import (
    home_view, 
    tweet_detail_view, 
    tweet_list_view,
    tweet_create_view,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view),        # http://127.0.0.1:8000
    path('abc/', home_view),    # http://127.0.0.1:8000/abc/
    path('tweets', tweet_list_view),   # http://127.0.0.1:8000/tweets
    path('create-tweet', tweet_create_view),   # http://127.0.0.1:8000/create-tweet
    path('tweets/<int:tweet_id>', tweet_detail_view),   # http://127.0.0.1:8000/tweets/1234
]
