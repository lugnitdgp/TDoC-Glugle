from flask import Flask, render_template, url_for, request

from flask_paginate import Pagination, get_page_args
import pymongo

app = Flask(__name__)


@app.route("/")
def hello_name():
    return render_template('start.html')


@app.route("/search_results")
def fun():
    client = pymongo.MongoClient("mongodb://127.0.0.1:27017/", connect=False)

    database = client['glugledb']
    search_string = request.args.get('gold')
    search_result = []
    required = []
    search_result = database.results.find(
        {"$text": {"$search": search_string, '$caseSensitive': False}})
    for object in search_result:
        exist = False
        for result in required:
            if result['title'] == object['title'] or result['url'] == object['url']:
                exist = True

                break

        if exist == False:
            # print(dir(object))
            required.append(object)
        # print(required)
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')

    total = len(required)

    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')
    return render_template('results.html',
                           required=required[offset:offset+per_page],
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           search_string=search_string
                           )


if __name__ == '__main__':
    app.run(debug=True)
