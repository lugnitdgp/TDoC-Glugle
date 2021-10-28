from django.shortcuts import render
from django.core.paginator import Paginator
import pymongo
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
import speech_recognition as sr
import time



def home(request):
    return render(request, 'search/home.html')


def voice(request):
    voice = ''
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        voice =  r.recognize_google(audio)
    except:
        voice = 'Something Wrong !'

    return render(request, 'search/home.html', {'voice' : voice})


def search(request):
    start_time = time.time()

    mongo_url = "mongodb://localhost:27017/"
    client = pymongo.MongoClient(mongo_url)

    db = client['search']

    search = request.GET.get('search')

    # lowercasing
    search = search.lower()

    # remove punctuations
    translator = str.maketrans('', '', string.punctuation)
    search = search.translate(translator)
    search = " ".join(search.split())

    # removing stopwords and tokenization
    stop_words = set(stopwords.words("english"))
    word_tokens = word_tokenize(search)
    query = [word for word in word_tokens if word not in stop_words]

    stemmer = PorterStemmer()
    query = [stemmer.stem(word) for word in query]

    str_query = " ".join(str(x) for x in query)

    # searching

    all_search_result = db['search_result'].find(
        {
            '$text': {
                '$search': str_query,
                '$caseSensitive': False,
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

    search_result = []

    # removing duplicate data

    for item in all_search_result:
        exist = False
        for result in search_result:
            if result['title'] == item['title'] or result['url'] == item['url']:
                exist = True
                break

        if exist == False:
            search_result.append(item)

    list_cur = list(search_result)

    # ranking

    for result in list_cur:
        for word in query:
            if word in result['title'].lower().translate(translator):
                result['score'] += 2
            else:
                result['score'] += 0
            if word in result['description'].lower().translate(translator):
                result['score'] += 1
            else:
                result['score'] += 0

    sorted(list_cur, key=lambda result: result['score'], reverse=True)

    paginator = Paginator(list_cur, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    length = len(list_cur)
    ex_time = round(time.time() - start_time, 2)

    return render(request, 'search/search.html', {'page_obj': page_obj, 'search': search, 'length':length, 'time': ex_time})
