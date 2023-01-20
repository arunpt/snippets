import re
import csv
import requests
from bs4 import BeautifulSoup
from bs4.element import ResultSet


class TechnoParkScaper:
    def __init__(self) -> None:
        self.header = ["title", "posted on", "closing on", "contact", "descripton", "skills", "company name", "address", "website"]

    def get_soupy_source_code(self, url) -> BeautifulSoup:
        res = requests.get(url)
        return BeautifulSoup(res.text, "html.parser")

    def job_post_list(self) -> ResultSet:
        soup = self.get_soupy_source_code("https://www.technopark.org/job-search")
        return soup.find_all("tr", {"class": "companyList"})

    def scrape(self) -> None:
        with open('data.csv', 'w', encoding="UTF-8") as f:
            writer = csv.writer(f)
            writer.writerow(self.header)
            total_job_post_list = self.job_post_list()
            print(f"found {len(total_job_post_list)} job posts")
            for job_post in total_job_post_list:
                title = job_post.td.text
                url_path = job_post.td.a.get("href")
                cname = job_post.select_one("td:nth-of-type(2)").text
                closing_date = job_post.select_one("td:nth-of-type(3)").text
                if not url_path:
                    continue
                print(f"processing - {title} at {cname}")
                details_soup = self.get_soupy_source_code(f"http://technopark.org{url_path}")
                company_details = details_soup.find("ul", class_="list-sx")
                for dlist in company_details.find_all("li"):
                    if re.search(r"address", dlist.div.text):
                        dlist.find("div").decompose()
                        caddress = dlist.text.strip()
                    elif re.search(r"website", dlist.div.text):
                        cwebsite = dlist.a.text

                for detail in details_soup.find_all("div", class_="block"):
                    if head := detail.find("p", class_="head"):
                        if re.search(r"posted\son.*", head.text, re.IGNORECASE):
                            posted_child = detail.select_one("p:nth-of-type(2)")
                            posted_date = posted_child.text
                        elif re.search(r"contact.*", head.text, re.IGNORECASE):
                            contact = detail.a.text
                        elif re.search(r".*description.*", head.text, re.IGNORECASE):
                            detail.find("p", class_="head").decompose()
                            description = detail.text.strip()
                        elif re.search(r"skills.*", head.text, re.IGNORECASE):
                            detail.find("p", class_="head").decompose()
                            skills = detail.text.strip()
                writer.writerow([
                    title, posted_date, closing_date,
                    contact, description, skills, cname,
                    caddress, cwebsite
                ])


sc = TechnoParkScaper()
sc.scrape()
