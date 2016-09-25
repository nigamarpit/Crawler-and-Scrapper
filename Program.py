import json
import os
import inspect
import urllib2
from bs4 import BeautifulSoup as BS
from collections import OrderedDict

class Program(object):
    def __init__(self):
        ospath=inspect.getfile(inspect.currentframe())
        self.path="\\".join(ospath.split("\\")[:-1])+"\\Data"
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.url ="http://beta.fortune.com/fortune500/walmart-1"
        self.baseurl="http://beta.fortune.com"
        self.links=[]
        self.soup = None
        self.result=list()
        for i in range(500):
            self.crawler()
            self.wrapper()
        l=list()
        for x in self.result:
            d=OrderedDict(dict())
            for y in x:
                d[y[0]]=y[1].encode("ascii","ignore")
            l.append(json.dumps(d))
        f=open("extractions.json","w")
        f.write("\n".join(l))
#        f.write(str(self.result).encode("utf-8"))
        f.close()
        
    def crawler(self):
        print "url:", self.url
        file=os.path.join(self.path,self.url.split("/")[-1].split("-")[-1]+"-"+"".join(self.url.split("/")[-1].split("-")[:-1])+".html")
        if not os.path.isfile(file):
            usock = urllib2.urlopen(self.url)
            data = usock.read()
            usock.close()
            self.soup = BS(data,"html.parser")
            f=open(file,"w")
            f.write(str(self.soup))
            f.close()
        else:            
            f=open(file,"r")
            self.soup=BS(f,"html.parser")
            f.close()

    
    def wrapper(self):
        l=list()
        l.append(("URL",self.url))
        company=self.soup.find("h1",attrs={"class":"branding-tile-title text-center"}).text.strip()
        l.append(("Company",company))
        ceo=[div.text for div in (self.soup.find_all("div",attrs={"class":"columns small-7 medium-6 company-info-card-data"}))][0]
#        print ceo
 #       ceo=[div.p.text for div in (div.div for div in (div.div  for div in self.soup.findAll("div",attrs={"class":"small-12 columns remove-all-padding"})))][0]
        l.append(("CEO",ceo))
        sector=[div.text for div in (self.soup.find_all("div",attrs={"class":"columns small-7 medium-6 company-info-card-data"})[1])][0]
        l.append(("Sector",sector))
        hq=[div.text for div in (self.soup.find_all("div",attrs={"class":"columns small-7 medium-6 company-info-card-data"})[3])][0]
        l.append(("HQLocation",hq))
        employees=[div.text for div in (self.soup.find_all("div",attrs={"class":"columns small-7 medium-6 company-info-card-data"})[5])][0]
        l.append(("Employees",employees))
        revenue=[span for span in self.soup.find_all("span",attrs={"class":"data"})[1]][0]
        l.append(("Revenue",revenue))
        assets=[span for span in self.soup.find_all("span",attrs={"class":"data"})[3]][0]
        l.append(("Assets",assets))
        self.result.append(l)
        linkdivs=[div.a for div in self.soup.findAll("div",attrs={"class":"nav-button"})]
#        print "rightdivs:", len(linkdivs)
        if len(linkdivs)==1:
            urllink=linkdivs[0].get("href").encode("ascii","ignore")
            self.links.append((self.baseurl+urllink).strip())
            self.url=self.links[-1]
            return
        """
        if(re.match(pattern,str(urllink))):
            if not (self.baseurl+urllink).strip() in self.links:
        """
        if self.links[-1]=="http://beta.fortune.com/fortune500/celanese-453":
            self.links.append("http://beta.fortune.com/fortune500/clorox-455")
            self.url=self.links[-1]    
            return
        if self.links[-1]=="http://beta.fortune.com/fortune500/ashland-472":
            self.links.append("http://beta.fortune.com/fortune500/insight-enterprises-474")
            self.url=self.links[-1]    
            return
        urllink=linkdivs[1].get("href").encode("ascii","ignore")
        self.links.append((self.baseurl+urllink).strip())
        self.url=self.links[-1]    
Program()