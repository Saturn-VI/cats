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

class Submission:
    def __init__(self, url, title):
        self.url = url
        self.title = title
    def __str__(self):
        return f"Url: {self.url}\nTitle: {self.title}"

def get_cats(subreddit_choice):
    if subreddit_choice == '':
        subreddit_choice = subreddits[randint(0, 3)]    
    subreddit = reddit.subreddit(subreddit_choice)

    for result in subreddit.top(time_filter = "day"):
        url = reddit.submission(result).url
        print(subreddit)
        print(result)
        print(result.title)
        print(url)
        submission = Submission(url, result.title)
        submissions.append(submission)

    index_length = randint(0,len(submissions)-1)


app = Flask(__name__, static_folder='static')

#get_cats('cats')
#get_cats('OneOrangeBraincell')
get_cats('CatPics')
#get_cats('CatLoaf')

submissions = [s for s in submissions if 'gallery' not in s.url]

print('\n\n\n\n<----------------------------------------------------->\n\n\n\n')

for submission in submissions:
    print(submission)

index_length = len(submissions)

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/api", methods=['GET'])
def api():
    if(request.method == 'GET'):
        random_number = randint(0, ((index_length)-1))
        submission_url_choice = submissions[random_number].url
        submission_title_choice = submissions[random_number].title
        print('\n\n')
        print(submission_title_choice)
        print(submission_url_choice)
        return {'url':submission_url_choice, 'title':submission_title_choice}


if __name__ == "__main__":
    app.run(host = getenv('HOST-ADDRESS'), port = 5050)
