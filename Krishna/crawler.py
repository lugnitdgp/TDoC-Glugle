import pymongo
import requests
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
            

class Crawler:
    client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
    db = client.crawl_database
    collection = db.crawl_collection_gfg

    disallowed_links = []

    def start_crawl(self, url, depth):
        
        try:
            complete_url = urllib.parse.urljoin(url,'/robots.txt')
            robots = requests.get(complete_url)

            soup = BeautifulSoup(robots.text, 'lxml')
            our_robots = soup.find('p').text
            #find words starting with / and append it to disallowed_links
            
          
            for link in our_robots:
                if link(0)=='/':
                    Link = urllib.parse.join(url,link)
                    self.disallowed_links.append(Link)
        
        except:
            pass   

        self.crawl(url,depth,self.disallowed_links)
    
    def crawl(self, url, depth, *disallowed_links):
        try:
            complete_url = urllib.parse.urljoin('https://www.geeksforgeeks.org/fundamentals-of-algorithms/', url)
            response = requests.get(complete_url)
            print('Response received.')

            soup = BeautifulSoup(response.text, 'lxml')
            title = soup.find('title').text
            description = soup.find('p').text
            query = {
                'url' : url,
                'title' : title,
                'description' : description     
            }       

            self.collection.insert_one(query)
            self.collection.create_index(
                [
                    ('url',pymongo.TEXT),
                    ('title',pymongo.TEXT),
                    ('description',pymongo.TEXT),
                ], name='search_results', default_language='english'
            )
            links = []
            if depth==0:
                return
            else:
                for Link in soup.find_all('a'):
                    links.append(Link.get('href'))
            for link in links:
                if link in disallowed_links:
                    print('Disallowed link encountered.')
                else:
                    self.crawl(link, depth-1)

            self.client.close()

        except Exception as e:
            print(e)
        

object = Crawler()
object.start_crawl('https://www.geeksforgeeks.org/fundamentals-of-algorithms/', 1)



#Links:
#https://www.geeksforgeeks.org/fundamentals-of-algorithms/
#https://www.rottentomatoes.com/
#https://www.stackoverflow.com/

