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
filtered_keywords = ["v.redd.it", "www.reddit.com"]

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

def get_cats(subreddit_name, limit=None):
    """ Returns a list of submission objects, with top submissions from the past 24 hours from subreddit_name
    If **limit** is provided, then returns no more then that many items"""
    subreddit = reddit.subreddit(subreddit_name)

    for result in subreddit.top(time_filter = "day", limit=limit):
        url = reddit.submission(result).url
        print(subreddit)
        print(result)
        print(result.title)
        print(url)
        if filtered_keywords[0] not in url and filtered_keywords[1] not in url:
            outputs.append(Submission(url, result.title))
    return outputs


DEFAULT_SUBS = ['cats', 'OneOrangeBraincell', 'CatPics', 'CatLoaf', 'C_AT', 
            'IllegallySmolCats', 'Kitten', 'CatsStandingUp', 'Blep', 
            'BlackCats', 'StandardIssueCat']

print('\n\n\n\n<----------------------------------------------------->\n\n\n\n')

#---------------------
# Scraper logic
#---------------------

@click.command()
@click.option("--subs", default=None, help="Explicit list of subreddits to use")
@click.option("-f", "--filename", default="cats.pickle", help="filename to save submissions to")
@click.option("-l", "--limit", default=None, help="Maximum number of submissions to get, is occasionally 1-6 submissions over the limit")
@click.option("--nobackup", default=False, help="Don't create backup of existing pickle before overwriting it")
def scrape(subs, filename, limit, nobackup):
    """ Scrapes reddit for cat photos """
    limit = int(limit)
    if subs is None:
        subs = DEFAULT_SUBS
    kittehs = []
    
    kittycounts = 0  # running total of how many cats we've grabbed
    for sub in subs:
        if limit:
            newlist = get_cats(sub, limit-kittycounts)
        else:
            newlist = get_cats(sub)
        kittehs.extend(newlist)
        kittycounts += len(newlist)
        if kittycounts >= limit:
            break
    
    
    for kw in filtered_keywords:
        goodkittehs = [s for s in kittehs if kw not in s.url]

    print("\n\n>>>> Scraped", len(goodkittehs), "good kittehs <<<<\n")

    if not nobackup:
        pass
    
    with open(filename, 'wb') as f:
        pickle.dump(goodkittehs, f)
        
    

#---------------------
# Serving logic
#---------------------

@click.command()
@click.option("-f", "--filename", default="cats.pickle", help="file containing all the submissions")
@click.option("--port", default=5050, help="port to listen on")
@click.option("--host", default=getenv('HOST-ADDRESS'), help="local host address to listen on")
@click.option("--scrape", default=False, help="if this is set to true, cats.pickle is overwritten. Does not do anything if cats.pickle does not exist")
def serve(*args, **kw):
    return ("serve", args, kw)

def do_serve(filename, port, host, scrape):
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
