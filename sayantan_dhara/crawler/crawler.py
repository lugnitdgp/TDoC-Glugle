import requests
from bs4 import BeautifulSoup
import pymongo
import urllib.parse

class Crawler:

    #database connections
    client=pymongo.MongoClient("mongodb://127.0.0.1:27017/")
    db=client.urlList
    collection=db.urlcrawled

    urls=[]

    def __init__(self,urls):
        self.urls=urls

    disallowed_urls=[]

    def start_crawl(self,urls,disallowed_urls):
        temp_url_list=[]
        for url in urls:
            robot_url=urllib.parse.urljoin(url,'/robots.txt')
            try:
                robot=requests.get(robot_url)
                soup=BeautifulSoup(robot.content,'lxml').find('p').text
                # print(soup)
                lines=soup.split('\n')
                for line in lines:
                    if line.startswith('Disallow:'):    #handing disallow statements
                        temp=line.replace('Disallow: ','') 
                        if not temp=='/':                       
                            temp_url=urllib.parse.urljoin(url,temp)                        
                            disallowed_urls.append(temp_url)
                    if line.startswith('Sitemap'):      #handing Sitemaps statements
                        temp=line.replace('Sitemap: ','')
                        disallowed_urls.append(temp)
                    if line.startswith('Allow'):        #handing allow statements
                        temp=line.replace('Allow: ','')
                        temp_url=urllib.parse.urljoin(url,temp)
                        temp_url_list.append(temp_url)
                
                
            except:
                print(f"No robots.txt file for {url}")

        urls+=temp_url_list

    def crawl(self,disallowed_urls,urls,depth):
        for url in urls:
            if not url in disallowed_urls:
                try:
                    response=requests.get(url)
                    soup=BeautifulSoup(response.content,'lxml')
                                    
                    if not soup.find('title') == None and not soup.find('p') == None: 
                        description=''
                        paras=soup.find_all('p')
                        for para in paras:
                            description+=para.text
                        
                        # database query
                        query={
                            'url':url,
                            'title': soup.find('title').text,
                            'description': description
                        }

                        self.collection.insert_one(query)

                        self.collection.create_index([
                            ('url',pymongo.TEXT),
                            ('title',pymongo.TEXT),
                            ('description',pymongo.TEXT)
                        ],name='search_result',default_language='english')

                        print(f'Crawled url {url}')

                        if not depth == 0:
                            a_links=soup.findAll('a')
                            links=[]
                            a_links=set(a_links)
                            for a_link in a_links:
                                attribute_link=a_link.attrs
                                temp=attribute_link.get('href')
                                if not temp == None:
                                    url_temp=urllib.parse.urljoin(url.strip(),temp)
                                    if not url_temp in urls:
                                        links.append(url_temp)
                            self.crawl(disallowed_urls=disallowed_urls,urls=links,depth=depth-1)
                        else:                            
                            self.client.close()

                except:
                    print(f'Unable to process for {url}')

