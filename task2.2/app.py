from flask import Flask, render_template, request
import pymongo


app = Flask(__name__)


@app.route('/')
def search_entry():
    return render_template('home.html')


@app.route('/search_results')
def searching():
    # client = pymongo.MongoClient('mongodb://127.0.0.1:27017/', connect=Flase)
    # database = client.glugledb

    query_input = request.args.get('search')

    return render_template('searches.html', query_input=query_input)


if __name__ == '__main__':
    app.run(debug=True)
