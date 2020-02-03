import praw
import pprint
import urllib
import mechanicalsoup
import re
import omdb
import requests

reddit = praw.Reddit(client_id='',
                     client_secret='',
                     user_agent='',
                     username='Username',
                     password='Password')

subreddit = reddit.subreddit('MovieSuggestions')
comments = subreddit.stream.comments()
br = mechanicalsoup.StatefulBrowser()


def info(fType, x, text):
    for x in range(len(fType)):
        wurl = fType[x].replace(" ", "+")
        newURL = "http://www.omdbapi.com/?t={}&apikey=".format(
            wurl)
        html = requests.get(newURL).text.encode('utf8')
        br.open(newURL)

        title = re.findall(r'(?<="Title":")(.*?)(?=",)', html)
        year = re.findall(r'(?<="Year":")(.*?)(?=",)', html)
        rate = re.findall(r'(?<="Rated":")(.*?)(?=",)', html)
        rating = re.findall(r'(?<="imdbRating":")(.*?)(?=")', html)
        director = re.findall(r'(?<="Director":")(.*?)(?=",)', html)
        summary = re.findall(r'(?<="Plot":")(.*?)(?=",)', html)
        error = re.search(r'(?<="Error":)(.*?)(?=!"})', html)

        if error:
            continue
        else:
            if title[0] == fType[x]:
                print(title[0])
                print(year[0])
                print(rate[0])
                print(rating[0])
                print(director[0])
                print(summary[0])
            else:
                continue


f = 1

for comment in comments:
    try:
        author = str(comment.author)  # Get author
    except AttributeError:  # check if the author has been deleted
        print("Author has been deleted")
        continue

    print("======================================================")
    print("New Comment # " + str(f) + " by " +
          author.encode('utf-8') + "")
    f += 1
    text = str(comment.body.encode('utf-8'))  # Fetch body
    print(text)

    NumMultiWord = re.findall(
        r'([0-9]+(?= [A-Z])(?: [A-Z][a-z]+)+)', text)
    a = len(NumMultiWord)
    info(NumMultiWord, a, text)
    text = re.sub(r'([0-9]+(?= [A-Z])(?: [A-Z][a-z]+)+)', '', text)

    multiWordNum = re.findall(
        r'(?=.*[0-9]+)(?:[A-Z][a-z]*)(?: of the| the| of| a| to| to the| or| and| for the| for a| in the| for| on the| at| and the| from| at the| of a| in)*(?: [0-9]*)', text)
    b = len(multiWordNum)
    info(multiWordNum, b, text)
    text = re.sub(r'(?=.*[0-9]+)(?:[A-Z][a-z]*)(?: of the| the| of| a| to| to the| or| and| for the| for a| in the| for| on the| at| and the| from| at the| of a| in)*(?: [0-9]*)', '', text)

    multiWord = re.findall(
        r'([A-Z][a-z]*(?= [A-Z]*)(?: [A-Z][a-z]*)*)(?: of the| of a | and the| at the| to the| for the| in the| of| a| to| or| and| for a| for| on the| at| from| in)*(?: [A-Z][a-z]*)+', text)
    c = len(multiWord)
    info(multiWord, c, text)
    text = re.sub(r'([A-Z][a-z]*(?= [A-Z]*)(?: [A-Z][a-z]*)*)(?: of the| of a | and the| at the| to the| for the| in the| of| a| to| or| and| for a| for| on the| at| from| in)*(?: [A-Z][a-z]*)+', '', text)

    OneWordNum = re.findall(
        r'([A-Z][a-z]+(?= [0-9]+)(?: [0-9]*))', text)
    d = len(OneWordNum)
    info(OneWordNum, d, text)
    text = re.sub(r'([A-Z][a-z]+(?= [0-9]+)(?: [0-9]*))', '', text)

    NumOneWord = re.findall(
        r'([0-9]*(?= [A-Z][a-z]+)(?: [A-Z][a-z]+))', text)
    e = len(NumOneWord)
    info(NumOneWord, e, text)
    text = re.sub(r'([0-9]*(?= [A-Z][a-z]+)(?: [A-Z][a-z]+))', '', text)

    oneWord = re.findall(r'([A-Z][a-z]+)', text)
    f = len(oneWord)
    info(oneWord, f, text)
