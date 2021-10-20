import pymongo, urllib.parse, requests
from bs4 import BeautifulSoup
from pprint import pprint

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['glugle']
wiki = db['wiki']

pages_crawled = []

class Crawler:
    name = "crawler"

    def __init__(self, name):
        self.name = name
    
    def start_crawling(self, url, depth):
        complete_url = urllib.parse.urljoin(url, '/robots.txt')
        disallowed_links = []

        try:
            robots = requests.get(complete_url)
            soup = BeautifulSoup(robots.text, 'lxml')
            robots = soup.find('p').text
            disallowed_links = self.get_disallowed_links(robots)
        except:
            print("There was some issue getting the robots.txt")
        
        self.crawl(url, depth, disallowed_links)

        client.close()
    
    def crawl(self, url, depth, disallowed_links):

        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        query = self.extractData(soup, url)
        if wiki.find_one({'url' : url}) == None:
            wiki.insert_one(query)
            wiki.create_index([
                ('url', pymongo.TEXT),
                ('title', pymongo.TEXT),
                ('description', pymongo.TEXT)
            ], name = 'search_results', default_language = 'english')

        if depth < 0:
            return

        links = soup.find_all('a')

        for link in links:
            if 'href' in link.attrs:
                if link['href'].startswith('/wiki') and ':' not in link['href']:
                    if link['href'] not in pages_crawled and link['href'] not in disallowed_links:
                        new_link = f"https://en.wikipedia.org{link['href']}"
                        print(new_link)
                        pages_crawled.append(link['href'])
                        self.crawl(new_link, depth - 1, disallowed_links)
        
    def get_disallowed_links(self, robots):
        disallowed_links = []
        all_user_agents = False
        lines = str(robots).splitlines()
        for line in lines:
            line = line.lower()
            if line.startswith('user-agent: *'):
                all_user_agents = True
                continue
            elif line.startswith('user-agent:'):
                all_user_agents = False
                continue

            if all_user_agents == True:
                if line.startswith('disallow:'):
                    disallowed_links.append(line.split(' ')[1].strip())
            
        return disallowed_links

    def extractData(self, soup, url):
        title = soup.find('title').get_text()
        raw_description = soup.find_all('p')
        description = []
        for data in raw_description:
            description.append(data.get_text())
        query = {
            'url' : url,
            'title' : title,
            'description' : description
        }
        return query



def main():
    URL = 'https://en.wikipedia.org'
    my_crawler = Crawler("crawler")
    my_crawler.start_crawling(URL, 0)


if __name__ == '__main__':
    main()