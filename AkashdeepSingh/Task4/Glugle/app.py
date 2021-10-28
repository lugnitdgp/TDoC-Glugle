from flask import Flask, request, render_template, url_for
from flask_paginate import Pagination, get_page_args
import pymongo, string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from operator import itemgetter

app = Flask(__name__)

RESULTS_PER_PAGE = 5

def get_users(users, offset, per_page):
    return users[offset: offset + per_page]

def query_preprocessing(query):
    query = query.lower()
    translator = str.maketrans('', '', string.punctuation)
    query = query.translate(translator)
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(query)
    fitered_text = [word for word in word_tokens if word not in stop_words]
    query = ' '.join(fitered_text)
    word_tokens = word_tokenize(query)
    stemmer = PorterStemmer()
    stems = [stemmer.stem(word) for word in word_tokens]
    query = ' '.join(stems)

    return query

def rank_search_results(results, keywords):
    docs = []
    for doc in results:
        docs.append(doc)
    for doc in docs:
        doc['score'] = 0
    for keyword in keywords:
        for doc in docs:
            doc['score'] += 2 * doc['title'].lower().count(keyword)
            doc['score'] += 1 * doc['description'].lower().count(keyword)

    docs = sorted(docs, key = itemgetter('score'), reverse = True)

    return docs
    

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results')
def results():
    search_query = request.args.get('search_query')
    query = {}
    query['query'] = search_query
    search_query = query_preprocessing(search_query)
    keywords = word_tokenize(search_query)
    connection_url = "mongodb://127.0.0.1:27017/"
    client = pymongo.MongoClient(connection_url)
    db = client.results
    search_results = db.search_results
    results = search_results.find({'$text': {'$search': search_query, '$caseSensitive': False}})
    #docs.clear()
    docs = rank_search_results(results, keywords)
    # for doc in results:
    #     docs.append(doc)
    query['total_results'] = len(docs)
        
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    per_page = RESULTS_PER_PAGE;
    offset = (page - 1) * per_page
    total = len(docs)
    pagination_users = get_users(docs, offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')
    return render_template('results.html',
                           users=pagination_users,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           docs = docs,
                           query = query
                           )

if __name__ == '__main__':
    app.run(debug = True)