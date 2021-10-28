from flask import Flask,render_template,request,redirect,url_for,jsonify
# from flask_paginate import Pagination, get_page_parameter
from flask_paginate import Pagination, get_page_args
import pymongo
import string

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()

client=pymongo.MongoClient("mongodb://127.0.0.1:27017/")
db=client.urlList
collection=db.urlcrawled

app=Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

def get_paginated_search_results(search_results, offset=0, per_page=10):
    return search_results[offset: offset + per_page]


def text_lowercase(text):
    return text.lower()

def remove_punctuation(text):
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)

def remove_stopwords(text):
    stop_words = set(stopwords.words("english"))
    word_tokens = word_tokenize(text)
    filtered_text = [word for word in word_tokens if word not in stop_words]
    return filtered_text

def stem_words(text):
    word_tokens = word_tokenize(text)
    stems = [stemmer.stem(word) for word in word_tokens]
    return stems

@app.route('/search')
def search():
    page,per_page,offset=get_page_args(page_parameter='page',per_page_parameter='per_page')

    query_text=request.args.get('query','')
    query=text_lowercase(query_text)
    query=remove_punctuation(query)
    query=remove_stopwords(query)
    query_list=[]
    for query_item in query:
        query_list.append(*stem_words(query_item))

    search_results=[]

    for query_item in query_list:

        result_data=db.urlcrawled.find(
            {
                '$text':{
                    '$search':query_item,
                    '$caseSensitive':False
                }
            },
            {
                'score':{
                    '$meta':'textScore'
                }
            }
        ).sort(
            [
                ('score',{'$meta':'textScore'}),
                ('_id',pymongo.DESCENDING)
            ]
        )

        for data in result_data:
            data['score']=2*data['title'].count(query_item)+data['description'].count(query_item)
            exist=False
            for result in search_results:
                if result['title'] == data['title'] or result['url'] == data['url']:
                    exist=True
                    break
        
            if exist==False:
                search_results.append(data)

    new_search_results=sorted(search_results,key=lambda d:d['score'])

    total = len(new_search_results)

    pagination = Pagination(
        page=page,
        total=total,        
        per_page=per_page,
        format_total=True,
        prev_label='<i class="fa fa-caret-left"></i>',
        next_label='<i class="fa fa-caret-right"></i>',
        format_number=True,
        record_name='results',
        alignment='center'
    )

    return render_template(
        "search.html",
        query_text=query_text,    
        search_results=get_paginated_search_results(new_search_results, offset, per_page),
        total=total,
        pagination=pagination
    ) 
    

if __name__ == "__main__":
    app.run(debug=True,port=5001)