#cats
import praw
from dotenv import load_dotenv
from os import getenv
from time import sleep
from random import choice
from flask import Flask, render_template, jsonify, request

load_dotenv()

client_id = 'sRQE896lrpoIOE7Z4xbb6g'
redirect_uri = 'http://localhost:8080'
client_secret = getenv('SECRET')
user_agent = getenv('USER-AGENT')
password=getenv('PASSWORD')
username=getenv('REDDIT-USERNAME')

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    password=password,
    user_agent=user_agent,
    username=username
)

submissions = [] 

class Submission:
    def __init__(self, url, title):
        self.url = url
        self.title = title
    def __str__(self):
        return f"Url: {self.url}\nTitle: {self.title}"

def get_cats(subreddit_name):
    
    subreddit = reddit.subreddit(subreddit_name)

    for result in subreddit.top(time_filter = "day"):
        url = reddit.submission(result).url
        print(subreddit)
        print(result)
        print(result.title)
        print(url)
        submissions.append(Submission(url, result.title))

app = Flask(__name__, static_folder='static')

cat_subs = ['cats', 'OneOrangeBraincell', 'CatPics', 'CatLoaf', 'C_AT', 
            'IllegallySmolCats', 'Kitten', 'CatsStandingUp', 'Blep', 
            'BlackCats', 'StandardIssueCat']

get_cats('CatPics')

filtered_keywords = ["gallery", "v.redd.it", "www.reddit.com"]
for kw in filtered_keywords:
    submissions = [s for s in submissions if kw not in s.url]

print('\n\n\n\n<----------------------------------------------------->\n\n\n\n')

index_length = len(submissions)

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/api", methods=['GET'])
def api():
    if(request.method == 'GET'):
        submission = choice(submissions)
        url = submission.url
        title = submission.title
        print('\n\n', title, url,)
        return {'url':url, 'title':title}

if __name__ == "__main__":
    app.run(host = getenv('HOST-ADDRESS'), port = 5050)
