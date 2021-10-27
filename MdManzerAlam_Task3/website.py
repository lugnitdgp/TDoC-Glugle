from flask import Flask,render_template,request,redirect,url_for
from pymongo import MongoClient
from flask_paginate import Pagination, get_page_args

app = Flask(__name__)
# app.debug = True

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/results/")
def result():
    client = MongoClient('localhost',27017)
    database = client.gluggle
    collection = database.queries
    search_string = request.args.get('query')
    print(search_string)
    search_result = []
    required = []
    search_result = collection.find(
        {"$text": {"$search": search_string, '$caseSensitive': False}})
    for object in search_result:
        exist = False
        for result in required:
            if result['title'] == object['title'] or result['url'] == object['url']:
                exist = True

                break

        if exist == False:
            required.append(object)
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    total = len(required)

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