import re
import sys
import pymongo
import requests
import urllib.parse
from bs4 import BeautifulSoup
from pymongo.errors import ConnectionFailure

class Crawler():

    """
    The Crawler class is used to crawl on an entrypoint web URL, given as input by the user, with a depth also specified by the user.
    """


    def __init__(self):
        
        """
        Constructor for creating objects of the Crawler class.
        It creates a connection to the mongo database, or exits if it enconters an error.
        """

        try:
            self.client = pymongo.MongoClient("mongodb://127.0.0.1:27017")
            self.db = self.client.glugledb
        except pymongo.errors.ConnectionFailure as e:
            print("ERROR connecting to database", e)
            exit(0)


    def start_crawl(self, url, depth):

        """
        Initiates the crawling process on the given URL and depth.
        
        Downloads the robots.txt file of the input URL;
        Extracts all the disallowed links and;
        Makes a call to the recursive crawl() function to start crawling
        
        ##### Required parameters:
        `url` : URL to crawl upon
        `depth` : max recusion depth to control the number of pages crawled
        
        """
        
        disallowed_links = []

        try:
            # get the robots.txt file of the input URL
            complete_url = urllib.parse.urljoin(url, '/robots.txt')
            robots = requests.get(complete_url)
            soup = BeautifulSoup(robots.text, 'lxml')

            # extract the disallowed links
            our_robots = soup.find('p').text
            disallowed_links = [link[10:] for link in re.findall("Disallow: /.*", our_robots)]
        
        except requests.exceptions.ConnectionError as e:
            print("ERROR Connecting to", complete_url, ":", e)
            return

        # start crawling process
        self.crawl(url, depth, disallowed_links)


    def crawl(self, url, depth, disallowed_links):
        
        """
        A recursive function to crawl on a given URL. It extracts all the URLs available from the given page URL, and keeps going until it reaches the defined depth as input.

        ##### Required parameters:
        `url` : URL to crawl upon
        `depth` : max recusion depth to control the number of pages crawled
        `disallowed_links` : links that are disallowed in robots.txt of the domain

        """

        # create absolute URLs
        url = urllib.parse.urljoin(url, "")
        print(f"Crawling {url} at depth {depth}")
        title = ""
        desc = ""
        result = None

        try:
            # get the page data
            result = requests.get(url)

            try:
                soup = BeautifulSoup(result.text, 'lxml')
                
                try:
                    title = soup.find('title')
                    title = title.text
                except:
                    title = ""

                try:
                    desc_list = soup.find_all('p')
                    desc = " ".join(item.text.replace('\n', '') for item in desc_list)
                except:
                    desc = ""
                
            except Exception as e:
                print("ERROR getting page details : ", e)

            # process and insert query data in database only if did not encounter a 404 error  
            if result and result.status_code != 404:
                
                query = {
                    'url':url,
                    'title': title,
                    'description': desc
                }
                print(query)

                try:
                    self.db.query_data.insert_one(query)
                    self.db.query_data.create_index(
                        [
                            ('url', pymongo.TEXT),  
                            ('title', pymongo.TEXT),
                            ('description', pymongo.TEXT)
                        ],
                        name="query_data_index",
                        default_language="english"
                    )
                except Exception as e:
                    print("ERROR inserting data : ", e)
                    exc_type, exc_val, tb_obj = sys.exc_info()
                    print(exc_type, "at", tb_obj.tb_lineno)

                # extract all links in page and continue crawling, only if max depth allowed has not reached 0
                if depth != 0:
                    try:
                        links = [urllib.parse.urljoin(url, link.get('href')) for link in soup.find_all('a')]
                        
                        for link in links:
                            if link not in disallowed_links:
                                self.crawl(link, depth-1, disallowed_links)

                    except Exception as e:
                        print("ERROR getting links : ", e)

        
        except:
            print("ERROR fetching", url)

        
        self.client.close()


crl = Crawler()
crl.start_crawl("https://www.wikipedia.org", 2)