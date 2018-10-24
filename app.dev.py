import requests
import bs4
from bs4 import BeautifulSoup

import pandas as pd
#import tie

URL = "https://www.indeed.com/jobs?q=data+scientist+%2420%2C000&l=New+York&start=10"

page = requests.get(URL)

soup = BeautifulSoup(page.text,"html.parser")

#print(soup.prettify())


title = []
for div in soup.find_all(name="div", attrs={"class": "row"}):
    for a in div.find_all(name="a", attrs={"data-tn-element": "jobTitle"}):
        title.append(a["title"])

company = []
for span in soup.find_all(name="span", attrs={"class": "company"}):
    company.append(span.get_text())

locations = []
for data in soup.find_all(name=["div", "span"], attrs={"class": "location"}):
    locations.append(data.get_text())

applytype = []
for data in soup.findAll(name=["div", "span"], attrs={"class": "iaLabel"}):
    applytype.append(data.get_text())

sponsored = []
for data in soup.findAll(name=["div", "span"], attrs={"class": "sponsoredGray"}):
    sponsored.append(data.get_text())

df = pd.DataFrame(list(zip(title,company,locations,applytype,sponsored)),columns=['title','company','location','applytype','sponsored'])
df