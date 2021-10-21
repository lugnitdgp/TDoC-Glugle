import requests
import pymongo
import urllib.parse
from bs4 import BeautifulSoup
import sys


class Crawler:
    client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
    db = client.database
    disallowed_links = []

    def start_crawl(self, url, depth):
        global robots
        complete_url = urllib.parse.urljoin(url, '/robots.txt')
        try:
            robots = requests.get(complete_url)
        except:
            print("Robots not found.")
            self.crawl(url, depth)

        soup = BeautifulSoup(robots.text, 'lxml')
        results = soup.find('p').text
        for text in results:
            if text[0] == '/':
                self.disallowed_links.append(urllib.parse.urljoin(url, text))
        self.crawl(url, depth, self.disallowed_links)

    def crawl(self, url, depth, *disallowed_links):
        
        try:
            print(f"Crawling url {url} at depth: {depth}")
            response = requests.get(url)
        except:
            return
        
        soup = BeautifulSoup(response.text, 'lxml')

        try:
            title = soup.find('title').text
            description = ''

            for tag in soup.findAll():
                if tag.name == 'p':
                    description += tag.text.strip().replace('\n', ' ')
        
        except:
            return
        
        query = {
            'url' : url,
            'title': title,
            'description' : description,
        }

        search_results = self.db.search_results

        search_results.insert_one(query)

        search_results.create_index(
            [
                ('url', pymongo.TEXT),
                ('title', pymongo.TEXT),
                ('description', pymongo.TEXT)
            ],
            name='search_results',
            default_language="english"
        )

        if depth == 0:
            return

        links = soup.findAll('a')

        for link in links:
            try:
                if link['href'] not in disallowed_links:
                    if 'http' in link['href']:
                        self.crawl(link['href'], depth-1, disallowed_links)
                    else:
                        link['href'] = urllib.parse.urljoin(url, link['href'])
                        self.crawl(link['href'], depth-1, disallowed_links)
            except :
                print("no links retrieved from the page")
                pass

        self.client.close()



crawler = Crawler()
crawler.start_crawl(
    sys.argv[1], int(sys.argv[2])
)