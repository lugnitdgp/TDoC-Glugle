from flask import Flask, render_template, request
from flask_paginate import Pagination, get_page_args
import pymongo, string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()
import nltk
nltk.download('stopwords')
nltk.download('punkt')
app = Flask(__name__)

@app.route('/')
def home():
  return render_template('home.html')

def remove_stopwords(text):
  stop_words = set(stopwords.words("english"))
  word_tokens = word_tokenize(text)
  filtered_text = [word for word in word_tokens if word not in stop_words]
  return filtered_text

def stem_words(text):
  word_tokens = word_tokenize(text)
  stems = [stemmer.stem(word) for word in word_tokens]
  return stems

@app.route('/search_results/')
def search_results():
  # connect_url = "mongodb+srv://goofynugtz:1two3456@glugle.l17hyjv.mongodb.net/test"
  connect_url = "mongodb://127.0.0.1:27017/"
  client = pymongo.MongoClient(connect_url)
  db = client.glugle
  search_string = request.args.get('search')
  search_string = search_string.lower()
  search_string = search_string.translate(str.maketrans('','', string.punctuation))
  search_string = remove_stopwords(search_string)

  query = []
  for words in search_string:
    query.append(*stem_words(words))

  search_result = []
  for doc in query:
    results = db.search.find(
      {
        "$text": 
        {
          "$search":doc,
          "$caseSensitive": False
        }
      },
      {"score":{"$meta": "textScore"}}
    )
    results.sort([
      ("score", {"$meta":"textScore"}),
      ("_id", pymongo.DESCENDING)
    ])
    for result in results:
      result["score"] = 2*result["title"].count(doc)+result["description"].count(doc)
      exist = False
      for x in search_result:
        if x["title"] == result["title"] or x["url"] == result["url"]:
          exist = True
          break
      if exist == False:
        search_result.append(result)

  search_result = sorted(search_result, key=lambda x:x["score"])
  # print("\n\nSearch: ", search_result)
  page, per_page, offset = get_page_args(
    page_parameter='page', 
    per_page_parameter='per_page'
  )
  total = len(search_result)
  pagination = Pagination(
    page=page, 
    per_page=per_page, 
    total=total)

  return render_template(
    'search.html', 
    search_result = search_result[offset:offset + per_page],
    page=page,
    per_page=per_page,
    pagination=pagination,
    search_string=search_string
  )

if __name__ == '__main__':
  app.run(debug=True)