import requests
import re
from bs4 import BeautifulSoup
from tld import get_tld
import pprint
    
#TODO: Capture the username from the href - include username check in __equals__
socialDomains = ["twitter.com","facebook.com","linkedin.com","quora.com","angel.co"]

def isTwitterProfile(href,tld):
    urlParts = href.split(str(tld))
    if(re.match(r'^/[\w\d\.-]+[\w\d]$', urlParts[1])):
        if(len(urlParts[0])==0 or re.match(r'[\w\d://]*www[\.]$', urlParts[0]) or re.match(r'[\w:/]+[/]$', urlParts[0])):
            uname = re.search(r'[\w\d.-]+[\w\d]$',urlParts[1]).group();
            if uname == 'share':
                return False
            else:
                return True
    return False
    
def isFacebookProfile(href,tld):
    urlParts = href.split(str(tld))
    if re.match(r'^/[\w\d\.-]+[\w\d]$', urlParts[1]):
        return True
    return False
    
def isLinkedInProfile(href,tld):
    urlParts = href.split(str(tld))
    if re.match(r'^/[\w\d/\.-]+[\w\d]$', urlParts[1]):
        return True
    return False
    
def isAngelProfile(href,tld):
    urlParts = href.split(str(tld))
    if re.match(r'^/[\w\d\.-]+[\w\d]$', urlParts[1]):
        return True
    return False
    
def isQuoraProfile(href,tld):
    urlParts = href.split(str(tld))
    if re.match(r'^/[\w\d\.-]+[\w\d]$', urlParts[1]):
        return True
    return False
            
class URL:
    def __init__(self, href, tld):
        self.href = href
        self.tld = tld
        self.social = self.isSocial(tld)
        if self.social:
            self.profile = self.isSocialProfile(tld)
        else:
            self.profile = False
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.href == other.href

    def isSocial(self, tld):
        return str(tld) in socialDomains

    def isSocialProfile(self, tld):
        if str(tld) == "twitter.com":
            return isTwitterProfile(self.href, tld)
        if str(tld) == "facebook.com":
            return isFacebookProfile(self.href, tld)
        if str(tld) == "linkedin.com":
            return isLinkedInProfile(self.href, tld)
        if str(tld) == "quora.com":
            return isQuoraProfile(self.href, tld)
        if str(tld) == "angel.co":
            return isAngelProfile(self.href, tld)
      
def getAllLinks(url):
    try:
        r = requests.get(url)
        s = BeautifulSoup(r.content)
        return s.findAll("a", href=True)
    except:
        return []

def getValidURLs(links):
    URLs = []
    for link in links:
        tld = get_tld(link['href'], fail_silently=True)
        if tld is not None:
            url = URL(link['href'], tld)
            if url not in URLs:
                URLs.append(url)
    return URLs

def processURLs(URLs):
    data = {} 
    for socialDomain in socialDomains:
        data[socialDomain] = []
        
    found = False
    for URL in URLs:
        if URL.profile:
            data[str(URL.tld)].append(URL.href)
            print(URL.href)
            if not found:
                found = True
                
    if not found:
        print("No social URLs found")
    
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(data)

    return data

def getSocialURLs(url):
    links = getAllLinks(url)
    urls = getValidURLs(links)
    processURLs(urls)


if __name__ == "__main__":
    bored = False
    while not bored:
        url = input('Enter a URL (Enter "X" to stop break the loop) >>')
        if(url == "X"):
            bored = True
            break
        getSocialURLs(url)

    
    
