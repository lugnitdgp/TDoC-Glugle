import pymongo
import urllib.parse
import requests
from bs4 import BeautifulSoup


class Crawler:
    client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
    db = client['glugle']
    my_collections = db['info']
    import collections
    disallowed_links = []

    def start_crawl(self, url, depth):
        complete_url = urllib.parse.urljoin
        (url, '/robots.txt')

        try:
            robots = requests.get(complete_url)
            soup = BeautifulSoup(robots.text, 'html.parser')
            try:
                our_robots = soup.find('p')
                for e in our_robots:
                    if e[0] == '/':
                        c_url = urllib.parse.join(
                            url, 'e')
                        disallowed_links.append(c_url)

            except Exception as e:
                pass
        except Exception as e:
            pass

    def crawl(self, url, depth):
        complete_url = urllib.parse.urljoin(
            url, '/robots.txt')
        try:
            robots = requests.get(complete_url)
        except Exception as e:
            pass
        try:
            soup = BeautifulSoup(robots.content, 'html.parser')
            title = soup.find('title')
            description = soup.find('p')
            href = soup.find('a')
            query = {

                "url": complete_url,

                "title": title,

                "description": description
            }

            self.my_collections.insert_one(query)
            self.my_collections.create_index([
                ('url', pymongo.TEXT),
                ('title', pymongo.TEXT),
                ('description', pymongo.TEXT),
            ], name='search_results', default_language='english')

            if depth == 0:
                return
            else:
                links = []
                links.append(href)
                for link in links:
                    if link in self.disallowed_links:
                        pass
                    else:
                        self.crawl(link, depth-1)
            self.client.close()
        except Exception as e:
            pass


obj = Crawler()
obj.start_crawl('https://www.rottentomatoes.com/', 3)
obj.crawl('https://www.rottentomatoes.com/', 3)
