#cats
import praw
from dotenv import load_dotenv
from os import getenv

load_dotenv()

client_id = 'sRQE896lrpoIOE7Z4xbb6g'
redirect_uri = 'http://localhost:8080'
client_secret = getenv('SECRET')
user_agent = getenv('USER-AGENT')
password=getenv('PASSWORD')
username=getenv('USERNAME')

reddit = praw.Reddit(
    client_id='sRQE896lrpoIOE7Z4xbb6g',
    client_secret=getenv('SECRET'),
    password=getenv('PASSWORD'),
    user_agent=getenv('USER-AGENT'),
    username=getenv('USERNAME')
)