from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Chat, Message
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import os
import random
import nltk
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.conf import settings
from authentication.models import User
from .nlp_model import *


@login_required
def home(request):
    chats = Chat.objects.filter(user=request.user).order_by('-created')
    return render(request, "chat/index.html", {'chats': chats})

def welcome(request):
    return render(request, "auth/gs.html")

@csrf_exempt
def create_chat(request):
    if request.method == 'POST':
        text = request.POST.get('text', '')
        if text:
            chat = Chat.objects.create(user=request.user, title=text[:50])
            Message.objects.create(chat=chat, user=request.user, text=text)

            bot, created  = User.objects.get_or_create(email="bot@bot.com", password="botforwhat")
            
            # Simulate a bot response        
            bot_response = get_chatbot_response(text)
            Message.objects.create(chat=chat, user= bot, text=bot_response)
            
            return JsonResponse({'status': 'success', 'chat_id': chat.uid, 'response': bot_response})
        return JsonResponse({'status': 'error', 'message': 'No text provided'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

# @csrf_exempt
# def create_chat(request):
#     if request.method == 'POST':
#         text = request.POST.get('text', '')
#         if text:
#             chat = Chat.objects.create(user=request.user, title=text[:30])
#             Message.objects.create(user=request.user, chat=chat, text=text)
#             return JsonResponse({'status': 'success', 'chat_id': chat.uid, 'title': text[:30]})
#     return JsonResponse({'status': 'error', 'message': 'Invalid request'})

# @csrf_exempt
# def add_message(request, chat_id):
#     if request.method == 'POST':
#         text = request.POST.get('text', '')
#         if text:
#             chat = get_object_or_404(Chat, uid=chat_id)
#             Message.objects.create(user=request.user, chat=chat, text=text)
#             if greet(text):
#                 return JsonResponse({'response': greet(text)})
#             else:
#                 sentence_tokens.append(text)
#                 word_tokens.extend(nltk.word_tokenize(text))
#                 bot_response = response(text)
#                 sentence_tokens.remove(text)
#             return JsonResponse({'status': 'success', 'response': bot_response})
#     return JsonResponse({'status': 'error', 'message': 'Invalid request'})


@csrf_exempt
def add_message(request, chat_id):
    if request.method == 'POST':
        chat = get_object_or_404(Chat, uid=chat_id)
        text = request.POST.get('text', '')
        if text:
            Message.objects.create(chat=chat, user=request.user, text=text)

            # Simulate a bot response
            bot_response = get_chatbot_response(text)
            bot, created  = User.objects.get_or_create(email="bot@bot.com", password="botforwhat")
            
            # Save bot response to the database
            Message.objects.create(chat=chat, user=bot, text=bot_response)
            
            return JsonResponse({'status': 'success', 'response': bot_response})
        return JsonResponse({'status': 'error', 'message': 'No text provided'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def chat_view(request, chat_id):
    chats = Chat.objects.filter(user=request.user).order_by('-created')
    chat = get_object_or_404(Chat, uid=chat_id)
    messages = Message.objects.filter(chat=chat).order_by('-created')
    return render(request, 'chat/index.html', {'chats': chats, 'chat': chat, 'messages': messages})
