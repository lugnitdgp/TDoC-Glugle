
from flask import Flask, render_template, request
from flask_paginate import Pagination, get_page_args
import pymongo
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
import requests
import json
import random


app = Flask(__name__)

@app.route('/')
def home():
    quote = get_quote()
    return render_template('home.html',quote=quote)


@app.route('/search_results')
def search_results():
    connect_url = 'mongodb://127.0.0.1:27017/'
    client = pymongo.MongoClient(connect_url, connect=False)
    db = client.results

    search_string = request.args.get('search')
    res = clean(search_string)
    print(res1 := ' '.join(str(e) for e in res))

    query = db.search_results.find(
        {'$text': {'$search': res1, '$caseSensitive': False}},
        {'score': {
                '$meta': "textScore"}}).sort(
        [
            ('score', {'$meta': 'textScore'}),
            ('_id', pymongo.DESCENDING)
        ])
    print("query is ****** " , query)

    search_result = []

    for doc in query:
        # print(doc)
        exist = False
        for result in search_result:

            if result['title'] == doc['title'] or result['url'] == doc['url']:
                exist = True
                break

        if exist == False:
            search_result.append(doc)

    point_result = search_result
    print(type(point_result) )   

    for one_doc in search_result:
        for key , value in one_doc.items():
            print(key , "&&&&&&&&&&&&&" , value)
        break        

    var =  rank_algo(search_result, res1)
    print(var)

    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')

    total = len(search_result)
    # changewall()

    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')

    return render_template('result.html',
                           search_result=search_result[offset:offset+per_page],
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           search_string=search_string,
                           myurl = usr_url
                           )


def clean(search_string): 
    search_clean = search_string.lower()
    translator = str.maketrans('', '', string.punctuation)
    search_clean = search_clean.translate(translator)
    stop_words = set(stopwords.words("english"))
    search_clean = word_tokenize(search_clean)
    print(search_clean)
    search_clean = [word for word in search_clean if word not in stop_words]
    stemmer = PorterStemmer()
    print(search_clean)
    search_clean = [stemmer.stem(word) for word in search_clean]
    return search_clean

def rank_algo(search_result, keywords):
    for result in search_result:
        for word in keywords:
            if word in result['title']:
                result['score'] += 2
            else:
                result['score'] += 0
            if word in result['description']:
                result['score'] += 1
            else:
                result['score'] += 0
    return sorted(search_result, key = lambda result: result['score'], reverse=True)

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote= json_data[0]['q']+ ' ---' + json_data[0]['a']
  return(quote)

@app.route('/changewall')
def changewall():
    print('hello')
    global usr_url 
    # usr_url=" "
    usr_url = request.args.get('userurl')
    return render_template('changewall.html', myurl=usr_url)

if __name__ == '__main__':
    app.run(debug=True)
