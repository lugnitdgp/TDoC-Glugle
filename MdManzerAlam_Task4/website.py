from flask import Flask,render_template,request,redirect,url_for
from pymongo import MongoClient
from flask_paginate import Pagination, get_page_args
import nltk
import pymongo
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
import os
import string
app = Flask(__name__)
# app.debug = True

@app.route("/")
def home():
    return render_template("index.html")

def search_string_optimizations(search_string):
    # lowercasing the serch_results
    search_string = search_string.lower()

    # remove punctuations from the search_results
    translator = str.maketrans('', '', string.punctuation)
    search_string = search_string.translate(translator)

    # removing stopwords and tokenization from the search_results
    stop_words = set(stopwords.words("english"))
    word_tokens = word_tokenize(search_string)
    filtered_search_string = [
        word for word in word_tokens if word not in stop_words]

    # performing stemming in the search_results
    stemmer = PorterStemmer()
    word_tokens = word_tokenize(search_string)
    stems = [stemmer.stem(word) for word in word_tokens]
    return stems

def sort_rank(required, optimized_res):
    for result in required:
        for word in optimized_res:
            if word in result['title']:
                result['score'] += 2
            else:
                result['score'] += 0
            if word in result['description']:
                result['score'] += 1
            else:
                result['score'] += 0
    print('DONE ! DONE ! DONE')
    return sorted(required, key=lambda result: result['score'], reverse=True)

@app.route("/results/")
def result():
    client = MongoClient('localhost',27017)
    database = client.gluggle
    collection = database.queries
    search_string = request.args.get('query')
    optimized_res = search_string_optimizations(search_string)
    print(search_string)
    search_result = []
    required = []
    search_results = collection.find(
        {
            "$text": {
                "$search": search_string,
                '$caseSensitive': False
            }
        },
        {
            "score": {
                '$meta' : "textScore"
            }
        }). sort(
            [
                ('sort', {'$meta': 'textScore'}),
                ('_id', pymongo.DESCENDING)
            ]
        )

    for object in search_results:
        exist = False
        for result in required:
            if result['title'] == object['title'] or result['url'] == object['url']:
                exist = True
                break

        if exist == False:
            # print(dir(object))
            required.append(object)
        # print(required)

    required = sort_rank(required, optimized_res)

    page, per_page, offset = get_page_args(
        page_parameter='page', per_page_parameter='per_page')
    total = search_results.count()

    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')
    return render_template('result.html',
                           required=required[offset:offset+per_page],
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           q=search_string
                           )

if __name__ == "__main__":
    app.run(debug=True)