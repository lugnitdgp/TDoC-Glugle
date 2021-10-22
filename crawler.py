import requests
from bs4 import BeautifulSoup
import urllib.parse
import urllib.request
import pymongo
import lxml
import sys


class Crawler:
    client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
    db = client.glugledb
    collection = db.info

    disallowed_link = []

    def start_crawl(self, url, depth):
        robots = urllib.parse.urljoin(url, '/robots.txt')

        try:
            robot = requests.get(robots)
        except:
            print("Robots not found here!")
            self.crawl(url, depth)

        soup = BeautifulSoup(robot.text, 'lxml')
        content = soup.find('p').text

        for word in content:
            if word[0] == '/':
                self.disallowed_link.append(urllib.parse.urljoin(url, word))
        print("Robots found and appended in dissallowed_links...")

        self.crawl(url, depth, self.disallowed_link)

    def crawl(self, url, depth, *disallowed_link):
        try:
            print(f"Crawling url {url} at depth: {depth}")
            response = requests.get(url)
        except:
            print(f"Failed to perform HTTP GET request on {url}")
            return
        soup = BeautifulSoup(response.text, 'lxml')

        try:
            title = soup.find('title').text
            desc = ''

            for tag in soup.findAll():
                if tag.name == 'p':
                    desc = desc + tag.text.strip().replace('\n', '')

        except:
            print("Failed to retrieve title and desc...")
            return

        query = {
            'url': url,
            'title': title,
            'description': desc,
        }

        results = self.db.results
        results.insert_one(query)
        results.create_index(
            [
                ('url', pymongo.TEXT),
                ('title', pymongo.TEXT),
                ('desc', pymongo.TEXT)
            ],
            name='results',
            default_language='english'
        )

        if depth == 0:
            return

        links = soup.findAll('a')

        for link in links:
            try:
                if link['href'] not in disallowed_link:
                    if 'http' in link['href']:
                        self.crawl(link['href'], depth-1, disallowed_link)
                    else:
                        link['href'] = urllib.parse.urljoin(url, link['href'])
                        self.crawl(link['href'], depth-1, disallowed_link)
            except KeyError:
                print("No links retrieved from the page")
                pass

        self.client.close()


spider = Crawler()
spider.start_crawl(
    sys.argv[1], int(sys.argv[2])
)
