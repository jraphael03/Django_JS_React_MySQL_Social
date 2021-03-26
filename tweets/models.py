from django.db import models
import random;

# When you change this file run 
# python3 manage.py make migrations
# python3 manage.py migrate

class Tweet(models.Model):
    # Maps to SQL Data
    # id = models.AutoField(primary_key=true)   (hidden field does not need to be added)
    content = models.TextField(blank=True, null=True)                          # blank means it's not required in Django, and null means it's not required in db
    image = models.FileField(upload_to='images/', blank=True, null=True)       # In db there will be a path to file we uploaded 

    # Show tweets is descending order on page
    class Meta:
        ordering = ['-id']  # Prepend tweets by using -id which is descending order

    def serialize(self):
        return{
            "id": self.id,
            "content": self.content,
            "likes": random.randint(0, 200)
        }
