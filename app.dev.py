import requests
import bs4
from bs4 import BeautifulSoup

import pandas as pd
#import tie

dataframe = pd.DataFrame()
counter = 0
for i in range(1, 5):
    URL = f'https://www.indeed.com/jobs?q=title%3A%28data+scientist%29&sort=date&limit=50&fromage=1&radius=25&start={counter}'
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, "html.parser")

    title = []
    for div in soup.find_all(name="div", attrs={"class": "row"}):
        for a in div.find_all(name="a", attrs={"data-tn-element": "jobTitle"}):
            title.append(a["title"])

    company = []
    for div in soup.find_all(name="div", attrs={"class": "row"}):
        for span in div.find_all(name="span", attrs={"class": "company"}):
            company.append(span.get_text())

    location = []
    for div in soup.find_all(name="div", attrs={"class": "row"}):
        for span in div.find_all(name=["div", "span"], attrs={"class": "location"}):
            location.append(span.get_text())

    applytype = []
    for div in soup.find_all(name="div", attrs={"class": "row"}):
        if div.find_all(name="span", attrs={"class": "iaLabel"}):
            for span in div.find_all(name="span", attrs={"class": "iaLabel"}):
                applytype.append(span.get_text())
        else:
            applytype.append('Standard')

    links = []
    for div in soup.find_all(name="div", attrs={"class": "row"}):
        for a in div.find_all(name="a", attrs={"data-tn-element": "jobTitle"}):
            links.append("https://www.indeed.com" + a["href"])

    date = []
    for div in soup.find_all(name="div", attrs={"class": "row"}):
        for span in div.find_all(name="span", attrs={"class": "date"}):
            date.append(span.get_text())

    df = pd.DataFrame(list(zip(title, company, location, date, applytype, links)),
                      columns=['Title', 'Company', 'Location', 'Posted Date', 'Applytype', 'Links'])
    dataframe = dataframe.append(df, ignore_index=True)
    print(URL)
    counter += 50

# print(soup.prettify())

dataframe = dataframe.replace(['\n','\n\n'],'',regex=True)
dataframe

dataframe.to_csv('job_data.csv', sep=',')