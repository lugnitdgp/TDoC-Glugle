from crawler.crawler import Crawler
from urls.urls import urls

crawler_obj=Crawler(urls)
crawler_obj.start_crawl(urls=crawler_obj.urls, disallowed_urls=crawler_obj.disallowed_urls)
crawler_obj.crawl(disallowed_urls=crawler_obj.disallowed_urls, urls=crawler_obj.urls, depth=2) #change depth to increase search depth but at your own risk