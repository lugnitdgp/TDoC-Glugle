import pymongo
from bs4 import BeautifulSoup
import requests
import urllib.parse
import sys


class Crawler:
    client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
    db = client.TDoC_Glugle
    Collection = db.results
    disallowed_links = []

    def start_crawling(self, url, depth):
        complete_url = urllib.parse.urljoin(url, '/robots.txt')
        try:
            robots = requests.get(complete_url)
        except Exception as e:
            print("Not get any url")
            self.crawl(url, depth)
        soup = BeautifulSoup(robots.text, 'lxml')
        try:
            content = soup.find('p').text
        except Exception as e:
            print("Not find any p tag")
            pass
        for text in content:
            if text[0] == '/':
                c_url = urllib.parse.urljoin(url, text)
                self.disallowed_links.append(c_url)
        print("-----robots found and appended in disallowed_links-----")
        self.crawl(url, depth, self.disallowed_links)

    def crawl(self, url, depth, *disallowed_links):
        try:
            print(f"Crawling url {url} at depth {depth}")
            robots = requests.get(url)
        except Exception as e:
            print("Failed to perform HTTP GET request on {url}")
            return
        soup = BeautifulSoup(robots.text, 'lxml')
        try:
            title = soup.find('title').text
            description = ''
            for tag in soup.findAll():
                if tag.name == 'p':
                    description += tag.text.strip().replace('\n', '')
        except:
            print("Failed to retrive data")
            return

        query = {'url': url, 'title': title,
                 'description': description}

        self.Collection.insert_one(query)
        self.Collection.create_index([
            ('url', pymongo.TEXT),
            ('title', pymongo.TEXT),
            ('description', pymongo.TEXT),
        ], name='search_result', default_language='english')

        if depth == 0:
            print("--its end--")
            return

        links = soup.findAll('a')

        for link in links:
            try:
                if link['href'] not in self.disallowed_links:
                    if 'http' in link['href']:
                        self.crawl(link['href'], depth-1, disallowed_links)
                else:
                    link['href'] = urllib.parse.urljoin(url, link['href'])
                    self.crawl(link['href'], depth-1, disallowed_links)
            except Exception as e:
                print("Not find any link")
                pass
        self.client.close()


p1 = Crawler()
p1.start_crawling(
    sys.argv[1], sys.argv[2]
)
