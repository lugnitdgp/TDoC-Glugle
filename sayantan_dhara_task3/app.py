from flask import Flask,render_template,request,redirect,url_for
# from flask_paginate import Pagination, get_page_parameter
from flask_paginate import Pagination, get_page_args
import pymongo

client=pymongo.MongoClient("mongodb://127.0.0.1:27017/")
db=client.urlList
collection=db.urlcrawled

app=Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

def get_paginated_search_results(search_results, offset=0, per_page=10):
    return search_results[offset: offset + per_page]

@app.route('/search')
def search():
    page,per_page,offset=get_page_args(page_parameter='page',per_page_parameter='per_page')

    query=request.args.get('query','')
    search_results=[]

    result_data=db.urlcrawled.find(
        {
            '$text':{
                '$search':query,
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
        exist=False
        for result in search_results:
            if result['title'] == data['title'] or result['url'] == data['url']:
                exist=True
                break
        
        if exist==False:
            search_results.append(data)

    total = len(search_results)

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
        query=query,    
        search_results=get_paginated_search_results(search_results, offset, per_page),
        total=total,
        pagination=pagination
    ) 

# @app.route('/search')
# def search_pages():
#     query_text=request.args['query'].strip()
#     if query_text == '':
#         return redirect('/')
#     print(query_text)
#     query_list=collection.find(
#         {'$text':{'$search':query_text,'$caseSensitive':False}}
#     )
#     search_result=[]
#     for elem in query_list:
#         exist = False
#         for result in search_result:
#             if result['title'] == elem['title'] or result['url'] == elem['url']:
#                 exist = True
#                 break

#         if exist == False:
#             search_result.append(elem)
#     print(len(search_result))
#     print(search_result)
#     return redirect(url_for('/search/1',search_result=search_result))
#     # pagination = Pagination(total=len(search_result), record_name=search_result)
#     # return render_template('search.html',query_text=query_text,pagination=pagination,search_result=search_result)

# @app.route('/search/<int:i>')
# def search_page_num(i):
#     limit=10
#     offset=10*(i-1)
#     starting_id=search_result.sort('_id',pymongo.ASCENDING)
#     last_id=starting_id[offset]['_id']

#     numbers=search_result.find({'_id':{'$gte':last_id}}).sort('_id',pymongo.ASCENDING).limit(limit)

#     return render_template('search.html',pages=numbers)


# def get_page_items():
#     page = int(request.args.get('page', 1))
#     per_page = request.args.get('per_page')
#     if not per_page:
#             per_page = current_app.config.get('PER_PAGE', 10)
#     else:
#             per_page = int(per_page)

#     offset = (page - 1) * per_page
#     return page, per_page, offset

if __name__ == "__main__":
    app.run(debug=True)