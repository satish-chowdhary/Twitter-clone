from django.shortcuts import render, redirect
import random
from django.conf import settings
from django.utils.http import is_safe_url
from django.http import HttpResponse, Http404, JsonResponse
from .models import Tweet
from .forms import TweetForm

ALLOWED_HOSTS = settings.ALLOWED_HOSTS
# Create your views here.

def home_view(request, *args, **kwargs):
    return render(request, 'pages/home.html')

def tweet_create_view(request, *args, **kwargs):
    form = TweetForm(request.POST or None)
    next_url = request.POST.get('next') or None
    if form.is_valid():
        obj = form.save(commit = False)
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status = 201)
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()
    return render(request, 'components/form.html', context={"form": form})

def tweets_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    tweets_list = [x.serialize() for x in qs]
    data = {
        "response" : tweets_list
    }
    return JsonResponse(data)

def home_detail_view(requests, tweet_id, *args, **kwargs):
    data = {
        "id":tweet_id,
    }
    status = 200
    try:
        obj = Tweet.objects.get(id = tweet_id)
        data ["content"] = obj.content
    except:
        data['message '] = "Not found"
        status = 404
    return JsonResponse(data, status = status)