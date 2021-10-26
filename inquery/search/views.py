from django.shortcuts import render
from django.core.paginator import Paginator
import pymongo

def home(request):
    return render(request, 'search/home.html')

def search(request):
    mongo_url = "mongodb://localhost:27017/"
    client = pymongo.MongoClient(mongo_url)

    db = client['search']

    search = request.GET.get('search')
    search_result = db['search_result'].find({'$text': {'$search': search}})
    list_cur = list(search_result)

    paginator = Paginator(list_cur, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'search/search.html', {'page_obj': page_obj, 'search': search})
