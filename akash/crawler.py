import requests
from bs4 import BeautifulSoup
import pymongo

class Crawler:
    mongo_url = "mongodb://localhost:27017/"
    client = pymongo.MongoClient(mongo_url)

    disallowed_links = []

    db = client['search']

    def robot(self, url):
        bot_url = f'{url}/robots.txt'
        try:
            bot_text = requests.get(bot_url, 'lxml').text
        except:
            print("Failed to Perform HTTP GET Request ! ")
            return

        soup = BeautifulSoup(bot_text)
        p = soup.find('p').text

        lines = str(p).splitlines()

        for line in lines:
            if line.startswith('Disallow:'):
                split = line.split(':', maxsplit=1)

                self.disallowed_links.append(
                    f'{url}{split[1].strip()}')
        print(self.disallowed_links)
    def crawl(self, url, depth, links = disallowed_links):
        if url not in links:
            try:
                html_text = requests.get(url, 'lxml').text
            except:
                print("Failed to Perform HTTP GET Request ! ")
                return
        else:
            return

        soup = BeautifulSoup(html_text)

        try:
            title = soup.find('title').text

            description = ''
            contents = soup.find_all('p')
        except:
            return

        for content in contents:
            description += content.text.strip().replace('\n', '')

        result = {
            'url': url,
            'title': title,
            'description': description
        }

        search_results = self.db['search_result']

        search_results.insert_one(result)
        search_results.create_index([
            ('url', pymongo.TEXT),
            ('title', pymongo.TEXT),
            ('description', pymongo.TEXT)
        ], name='search_results', default_language='english')

        # search_results.remove( { } )

        for item in search_results.find():
            print(item)

        if depth == 0:
            return

        links = soup.find_all('a')

        for link in links:
            try:
                if 'http' in link['href']:
                    self.crawl(link['href'], depth-1)
            except KeyError:
                pass
        self.client.close()


crawler = Crawler()
crawler.robot('https://geeksforgeeks.org/')
crawler.crawl('https://geeksforgeeks.org/', 0) 