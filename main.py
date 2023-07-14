import csv
import time
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

file_path = "data/results.csv"
class CrawledApprenticeship:
    def __init__(self, profession, company, url, start, district, qualification, company_id, offer_id, chash):
        self.profession = profession
        self.company = company
        self.url = url
        self.start = start
        self.district = district
        self.qualification = qualification
        self.company_id = company_id
        self.offer_id = offer_id
        self.chash = chash


class ApprFetcher:
    def fetch(self):
        time.sleep(1)
        link = "https://www.lehrstelle-handwerk.de/ausbildung/lehrstellenboerse-praktikumsboerse/lehrstelle-suchen/list"
        rh = requests.get(link)
        site = BeautifulSoup(rh.text, "html.parser")
        apprenticeships = []
        for table in site.find_all("tbody"):
            profession = table.select_one(".lehrstellen").text.strip()

            for tr in table.find_all("tr"):

                if tr.select_one(".flush") is None:
                    continue
                else:

                    company = tr.select_one(".flush").text.strip()
                    url = "https://www.lehrstelle-handwerk.de" + tr.select_one("a", href=True)['href'].strip()
                    start = tr.select_one("a").text.strip()
                    both_ids = str(url)[slice(str(url).find("firma/") + 6, str(url).find("?"))].strip()
                    company_id, offer_id = both_ids.split(".")
                    chash = str(url)[slice(str(url).find("?cHash=") + 7, len(url))].strip()
                    district = tr.select_one("td[data-label='Stadtteil']").text.strip()
                    qualification = tr.select_one("td[data-label='Abschluss']").text.strip()

                    apprenticeships.append(
                        CrawledApprenticeship(profession, company, url, start, district, qualification, company_id, offer_id, chash))

        return apprenticeships


fetcher = ApprFetcher()

# write CSV file

file_exists = os.path.isfile(file_path)
print(file_exists)

with open(file_path, 'a', newline='', encoding='utf-8') as csvfile:
    print("Opening file ....")
    writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not file_exists:
        writer.writerow(
            ["timestamp", "hash", "profession", "company_ident", "company_name", "offer_id", "url", "start_date", "district", "qualification"])
    for appr in fetcher.fetch():
        writer.writerow(
            [timestamp, appr.chash, appr.profession, appr.company_id, appr.company, appr.offer_id, appr.url, appr.start, appr.district,
             appr.qualification])
    print("Closing ...")

