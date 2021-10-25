from flask import Flask, request, render_template, url_for
from flask_paginate import Pagination, get_page_args
import pymongo

app = Flask(__name__)

docs = []
query = {'query': '', 'total_results': 0}
RESULTS_PER_PAGE = 5

def get_users(users, offset, per_page):
    return users[offset: offset + per_page]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods = ['GET','POST'])
def results():
    if request.method == 'POST':
        search_query = (str)(request.form['search_query'])
        query['query'] = search_query
        connection_url = "mongodb://127.0.0.1:27017/"
        client = pymongo.MongoClient(connection_url)
        db = client.results
        search_results = db.search_results
        results = search_results.find({'$text': {'$search': search_query, '$caseSensitive': False}})
        docs.clear()
        for doc in results:
            docs.append(doc)
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