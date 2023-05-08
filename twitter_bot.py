import tweepy
import os
from dotenv import load_dotenv
load_dotenv()
# Twitter API credentials
bearer_token =os.getenv("bearer_token")
consumer_key = os.getenv("consumer_key")
consumer_secret = os.getenv("consumer_secret")
access_token = os.getenv("access_token")
access_token_secret = os.getenv("access_token_secret")
print(consumer_key)
print(type(consumer_key))

client = tweepy.Client(bearer_token,consumer_key,consumer_secret, access_token,access_token_secret)
def post_tweet(text):
    post = client.create_tweet(text=text)
    return post

def my_details():
    me=client.get_me()
    return me 

print(my_details())


