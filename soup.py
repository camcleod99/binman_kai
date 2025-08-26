from bs4 import BeautifulSoup
import requests
from logger import init_log
from database import *

TEST_URL = "https://www.eastdunbarton.gov.uk/services/a-z-of-services/bins-waste-and-recycling/bins-and-recycling/collections/?uprn=132015695"

log_soup = init_log("soup")

class Soup:
    def __init__(self):
        self.log = log_soup
        pass


    def get_data(self, url = TEST_URL) -> list or tuple:
        self.log.info(f"Soup - Fetching {url}:")
        try:
            response = requests.get(url)
            response.raise_for_status()
            site = BeautifulSoup(response.text, 'html.parser')
            self.log.info(f"Success")
            site_table = site.select_one(".bin-table")
            rows = site_table.find_all("tr")
            table_rows = []
            for row in rows:
                table_rows.append([c.get_text(strip=True) for c in row.find_all("td")])
            data = table_rows
        except requests.exceptions.RequestException as e:
            self.log.error(f"Error fetching {url}: {e}")
            raise

        output = []
        table_rows = [r for r in data if r]
        for row in table_rows:
            if row is None:
                continue
            else:
                collection_type = row[0].strip()
                collection_days, collection_date = row[1].split("days", 1)
                output.append([collection_type, collection_days.strip(), collection_date.strip()])
                self.log.info(f"Output Added: {collection_type}, {collection_days.strip()}, {collection_date.strip()}")
        return output