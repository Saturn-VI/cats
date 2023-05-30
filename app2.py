#cats
import praw
from dotenv import load_dotenv
from os import getenv, rename
from time import sleep
from datetime import datetime
from random import choice
import pickle
import os.path
from flask import Flask, render_template, jsonify, request
import click
from commands_file import servename, scrapename

default_subs = ['cats', 'OneOrangeBraincell', 'CatPics', 'CatLoaf', 'C_AT', 
            'IllegallySmolCats', 'Kitten', 'CatsStandingUp', 'Blep', 
            'BlackCats', 'StandardIssueCat']

print('\n\n\n\n<----------------------------------------------------->\n\n\n\n')

#---------------------
# Scraper logic
#---------------------

@click.command()
@click.option("--subs", default=None, help="Explicit list of subreddits to use. Format: subreddit1,subreddit2,subreddit3, etc. NO SPACES.")
# @click.option("-f", "--filename", default="cats.pickle", help="filename to save submissions to [DEPRECATED]")
@click.option("-l", "--limit", default=None, help="Maximum number of submissions to get. Collects this amount from each sub in --subs")
@click.option("--nobackup", default=False, help="Don't create backup of existing pickle before overwriting it")
def scrape(subs, limit, nobackup):
    return scrapename(subs, limit, nobackup)

    

#---------------------
# Serving logic
#---------------------

@click.command()
# @click.option("-f", "--filename", default="cats.pickle", help="file containing all the submissions") obsolete at the moment due to line 71
@click.option("--port", default=5050, help="port to listen on")
@click.option("--host", default=getenv('HOST-ADDRESS'), help="local host address to listen on")
@click.option("--scrape_subs", default=True, help="if this is set to false, old cats.pickle is used and scrape() is not called (this flag has no effect on first run)")
def serve(port, host, scrape_subs): #MUST NOT BE PLAIN "scrape", that breaks things
    servename(port, host, scrape_subs)



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
