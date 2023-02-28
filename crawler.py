import pymongo
import urllib.parse
import requests
from bs4 import BeautifulSoup
import sys
from decouple import config

class Crawler():
  client = pymongo.MongoClient(config('MONGO_URI'))
  # client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
  db = client.glugle
  dissallowedLinks = []
  
  def StartCrawl (self, url, depth):
    complete_url = urllib.parse.urljoin(url, "/robots.txt")
    print(complete_url)
    try:
      response = requests.get(complete_url)
      print("Response: ", response)
    except:
      print("Failed to get response!")
      self.Crawl(url, depth)

    soup = BeautifulSoup(response.text, 'lxml')
    robots_content = soup.find('p').text
    links = robots_content.split()
    for link in links:
      if (link[0] == '/'):
        self.dissallowedLinks.append(urllib.parse.urljoin(url, link))
    print("Robots found and appended!")
    self.Crawl(url, depth, self.dissallowedLinks)

  def Crawl(self, url, depth, *dissallowedLinks):
    try:
      print(f"Crawling url: {url} at depth {depth}")
      response = requests.get(url)
    except:
      print(f"Failed to perform GET req on {url}")
      return
    soup = BeautifulSoup(response.text, 'lxml')
    try:
      title = soup.find('title').text
      description = ''
      for tag in soup.findAll():
        if tag.name == 'p':
          description += tag.text.strip().replace('\n', '')
    except:
      print("Failed to retrieve title and desc.")
      return

    query = {
      'url': url,
      'title': title,
      'description': description
    }
    search_results = self.db.search
    search_results.insert_one(query)
    search_results.create_index(
      [
        ('url', pymongo.TEXT),
        ('title', pymongo.TEXT),
        ('description', pymongo.TEXT)
      ],
      name = 'search_results',
      default_language = 'english'
    )
    if depth == 0:
      return
    links =  soup.findAll('a')
    for link in links:
      try:
        if link['href'] not in dissallowedLinks[0]:
          if 'http' in link['href']:
            self.Crawl(link['href'], depth-1, dissallowedLinks[0])

          else:
            link['href'] = urllib.parse.urljoin(url, link['href'])
            self.Crawl(link['href'], depth-1, dissallowedLinks[0])

      except:
        print("No links retieved from page")
        pass

    self.client.close()

crawler = Crawler()
# crawler.StartCrawl("https://www.rottentomatoes.com", 2)
crawler.StartCrawl("https://www.wikipedia.org/", 2)


crawler.StartCrawl(
  sys.argv[1], int(sys.argv[2])
)