import requests
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
import pandas as pd


class Scraper:

    def __init__(self, job_title):
        self.job_title = quote_plus(job_title)
        print(self.job_title)
        self.dataframe = pd.DataFrame()

    def scrape(self):
        counter = 0
        for _ in range(1, 5):
            URL = f'https://www.indeed.com/jobs?q=title%3A%28{self.job_title}%29&sort=date&limit=50&fromage=1&radius=25&start={counter}'
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
            self.dataframe = self.dataframe.append(df, ignore_index=True)
            print(URL)
            counter += 50
        self.dataframe = self.dataframe.replace(['\n', '\n\n'], '', regex=True)

    def to_csv(self):
        self.dataframe.to_csv('job_data.csv', sep=',')


scraper = Scraper("data scientist")
scraper.scrape()
scraper.to_csv()

# print(soup.prettify())