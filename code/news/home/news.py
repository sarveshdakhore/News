import requests
from models import *

API_KEY = "2e25cce3b0d0481aab616a68309b885c"
BASE_URL = "https://newsapi.org/v2/top-headlines"

def get_top_stories():
    url = f"{BASE_URL}/top-headlines"
    params = {
        "country": "in",
        "category": "general",
        "apiKey": API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    for article in data['articles']:
        unique_id = f"{article['source']['name']}-{article['author']}-{article['publishedAt']}"
        Story.objects.get_or_create(title=unique_id)
    return data

def get_new_stories():
    url = f"{BASE_URL}/everything"
    params = {
        "country": "in",
        "category": "general",
        "apiKey": API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    for article in data['articles']:
        unique_id = f"{article['source']['name']}-{article['author']}-{article['publishedAt']}"
        Story.objects.get_or_create(title=unique_id)
    return data

def get_best_stories():
    url = f"{BASE_URL}/best-stories"
    params = {
        "country": "in",
        "category": "general",
        "apiKey": API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    for article in data['articles']:
        unique_id = f"{article['source']['name']}-{article['author']}-{article['publishedAt']}"
        Story.objects.get_or_create(title=unique_id)
    return data

def get_india_stories(category):
    params = {
        "country": "in",
        "category": category,
        "apiKey": API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    articles = data["articles"]
    for article in data['articles']:
        unique_id = f"{article['source']['name']}-{article['author']}-{article['publishedAt']}"
        Story.objects.get_or_create(title=unique_id)
    return articles

def search_stories(query):
    url = f"{BASE_URL}/everything"
    params = {
        "q": query,
        "apiKey": API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    for article in data['articles']:
        unique_id = f"{article['source']['name']}-{article['author']}-{article['publishedAt']}"
        Story.objects.get_or_create(title=unique_id)
    return data


print(get_top_stories())