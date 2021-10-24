from flask import Flask, render_template, request, redirect, url_for
from flask_paginate import Pagination, get_page_args
import pymongo

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


@app.route("/search")
def search():

    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')

    query = request.args.get('query', "")
    search_results = []

    result_data = db.query_data.find(
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

    for doc in result_data:
        exist = False
        for result in search_results:
            if result['title'] == doc['title'] or result['url'] == doc['url']:
                exist = True
                break

        if exist == False:
            search_results.append(doc)

    # search_results = db.query_data.find(
    #     {
    #         '$text' : {
    #             '$search' : query,
    #             '$caseSensitive' : False,
    #         }
    #     },
    #     {
    #         'score': {
    #             '$meta': "textScore"
    #         }
    #     }
    # ).sort(
    #     [
    #         ('score', {'$meta': 'textScore'}),
    #         ('_id', pymongo.DESCENDING)
    #     ]
    # ).skip(offset).limit(per_page)


    total = len(search_results)

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