import random
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

# REST FRAMEWORK IMPORTS
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

from .forms import TweetForm
from .models import Tweet
from .serializers import TweetSerializer, TweetActionSerializer

ALLOWED_HOSTS = settings.ALLOWED_HOSTS  # Allows host grabbed from settings.py

# Create your views here.
def home_view(request, *args, **kwargs):
    #print(request.user) # request comes with user
    #print(args, kwargs)
    #return HttpResponse("<h1>Hello World</h1>")
    return render(request, "pages/home.html", context={}, status=200)

# DJANGORESTFRAMEWORKS USE SERIALIZERS.PY FILE

# CREATING (POST) FOR TWEET USING DJANGORESTFRAMEWORK
@api_view(['POST'])                     # http method the client == POST
@authentication_classes([SessionAuthentication])    # only SessionAuthentication is allowed
@permission_classes([IsAuthenticated])   # If the user is authenticated they have access to this is not they do not
def tweet_create_view(request, *args, **kwargs):
    serializer = TweetSerializer(data = request.POST)
    if serializer.is_valid(raise_exception=True):
        obj = serializer.save(user = request.user)
        return Response(serializer.data, status=201)                # Import response above no longer need JsonResponse
    return Response({}, status=400)


# USING ID TO GET TWEETS FROM DB USING DJANGORESTFRAMEWORK
@api_view(['GET'])
def tweet_detail_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    serializer = TweetSerializer(obj)   # Not pulling many only obj we are pulling id
    return Response(serializer.data)


# DELETING TWEET FROM DB USING DJANGORESTFRAMEWORK
@api_view(['DELETE', 'POST'])
# CHECK PERMISSION THAT THE USER CAN DELETE SELECTED TWEET
@permission_classes([IsAuthenticated])   # If the user is authenticated they have access to this is not they do not
def tweet_delete_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    # RESPONSE IF USER CANNOT DELETE
    if not qs.exists():
        return Response({}, status=404)
    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({"message": "You cannot delete this tweet"}, status=401)
    # RESPONSE FOR SUCCESSFUL DELETE
    obj = qs.first()
    obj.delete()
    return Response({"message": "Tweet removed"}, status=200)


# LIKING A TWEET
@api_view(['POST'])
# CHECK PERMISSION THAT THE USER CAN DELETE SELECTED TWEET
@permission_classes([IsAuthenticated])   # If the user is authenticated they have access to this is not they do not
def tweet_action_view(request, *args, **kwargs):
    """
    id is required
    Actions options are: like, unlike, retweet
    """
    #print(request.POST, request.data)
    serializer = TweetActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        tweet_id = data.get("id")
        action = data.get("action")

    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    # If user likes we will remove it or add
    if action == "like":
        obj.likes.add(request.user)
        serializer = TweetSerializer(obj)
        return Response(serializer.data, status=200)
    elif action == "unlike":
        obj.likes.remove(request.user)
    elif action == "retweet":
        # this is todo
        pass
    return Response({}, status=200)


# GETTING TWEETS FROM DB USING DJANGORESTFRAMEWORK
@api_view(['GET'])
def tweet_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    serializer = TweetSerializer(qs, many=True)

    return Response(serializer.data)






# PURE DJANGO USES FORMS.PY FILE

# VIEW FOR CREATING (POST) A TWEET 
def tweet_create_view_pure_django(request, *args, **kwargs):
    """
    REST API CREATE VIE -> Django Rest Framework
    """
    # Check for authenticated user
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({}, status=401)
        return redirect('settings.LOGIN_URL')

    #print("ajax", request.is_ajax())
    # POST TWEET FROM Home.html FORM
    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next") or None     # "next" comes from form on home.html
    if form.is_valid():                         # if form is valid save, if it is not valid the page will render that
        obj = form.save(commit = False)
        # do other form related logic
        obj.user = user
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
def tweet_list_view_pure_django(request, *args, **kwargs):
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
def tweet_detail_view_pure_django(request, tweet_id, *args, **kwargs):
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
    