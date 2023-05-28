#cats
import praw
from dotenv import load_dotenv
from os import getenv
from time import sleep
from random import randint

load_dotenv()

client_id = 'sRQE896lrpoIOE7Z4xbb6g'
redirect_uri = 'http://localhost:8080'
client_secret = getenv('SECRET')
user_agent = getenv('USER-AGENT')
password=getenv('PASSWORD')
username=getenv('REDDIT-USERNAME')

reddit = praw.Reddit(
    client_id='sRQE896lrpoIOE7Z4xbb6g',
    client_secret=getenv('SECRET'),
    password=getenv('PASSWORD'),
    user_agent=getenv('USER-AGENT'),
    username=getenv('REDDIT-USERNAME')
)

subreddits = ['cats', 'OneOrangeBraincell', 'CatPics', 'CatLoaf']

def get_cats():
    subreddit_choice = subreddits[randint(0, 3)]
    subreddit = reddit.subreddit(subreddit_choice)

    submissions = []
    submission_titles = []
    submission_ids = []

    for submission in subreddit.top(time_filter = "day"):
        filtered_submission = reddit.submission(submission).url
        print(subreddit)
        print(submission)
        print(submission.title)
        print(filtered_submission)
        submissions.append(filtered_submission)
        submission_titles.append(submission.title)
        submission_ids.append(submission)

    index_length = randint(0,len(submissions)-1)
    print(index_length)
    print(submissions)
    print(submission_ids)
    print(submission_titles)


while (1):
    
    get_cats()

    input()