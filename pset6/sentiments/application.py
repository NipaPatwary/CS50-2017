from flask import Flask, redirect, render_template, request, url_for

import os
import sys
import nltk

import helpers
from analyzer import Analyzer

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():

    # validate screen_name
    screen_name = request.args.get("screen_name", "")
    if not screen_name:
        return redirect(url_for("index"))

    # get screen_name's tweets
    tweets = helpers.get_user_timeline(screen_name)
    if tweets == None:
        return redirect(url_for("index"))

    # absolute paths to lists
    positives = os.path.join(sys.path[0], "positive-words.txt")
    negatives = os.path.join(sys.path[0], "negative-words.txt")

    # instantiate analyzer
    analyzer = Analyzer(positives, negatives)

    # define tokenizer
    tokenizer = nltk.tokenize.TweetTokenizer()

    # tokenize every tweet, analyze every word (token)
    # and calculate percent of positive, negative and neutral tweets
    positive, negative, neutral = 0.0, 0.0, 0.0

    for tweet in tweets:
        total = 0
        tokens = tokenizer.tokenize(tweet)

        for token in tokens:
            score = analyzer.analyze(token)
            total += score

        if total > 0:
            positive += 1
        elif total < 0:
            negative += 1
        else:
            neutral += 1

    # generate chart
    chart = helpers.chart(positive, negative, neutral)

    # render results
    return render_template("search.html", chart=chart, screen_name=screen_name)
