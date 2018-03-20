from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Post
from PyDictionary import PyDictionary
from .models import Question,Answer,User

###FOR YOUTUBE API
import argparse
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
DEVELOPER_KEY = 'AIzaSyCj9VfJo625SsADDXqX87iyOZhsYTC_MHk'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def courses(request):
    return render(request, 'coursera.html')

def coursera(request):
    print ("here")
    if request.method == 'POST':
        search_id = request.POST.get('textfield', None)
        searchfile = open("C:/Users/spgna/Documents/Django project/Codestrastra_round 0/askmeout/app/HEY.txt", "r")
        courses = {}
        i=0
        for line in searchfile:
            if search_id in line:
                print (line)
                i=i+1
                courses[i] = line
        searchfile.close()
        return render(request, 'coursera.html', {'data': courses.items()})

def posts(request):
    posts = Post.objects.order_by('created_date')
    return render(request, 'post_list.html', {'posts':posts,})


def new_post(request):
    print("yo")
    if request.user.is_authenticated:
        if request.method == "POST":
            author = request.user
            text = request.POST.get('text')
            title = request.POST.get('title')
            post = Post.objects.create(author=author,explanation=text,word=title)
            post.save()
            return redirect('/posts/')
        else:
            return render(request, 'post_add.html')
    else:
        return HttpResponseRedirect('/login')

def searchDef(request):
    if request.method == 'POST':
        search_id = request.POST.get('textfield', None)
        dictionary=PyDictionary()
        dict = dictionary.meaning(search_id)
        post = Post.objects.filter(word = search_id).values()
        selfdict = {}
        for newthing in post:
            print (newthing)
            value = [newthing['explanation']]
            print (newthing['id'])
            name = Post.objects.get(id=newthing['id'])
            key = name.author
            selfdict[key] = value
    return render(request, 'define.html', {'data': dict.items(), 'selfdict': selfdict.items()})


def youtube_search(word):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    q=word,
    part='id,snippet',
    maxResults=5
  ).execute()

  videos = []
  channels = []
  playlists = []
  dict = {}
  appendToID = "https://www.youtube.com/watch?v="
  appendToPlaylistID = "https://www.youtube.com/playlist?list="
  appendToChannelID = "https://www.youtube.com/channel/"
  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
  for search_result in search_response.get('items', []):
    imageUrl = search_result['snippet']['thumbnails']['medium']['url']
    if search_result['id']['kind'] == 'youtube#video':
      videos.append([search_result['snippet']['title'],
                                 appendToID + search_result['id']['videoId'], imageUrl])
    elif search_result['id']['kind'] == 'youtube#channel':
      channels.append([search_result['snippet']['title'],
                                   appendToChannelID + search_result['id']['channelId'], imageUrl])
    elif search_result['id']['kind'] == 'youtube#playlist':
      playlists.append([search_result['snippet']['title'],
                                    appendToPlaylistID + search_result['id']['playlistId'], imageUrl])
  dict = {}
  if(videos!=[]):
    dict['Videos'] = videos
  if(channels!=[]):
    dict['Channels'] = channels
  if(playlists!=[]):
    dict['Playlists'] = playlists
  return (dict)

def search(request):
    if request.method == 'POST':
        search_id = request.POST.get('textfield', None)
        print (search_id)
        dict = youtube_search(search_id)
    return render(request, 'youtube.html', {'data': sorted(dict.items())})

def jargon(request):
    return render(request, 'jargon.html')

def define(request):
    return render(request, 'define.html')

def youtube(request):
    return render(request, 'youtube.html')

def ask(request):
    return render(request, 'ask.html')

def logout_blog(request):
    print ("hi")
    if request.user.is_authenticated:
        logout(request)
        return render(request,'logout.html')
    else:
        return HttpResponseRedirect('/login/')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        name = request.POST.get('name')
        user = User.objects.create(
            first_name = name,
            username = username,
            )
        user.set_password(password)
        user.save()

        user = authenticate(username = username, password = password)
        login(request, user)
        return redirect('/ask/')
    else:
        return render(request,'register.html')   

def login_blog(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username = username, password = password)
        if user :
            if user.is_active:
                login(request,user)
                return redirect('/ask/')
            else:
                return HttpResponse('Disabled Account')
        else:
            return HttpResponse("Invalid Login details.Are you trying to Sign up?")
    else:
        return render(request,'login.html')


# Create your views here.  
######################################################
def questionDetail(request,id):
    #answer = Answer.objects.filter(qid = id)
    answer = Answer.objects.filter(quesid = id)
    question = Question.objects.get(qid = id)            
    #question.answer_set.all()
    print(question)
    return render(request,'questionDetail.html',{'question':question, 'answer':answer})


def sentQues(request):
    if request.method == 'POST':
        quesName = request.POST.get('qname')
        q = Question(name=quesName, uid='0',boolValue='False')
        q.save()
        questions = Question.objects.all()
    return render(request,'forum.html',{'questions':questions})

def sendAns(request,id):
    if request.method == 'POST':
        ansName = request.POST.get('ansname')
        q = Question.objects.get(qid=id)
        print("objectjnekhwuvhewku")
        print(q.qid)
        print(q.boolValue)
        q.boolValue=True
        q.save()
        a = Answer(name=ansName, uid='0', quesid=id,voting=0)
        a.save()
        questions = Question.objects.all()
    return render(request,'forum.html',{'questions':questions})

def questions(request):
    questions = Question.objects.all()
    return render(request,'post_list.html',{'posts': posts})

def forum(request):
    questions = Question.objects.all()
    return render(request, 'forum.html',{'questions':questions})