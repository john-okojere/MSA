# chatbot_service.py

import torch
from transformers import BertTokenizer, BertForSequenceClassification
import nltk
import string
import random
import os
from django.conf import settings

# Ensure that the directory exists
model_dir = os.path.join(settings.BASE_DIR, 'chat/fine_tuned_bert')

# Initialize BERT and tokenizer
model = BertForSequenceClassification.from_pretrained(model_dir)
tokenizer = BertTokenizer.from_pretrained(model_dir)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Load dataset
dataset_path = os.path.join(settings.BASE_DIR, 'data', 'Dataset.txt')
with open(dataset_path, 'r', errors='ignore') as f:
    raw_doc = f.read()

nltk.download('punkt')
sentence_tokens = nltk.sent_tokenize(raw_doc)

# Text preprocessing
lemmer = nltk.stem.WordNetLemmatizer()

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

remove_punc_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punc_dict)))

# Response generation
def response(user_response):
    MySava_response = ''
    sentence_tokens.append(user_response)
    encodings = tokenizer(sentence_tokens, truncation=True, padding=True, max_length=512, return_tensors='pt')
    inputs = encodings['input_ids'].to(device)
    attention_mask = encodings['attention_mask'].to(device)
    outputs = model(inputs, attention_mask=attention_mask)
    predictions = torch.argmax(outputs.logits, dim=-1)
    
    idx = predictions[-1].item()  # Get the index of the closest sentence
    sentence_tokens.pop()
    
    if predictions[-1].item() == 0:  # Adjust based on your label logic
        MySava_response = "I am sorry. Unable to understand you! Can you come again?"
    else:
        MySava_response = sentence_tokens[idx]
    
    return MySava_response

def get_chatbot_response(user_input):
    if user_input.lower() in ['bye', 'exit', 'quit']:
        return "Goodbye!"
    if user_input.lower() in ['thanks', 'thank you']:
        return "You are welcome!"
    if greet(user_input):
        return greet(user_input)
    return response(user_input)

# Greetings
greet_inputs = ('hello', 'hi', 'hey', 'whassup', 'how are you?', 'hello', 'hi', 'hey', 'whassup', 'how are you?')
greet_responses = ['Hi', 'Hey', 'Hey There!', 'Hello']

def greet(sentence):
    for word in sentence.split():
        if word.lower() in greet_inputs:
            return random.choice(greet_responses)
    return None
