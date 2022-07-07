from flask import Flask, render_template, request
from flask_paginate import Pagination, get_page_args
import pymongo

app = Flask(__name__)

@app.route('/')
def entry():
  return render_template('home.html')

@app.route('/search_results/')
def search_results():
  connect_url = "mongodb+srv://goofynugtz:1two3456@glugle.l17hyjv.mongodb.net/test"
  client = pymongo.MongoClient(connect_url)

  db = client.glugle

  search_string = request.args.get('search')

  # print("\n\n\nSearch: ", search_string)

  query = []
  query = db.search_results.find(
    {'$text': {'$search': search_string, '$caseSensitive': False}}
  )

  print("\n\nQuery: ", query[0])

  search_result = []

  for doc in query:
    exist = False
    for result in search_result:
      if result['title'] == doc['title'] or result['url'] == doc['url']:
        exist = True
        break

    if exist == False:
      search_result.append(doc)
  print("\n\nSearch: ", search_result)

  page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')

  total = len(search_result)

  pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')


  return render_template('search.html', 
    search_result = search_result[offset:offset + per_page],
    page=page,
    per_page=per_page,
    pagination=pagination,
    search_string=search_string
  )


if __name__ == '__main__':
  app.run(debug=True)