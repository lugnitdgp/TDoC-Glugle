class Popularity():
    popular_domains = [ 
                       'https://pypi.org/', 'https://www.indiatoday.in/', 
                     ]

    ps = 0

    def __init__(self, url):
        self.url = url

    def popularity_score(self):
        for domain in self.popular_domains:
            if domain == self.url:
                self.ps += 100/len(self.popular_domains)
            if domain in self.url:
                self.ps += 100/len(self.popular_domains)

        return self.ps