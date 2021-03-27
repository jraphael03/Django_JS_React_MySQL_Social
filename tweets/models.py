from django.db import models
from django.conf import settings
import random;

User = settings.AUTH_USER_MODEL # REFERENCES BUILT IN DJANGO FEATURE FOR USER MODEL

# When you change this file run 
# python3 manage.py make migrations
# python3 manage.py migrate

class TweetLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)    
    tweet = models.ForeignKey("Tweet", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    


class Tweet(models.Model):
    # Maps to SQL Data
    # id = models.AutoField(primary_key=true)   (hidden field does not need to be added)
    # When running makemigration if there are items in the db user needs to be supplied a default 
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Foreign key so many users can have many tweets, on_delete=models.CASCADE   deletes all tweets when a User is deleted    # (keep storage of tweets by setting null=True on_delete=models.SET_NULL)
    likes = models.ManyToManyField(User, related_name="tweet_user", blank=True, through=TweetLike)     # Many to Many can have mulitple Users, Through our second Model
    content = models.TextField(blank=True, null=True)                          # blank means it's not required in Django, and null means it's not required in db
    image = models.FileField(upload_to='images/', blank=True, null=True)       # In db there will be a path to file we uploaded 
    timestamp = models.DateTimeField(auto_now_add=True)

    

    # Show tweets is descending order on page
    class Meta:
        ordering = ['-id']  # Prepend tweets by using -id which is descending order

    def serialize(self):
        return{
            "id": self.id,
            "content": self.content,
            "likes": random.randint(0, 200)
        }
