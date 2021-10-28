
from flask import Flask, render_template, request
from flask_paginate import Pagination, get_page_args
import pymongo
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/search_results')
def search_results():
    connect_url = 'mongodb://127.0.0.1:27017/'
    client = pymongo.MongoClient(connect_url, connect=False)
    db = client.results

    search_string = request.args.get('search')
    res = clean(search_string)
    print(res1 := ' '.join(str(e) for e in res))

    query = db.search_results.find(
        {'$text': {'$search': res1, '$caseSensitive': False}})
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
        for key , value in one_doc:
            print(one_doc[key] , "&&&&&&&&&&&&&" , one_doc[value])
        break        



    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')

    total = len(search_result)


    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')

    return render_template('result.html',
                           search_result=search_result[offset:offset+per_page],
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           search_string=search_string
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


if __name__ == '__main__':
    app.run(debug=True)
