from flask import Flask, request
import pymongo, string
from utils import *
import nltk
from decouple import config
from flask_cors import CORS

# nltk.download('stopwords')
# nltk.download('punkt')

connect_url = config('MONGO_URI')
client = pymongo.MongoClient(connect_url)
db = client.glugle

app = Flask(__name__)
CORS(app)

# @app.route('/')
# def home():
#   return render_template('home.html')    

@app.route('/', methods=['POST'])
def search_results():
  print(request)
  print(request.json)
  # search_string = request.args.get('search')
  search_string = request.json['search']
  search_string = search_string.lower()
  search_string = search_string.translate(str.maketrans('','', string.punctuation))
  search_string = remove_stopwords(search_string)
  print("\n", search_string, "\n")

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
  response = JSONEncoder().encode(search_result)
  return response

if __name__ == '__main__':
  app.run(debug=True)