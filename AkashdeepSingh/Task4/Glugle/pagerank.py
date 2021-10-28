import pymongo
import networkx as nx
from operator import itemgetter

connection_url = "mongodb://127.0.0.1:27017/"
client = pymongo.MongoClient(connection_url)
db = client.results
results = db.search_results
entries = list(results.find({}))

total_entries = len(entries)

G = nx.DiGraph()

for doc in entries:
    G.add_node(doc['url'])

for i in range (0, total_entries):
        for j in range (0, total_entries):
            if i != j and entries[i]['url'] == entries[j]['url']:
                G.add_edge(entries[i]['url'], entries[j]['url'])

pageranks = nx.pagerank(G)

i = 0
for key in pageranks.keys():
    url = entries[i]['url']
    pagerank = pageranks[key]
    results.update_one({'url': url}, {'$set': {'pagerank': pagerank}})
    i += 1

client.close()
