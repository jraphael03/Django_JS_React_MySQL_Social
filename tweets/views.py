import random
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from .forms import TweetForm
from .models import Tweet

ALLOWED_HOSTS = settings.ALLOWED_HOSTS  # Allows host grabbed from settings.py

# Create your views here.
def home_view(request, *args, **kwargs):
    #print(args, kwargs)
    #return HttpResponse("<h1>Hello World</h1>")
    return render(request, "pages/home.html", context={}, status=200)


# VIEW FOR CREATING (POST) A TWEET 
def tweet_create_view(request, *args, **kwargs):
    #print("ajax", request.is_ajax())
    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next") or None     # "next" comes from form on home.html
    if form.is_valid():                         # if form is valid save, if it is not valid the page will render that
        obj = form.save(commit = False)
        # do other form related logic
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201) # 201 == created items     serialize comes from models

        # Utilizing redirect
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):            # if next_url != none redirect to new next_url, also checks url to make sure it is safe
            return redirect(next_url)
        form = TweetForm()          # reintializes blank form

    #Render error
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status=400)
    return render(request, 'components/form.html', context={"form": form})     # Pass form through the context


        
    



# GETTING TWEETS FROM DB
def tweet_list_view(request, *args, **kwargs):
    """ REST API VIEW, CONSUMED BY JS, RETURN JSON DATA
    """
    qs = Tweet.objects.all()    # Grabbing all Tweet objects from the Tweet Model
    tweets_list = [x.serialize() for x in qs]   # setailize grabs all inner data from models

    # tweets_list = [{ "id": x.id, "content": x.content, "likes": random.randint(0, 1353) } for x in qs]        # Listing out the items we want to pull from Tweet
    data = {
        "isUser": False,
        "response": tweets_list
    }
    return JsonResponse(data)



# USING ID IN URL TO GET ITEM FROM THE DB
def tweet_detail_view(request, tweet_id, *args, **kwargs):
    """ REST API VIEW, CONSUMED BY JS, RETURN JSON DATA
    """
    data = {
        "id": tweet_id,
    } 
    status = 200
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data['content'] = obj.content
    except:
        data['message'] = "Not Found"
        status = 404

    #return HttpResponse(f"<h1>Hello {tweet_id} - {obj.content}</h1>")   # f needs to be in the front
    return JsonResponse(data, status=status)   # Returns a dictionary of data from above
    