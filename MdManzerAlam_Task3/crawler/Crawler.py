from urllib.parse import *
from urllib import robotparser as rb
from urllib.robotparser import RobotFileParser
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from models.query import Query
class Crawler:
    def __init__(self) -> None:
        self.client = MongoClient('localhost',27017)
        pass
    def start_crawl(self,url):
        robo_file_parser = rb.RobotFileParser()
        robo_file_parser.set_url(url+'/robots.txt')
        robo_file_parser.read()
        self.url = url
        self.crawl(url=url,depth=2,rf_parser=robo_file_parser)

    def crawl(self,url,depth,rf_parser:RobotFileParser):
        print(url+" | "+str(depth))

        if depth == 0:
            # todo parse single page
            if rf_parser.can_fetch("*",url=url):

                try:
                    request = requests.get(url)
                    soup = BeautifulSoup(request.text,"lxml")
                    desc = ""
                    try:
                        for p_tag in soup.find_all("p"):
                            desc+=str(p_tag.text)
                    except:
                        desc = "empty"
                    title = ""
                    try:
                        title = soup.find('title').text
                    except:
                        title = "empty"
                    query = Query(title=title,url=url,description=desc)
                    query.save(self.client)
                except:
                    pass
            pass
        else :
            # todo parse multiple pages
            if rf_parser.can_fetch("*",url=url): 
                try:
                    request = requests.get(url)
                    soup = BeautifulSoup(request.text,"lxml")
                    desc = ""
                    try:
                        for p_tag in soup.find_all("p"):
                            desc+=str(p_tag)
                    except:
                        desc = "empty"
                    title = ""
                    try:
                        title = soup.find('title').text
                    except:
                        title = "empty"
                    query = Query(title=title,url=url,description=desc)
                    query.save(self.client)
                    in_page_links_raw = soup.find_all("a")
                    in_page_links = []
                    for a_tag in in_page_links_raw:
                        try:
                            param = str(a_tag["href"])
                        except:
                            param = ""
                            continue
                        if param.startswith(" "):
                            param.removeprefix(" ")
                        if param.startswith("http"):
                            in_page_links.append(param)
                        elif param.startswith("//www"):
                            in_page_links.append("https://"+param.removeprefix("//"))
                        else:
                            in_page_links.append(self.url+param)
                    for link in in_page_links:
                        self.crawl(link,depth-1,rf_parser)
                except:
                    pass
            pass