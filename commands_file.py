import praw
from dotenv import load_dotenv
from os import getenv, rename
from time import sleep
from datetime import datetime
from random import choice
import pickle
import os.path
from flask import Flask, render_template, jsonify, request

class Submission:
    def __init__(self, url, title):
        self.url = url
        self.title = title
    def __str__(self):
        return f"Url: {self.url}\nTitle: {self.title}"

load_dotenv()

filtered_keywords = ["v.redd.it", "www.reddit.com"]

client_id = 'sRQE896lrpoIOE7Z4xbb6g'
redirect_uri = 'http://localhost:8080'
client_secret = getenv('SECRET')
user_agent = getenv('USER-AGENT')
password=getenv('PASSWORD')
username=getenv('REDDIT-USERNAME')
filtered_keywords = ["v.redd.it", "www.reddit.com"]

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    password=password,
    user_agent=user_agent,
    username=username
)

default_subs = ['cats', 'OneOrangeBraincell', 'CatPics', 'CatLoaf', 'C_AT', 
            'IllegallySmolCats', 'Kitten', 'CatsStandingUp', 'Blep', 
            'BlackCats', 'StandardIssueCat']

def scrapename(subs=None, limit=None, nobackup=False):
    """ Scrapes reddit for cat photos """


    if limit != None:
        limit = int(limit)

    if subs is None:
        subs = default_subs
    else:
        subs = subs.split(',')


    
    if limit:
        kittehs = set()
        for sub in subs:
            remaining = limit

            results = get_cats(sub, remaining)
            for kw in filtered_keywords:
                results = [s for s in results if kw not in s.url]
            remaining -= len(results)
            kittehs.update(results)

            if len(kittehs) <= 0:
                break

    else:
        kittehs = set()
        for sub in subs:
            results = get_cats(sub, None)
            for kw in filtered_keywords:
                results = [s for s in results if kw not in s.url]
            kittehs.update(results)


    if limit and len(kittehs) > limit:
        subtraction_amount = len(kittehs) - limit
        for i in range(subtraction_amount):
            kittehs.pop()
            print(f"{i+1} kittehs popped")

    print("\n\n>>>> Scraped", len(kittehs), "good kittehs <<<<\n")

    for kitteh in kittehs:
        print(kitteh.title)

    if not nobackup:
        #rename file to time and date (with local time)
        backup_time = datetime.now().strftime("%Y-%m-%d-%H-%M")
        print(backup_time)
        #move file to pickle_backups
        rename('cats.pickle', f"pickle_backups/{backup_time}.pickle")
        print('moved pickle')
    
    with open('cats.pickle', 'wb') as f:
        pickle.dump(kittehs, f)

def get_cats(subreddit_name, limit=None):
    """ Returns a list of submission objects, with top submissions from the past 24 hours from subreddit_name
    If **limit** is provided, then returns no more then that many items"""
    subreddit = reddit.subreddit(subreddit_name)

    output = set()

    for result in subreddit.top(time_filter = "day", limit=limit):
        url = reddit.submission(result).url
        print(subreddit)
        print(result)
        print(result.title)
        print(url)
        if filtered_keywords[0] not in url and filtered_keywords[1] not in url:
            output.add(Submission(url, result.title))
    print(type(output))
    print(len(output))
    return output

def servename(port, host, scrape_subs): #MUST NOT BE PLAIN "scrape", that breaks things
    """ Launches a web server that gets random cat image through /api route """

    app = Flask(__name__, static_folder='static')
    
    @app.route("/")
    def index():
        return render_template('index.html')

    @app.route("/api", methods=['GET'])
    def api():
        if(request.method == 'GET'):
            submission = choice(list(submissions))
            url = submission.url
            title = submission.title
            print('\n\n', title, url,)
            return {'url':url, 'title':title}
    
    # look for the saved submissions file, and if it doesn't exist, then invoke the scraper
    if not os.path.exists('cats.pickle') or scrape_subs:
        print("Scraping...")
        scrape_function()
    
    # load the pickle
    with open('cats.pickle', "rb") as f:
        submissions = pickle.load(f)
    print("Loaded", len(submissions), "cat URLs. =^._.^=∫")

    app.run(host = host, port=port)