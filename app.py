#cats
import praw
from dotenv import load_dotenv
from os import getenv
from time import sleep
from random import randint
from flask import Flask, render_template, jsonify, request

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

submissions = []
submission_titles = []
submission_ids = []

def get_cats(subreddit_choice):
    if subreddit_choice == '':
        subreddit_choice = subreddits[randint(0, 3)]    
    subreddit = reddit.subreddit(subreddit_choice)

    #submissions = []
    #submission_titles = []
    #submission_ids = []

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
    #print(index_length)
    #print(submissions)
    #print(submission_ids)
    #print(submission_titles)

    for i in range (10):
        print('')


app = Flask(__name__, static_folder='static')

#get_cats('cats')
#get_cats('OneOrangeBraincell')
get_cats('CatPics')
#get_cats('CatLoaf')
submission_ids = []
    
index_length = len(submissions)

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/api", methods=['GET'])
def api():
    if(request.method == 'GET'):
        random_number = randint(0, ((index_length)))
        print(index_length)
        print(len(submissions))
        submission_choice = submissions[random_number]
        submission_title_choice = submission_titles[random_number]
        return jsonify({'URL':submission_choice, 'TITLE':submission_title_choice})


if __name__ == "__main__":
    app.run(host = '127.0.0.1', port = 5050)