from flask import Flask, render_template, request, redirect, url_for
from flask_paginate import Pagination, get_page_args
import pymongo
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer


app = Flask(__name__)
client = pymongo.MongoClient("mongodb://127.0.0.1:27017")
db = client.glugledb
query_data = db.query_data


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        query = request.form['query']
        return redirect(url_for("search", query=query))

    return render_template("index.html")


def get_paginated_search_results(search_results, offset=0, per_page=10):
    return search_results[offset: offset + per_page]


def get_query_keywords(query):
    # lowercasing
    query = query.lower()

    # remove punctuations
    translator = str.maketrans('', '', string.punctuation)
    query = query.translate(translator)
    
    # removing stopwords and tokenization
    stop_words = set(stopwords.words("english"))
    word_tokens = word_tokenize(query)
    filtered_query = [word for word in word_tokens if word not in stop_words]

    # perform stemming
    stemmer = PorterStemmer()
    word_tokens = word_tokenize(query)
    stems = [stemmer.stem(word) for word in word_tokens]
    return stems


def query_database(query):
    return db.query_data.find(
        {
            '$text' : {
                '$search' : query,
                '$caseSensitive' : False,
            }
        },
        {
            'score': {
                '$meta': "textScore"
            }
        }
    ).sort(
        [
            ('score', {'$meta': 'textScore'}),
            ('_id', pymongo.DESCENDING)
        ]
    )


def remove_duplicates(result_data):
    search_results = []
    for doc in result_data:
        exist = False
        for result in search_results:
            if result['title'] == doc['title'] or result['url'] == doc['url']:
                exist = True
                break

        if exist == False:
            search_results.append(doc)
    return search_results


def sort_rank(search_results, keywords):
    for result in search_results:
        for word in keywords:
            if word in result['title']:
                result['score'] += 2
            else:
                result['score'] += 0
            if word in result['description']:
                result['score'] += 1
            else:
                result['score'] += 0
    return sorted(search_results, key = lambda result: result['score'], reverse=True)


@app.route("/search")
def search():

    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')

    query = request.args.get('query', "")
    search_results = []

    # preprocess query
    keywords = get_query_keywords(query)
    processed_query = " ".join(keywords)

    # search for data in database
    search_results = query_database(processed_query)

    # filter out duplicate search results
    search_results = remove_duplicates(search_results)

    # rank the retrieved search results
    search_results = sort_rank(search_results, keywords)

    # find total no of search results
    total = len(search_results)

    # paginate the search results
    pagination = Pagination(page=page,
                            total=total,
                            css_framework='bootstrap4',
                            per_page=per_page,
                            format_total=True,
                            format_number=True,
                            record_name='results',
                            alignment='center')

    return render_template("search.html",
                            query=query,    
                            search_results=get_paginated_search_results(search_results, offset, per_page),
                            total=total,
                            pagination=pagination
                            )