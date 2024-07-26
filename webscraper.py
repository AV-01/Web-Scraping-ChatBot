import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urldefrag
import os
import json
import time

start = time.time()

class WebScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.domain = urlparse(base_url).netloc
        self.data_folder = "raw-data"
        self.status_file = os.path.join(self.data_folder, "scraped_links.json")

        # Create the data folder if it doesn't exist
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)

        # Load visited links from status file or initialize an empty dictionary
        if os.path.exists(self.status_file):
            with open(self.status_file, 'r', encoding='utf-8') as file:
                self.visited_links = json.load(file)
        else:
            self.visited_links = {}

    def scrape(self, url):
        normalized_url = self.normalize_url(url)
        if normalized_url in self.visited_links:
            return
        print(f"Scraping: {url}")

        try:
            response = requests.get(url)
            response.raise_for_status()
            success = True
            self.visited_links[normalized_url] = "success"
        except requests.RequestException as e:
            print(f"Failed to retrieve {url}: {e}")
            success = False
            self.visited_links[normalized_url] = "failed"

        if success:
            try:
                soup = BeautifulSoup(response.content, 'html.parser')
                links = self.extract_links(soup, url)
                self.process_page(soup, url)
                for link in links:
                    if "spanish" in link.lower() or "photo" in link.lower():
                        continue
                    if link.lower().endswith(".jpg") or link.lower().endswith(".png") or link.lower().endswith(".bmp") or link.lower().endswith(".htm") or link.lower().endswith(".doc") or link.lower().endswith(".docx") or link.lower().endswith(".jpeg"):
                        continue
                    elif link.lower().endswith(".pdf"):
                        response = requests.get(link)
                        pdf = open(os.path.join(self.data_folder,self.url_to_filename(link).replace(".txt", "")), 'wb')
                        pdf.write(response.content)
                        pdf.close()
                        continue
                    self.save_status()
                    self.scrape(link)
            except:
                print("An error occured, but ignored")

        self.save_status()

    def extract_links(self, soup, base_url):
        links = set()
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            full_url = self.normalize_url(urljoin(self.base_url, href))
            if self.is_valid_link(full_url):
                links.add(full_url)
            else:
                f = open("extra-links.txt", "a")
                f.write(full_url + "\n")
                f.close()
        return links

    def is_valid_link(self, url):
        parsed_url = urlparse(url)
        return parsed_url.netloc == self.domain

    def process_page(self, soup, url):
        for script in soup(["script", "style", "nav", "header", "footer"]):
            script.extract()
        main_text = soup.get_text(strip=True)
        main_content = soup.find("main")
        if main_content:
            main_text = main_content.get_text("\n",strip=True)
        filename = self.url_to_filename(url)
        with open(os.path.join(self.data_folder, filename), 'w', encoding='utf-8') as file:
            file.write(main_text)

    def url_to_filename(self, url):
        parsed_url = urlparse(url)
        path = parsed_url.path.strip("/").replace("/", "_")
        if not path:
            path = "index"
        return f"{parsed_url.netloc}_{path}.txt"

    def normalize_url(self, url):
        # Remove fragment identifiers and ensure consistent scheme
        url, _ = urldefrag(url)
        parsed_url = urlparse(url)
        normalized_url = parsed_url._replace(scheme='https', netloc=parsed_url.netloc.lower(), path=parsed_url.path).geturl()
        return normalized_url

    def save_status(self):
        with open(self.status_file, 'w', encoding='utf-8') as file:
            json.dump(self.visited_links, file, indent=4)

base_url = "https://rhs.rocklinusd.org/"
scraper = WebScraper(base_url)
scraper.scrape(base_url)

end = time.time()
total_time = end-start
print("Total time: " + str(total_time))