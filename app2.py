#cats
import praw
from dotenv import load_dotenv
from os import getenv
from time import sleep
from random import choice
import pickle
import os.path
from flask import Flask, render_template, jsonify, request
import click

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

class Submission:
    def __init__(self, url, title):
        self.url = url
        self.title = title
    def __str__(self):
        return f"Url: {self.url}\nTitle: {self.title}"

outputs = []

def get_cats(subreddit_name):
    """ Returns a list of submission objects, with top submissions from the past 24 hours from subreddit_name"""
    subreddit = reddit.subreddit(subreddit_name)

    for result in subreddit.top(time_filter = "day"):
        url = reddit.submission(result).url
        print(subreddit)
        print(result)
        print(result.title)
        print(url)
        outputs.append(Submission(url, result.title))
    return outputs

DEFAULT_SUBS = ['cats', 'OneOrangeBraincell', 'CatPics', 'CatLoaf', 'C_AT', 
            'IllegallySmolCats', 'Kitten', 'CatsStandingUp', 'Blep', 
            'BlackCats', 'StandardIssueCat']

#submissions = get_cats('CatPics')

filtered_keywords = ["gallery", "v.redd.it", "www.reddit.com"]
for kw in filtered_keywords:
    submissions = [s for s in submissions if kw not in s.url]

print('\n\n\n\n<----------------------------------------------------->\n\n\n\n')

index_length = len(submissions)

#---------------------
# Scraper logic
#---------------------

@click.command()
@click.option("--subs", default=None, help="Explicit list of subreddits to use")
def scrape_config(*args, **kw):
    return ("scrape", args, kw)

def scrape(subs=None):
    """ Scrapes reddit for cat photos """
    if subs is None:
        subs = DEFAULT_SUBS
    outputs = []
    for sub in subs:
        outputs.extend(get_cats(sub))
    with open("cats.pickle", 'wb') as f:
        pickle.dump(outputs, f)

#---------------------
# Serving logic
#---------------------

@click.command()
@click.option("-f", "--filename", default="cats.pickle", help="file containing all the submissions")
@click.option("--port", default=5050, help="port to listen on")
@click.option("--host", default=getenv('HOST-ADDRESS'), help="local host address to listen on")
@click.option("--scrape", default=False, help="if this is set to true, cats.pickle is overwritten. Does not do anything if cats.pickle does not exist")
def serve_config(*args, **kw):
    return ("serve", args, kw)

def serve(filename, port, host, scrape):
    """ Launches a web server that gets random cat image through /api route """

    app = Flask(__name__, static_folder='static')
    
    @app.route("/")
    def index():
        return render_template('index.html')

    @app.route("/api", methods=['GET'])
    def api():
        if(request.method == 'GET'):
            submission = choice(submissions)
            url = submission.url
            title = submission.title
            print('\n\n', title, url,)
            return {'url':url, 'title':title}
    
    # look for the saved submissions file, and if it doesn't exist, then invoke the scraper
    if not os.path.exists(filename) or scrape:
        print("Scraping...")
        scrape()
    
    # load the pickle
    with open(filename, "rb") as f:
        submissions = pickle.load(f)
    print("Loaded", len(submissions), "cat URLs. =^._.^=∫")

    app.run(host = host, port=port)

#---------------------
# Main
#---------------------

@click.group()
def cli(): 
    pass

cli.add_command(serve)
cli.add_command(scrape)

if __name__ == "__main__": 
    cli()