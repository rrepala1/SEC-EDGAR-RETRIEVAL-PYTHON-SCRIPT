import re
import urllib2
import os
 
from bs4 import BeautifulSoup
import requests
 
 
companyCodeList = list()    # company code list
cikList = list()              # cik code list
 
 
 
 
try:
    crs = open("data.txt", "r")
except:
    print "No input file Found"
 
    # get the comapny  quotes and cik number from the file.
for columns in ( raw.strip().split('\t') for raw in crs ):
    # print columns
    companyCodeList.append(columns[0])
    cikList.append(columns[1])
 
 
cikList = cikList[1:]
companyCodeList = companyCodeList[1:]
 
 
print companyCodeList, cikList
 
 
folder = input("Enter the Folder Name: ")
 
count = 0  # Count for displaying 40 elements on the Company Search page
tddoc = [1]  # Initialize to any non-empty list
companyList = []
typeList = ["8-K", "10-K"]
myList = ["8-K", "10-K", "8-K/A","10-K/A"]
 
if not os.path.exists("Crawled Data/"):
    os.makedirs("Crawled Data/")
if not os.path.exists("Crawled Data/" + str(folder)):
    os.makedirs("Crawled Data/" + str(folder))
for j in range(len(cikList)):
    if not os.path.exists("Crawled Data/" + str(folder) + "/" + str(cikList[j])):
        os.makedirs("Crawled Data/" + str(folder) + "/" + str(cikList[j]))
    if not os.path.exists("Crawled Data/" + str(folder) + "/" + str(cikList[j]) + "/" + str("8-K")):
        os.makedirs("Crawled Data/" + str(folder) + "/" + str(cikList[j]) + "/" + str("8-K"))
    if not os.path.exists("Crawled Data/" + str(folder) + "/" + str(cikList[j]) + "/" + str("10-K")):
        os.makedirs("Crawled Data/" + str(folder) + "/" + str(cikList[j]) + "/" + str("10-K"))
for z in range(len(typeList)):
    print typeList[z]
    for i in range(len(cikList)):
        print  "started data for " + cikList[i]
        count = 0
        while (count < 300):
 
            base_url = "http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=" + str(
                cikList[i]) + "&type="+str(typeList[z])+"&dateb=&owner=exclude&output=xml&match=&start=" + str(count) + "&count=100"
 
 
            r = requests.get(base_url)
            print base_url
            data = r.text
            soup = BeautifulSoup(data)  # Initializing to crawl again
            linkList = []  # List of all links from the CIK page
 
            count += 100
 
            docList = []
            docNameList = []  # List of document names
            # If the link is .htm convert it to .html
            for link in soup.find_all('filinghref'):
 
                URL = link.string
 
                txtdoc = URL[0:len(URL) - 11]
                docname1 = txtdoc.split("/")[len(txtdoc.split("/")) - 1]
                text1 = URL.rfind("/")
                text2 = docname1.rfind("-")
 
                URL2 = URL[0:text1 + 1]
 
                r1 = requests.get(URL)
                data1 = r1.text
                soup1 = BeautifulSoup(data1)
 
                for link1 in soup1.find_all('a'):
                    URL1 = link1.string
 
                    for t in soup1.find_all('strong'):
 
                        types = t.string
                        if types in myList:
                            fi = types
                            fslash = fi.find("/")
                            if fslash != -1 :
                                fi = fi[:fslash] + fi[(fslash)+1]
 
                    fname = URL[text1+2:len(URL)-10]
                    fname = fname + "_"+ str(cikList[i])+"_" + str(companyCodeList[i]) + "_" + str(fi)
 
 
 
                    if URL1 is not None:
                        m = URL1.find('.htm')
                        n = URL1.find('index')
                        p = URL1.find('.txt')
                        q = URL1.find('.xml')
 
                    if ((m != -1 or p!= -1 or q!=-1) and n == -1):
                        o = len(URL)
                        o = o - 39
 
                        year =  docname1[11:13]
 
 
                        txtdoc = URL2 + URL1
                        URL1 = str(year) + "_"+ str(fi) + "_" + URL1
 
                        base_url = txtdoc
 
                        r = requests.get(base_url)
                        data = r.text
                        if not os.path.exists("Crawled Data/" + str(folder) + "/" + str(cikList[i]) + "/" + str(typeList[z]) +"/"+ fname ):
                          os.makedirs(
                                 "Crawled Data/" + str(folder) + "/" + str(cikList[i]) + "/" + str(typeList[z]) + "/" + fname )
 
                          if m!= -1:
 
                              if not os.path.exists("Crawled Data/" + str(folder) + "/" + str(cikList[i]) + "/" + str(typeList[z]) +"/"+ fname + "/"+"html" ):
                                    os.makedirs(
                                        "Crawled Data/" + str(folder) + "/" + str(cikList[i]) + "/" + str(typeList[z])+ "/" + fname +"/"+  "html" )
                                path = "Crawled Data/" + str(folder) + "/" + str(cikList[i]) + "/" + str(typeList[z]) +"/"+  fname + "/" +"html"+ "/"  + URL1
                            elif p!= -1:
                                if not os.path.exists("Crawled Data/" + str(folder) + "/" + str(cikList[i]) + "/" + str(typeList[z]) +"/"+ fname + "/"+"text" ):
                                    os.makedirs(
                                        "Crawled Data/" + str(folder) + "/" + str(cikList[i]) + "/" + str(typeList[z]) + "/" + fname +"/"+  "text" )
 
                                path = "Crawled Data/" + str(folder) + "/" + str(cikList[i]) + "/" + str(typeList[z]) +"/"+ fname + "/" +"text"+ "/"  + URL1
 
                            else:
                                if not os.path.exists("Crawled Data/" + str(folder) + "/" + str(cikList[i]) + "/" + str(typeList[z]) +"/"+ fname+ "/"+"XML" ):
                                    os.makedirs(
                                        "Crawled Data/" + str(folder) + "/" + str(cikList[i]) + "/" + str(typeList[z]) + "/" + fname +"/"+  "XML" )
                                path = "Crawled Data/" + str(folder) + "/" + str(cikList[i]) + "/" + str(typeList[z]) +"/"+ fname + "/" +"XML"+ "/" + URL1
 
                        filename = open(path, "a")
                        filename.write(data.encode('ascii', 'ignore'))
