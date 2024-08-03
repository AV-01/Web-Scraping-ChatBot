import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urldefrag
import os
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

start = time.time()

class WebScraper:
    def __init__(self, base_url, data_folder, ignore_patterns = [], ignore_extensions = ["jpg","xml","xlsx","png","bmp","htm","doc","dox","jpeg"]):
        self.base_url = base_url
        self.domain = urlparse(base_url).netloc
        self.data_folder = data_folder
        self.status_file = os.path.join(self.data_folder, "scraped_links.json")
        self.ignore_patterns = ignore_patterns
        self.ignore_extensions = ignore_extensions

        # Create the data folder if it doesn't exist
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)

        # Load visited links from status file or initialize an empty dictionary
        if os.path.exists(self.status_file):
            with open(self.status_file, 'r', encoding='utf-8') as file:
                self.visited_links = json.load(file)
        else:
            self.visited_links = {}
        self.lock = Lock()

    def should_ignore_link(self, link):
        for extension in self.ignore_extensions:
            if link.lower().endswith(extension):
                return True
        for pattern in self.ignore_patterns:
            if pattern in link.lower():
                return True
        return False

    def download_pdf(self,url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            normalized_url = self.normalize_url(url)
            filename = self.url_to_filename(normalized_url).replace(".txt", ".pdf")
            with open(os.path.join(self.data_folder, filename), 'wb') as pdf_file:
                pdf_file.write(response.content)
            with self.lock:
                self.visited_links[normalized_url] = "success"
        except requests.RequestException as e:
            print(f"Failed to download PDF {url}: {e}")
            with self.lock:
                self.visited_links[normalized_url] = "failed"
    def scrape(self, url):
        normalized_url = self.normalize_url(url)
        with self.lock:
            if normalized_url in self.visited_links:
                return
        self.visited_links[normalized_url] = "pending"
        print(f"Scraping: {url}")

        try:
            response = requests.get(url)
            response.raise_for_status()
            with self.lock:
                self.visited_links[normalized_url] = "success"
        except requests.RequestException as e:
            print(f"Failed to retrieve {url}: {e}")
            with self.lock:
                self.visited_links[normalized_url] = "failed"
            return

        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            links = self.extract_links(soup, url)
            self.process_page(soup, url)
            futures = []
            with ThreadPoolExecutor(max_workers=10) as executor:
                for link in links:
                    if self.should_ignore_link(link):
                        continue
                    if link.lower().endswith(".pdf"):
                        futures.append(executor.submit(self.download_pdf, link))
                    else:
                        futures.append(executor.submit(self.scrape, link))
                for future in as_completed(futures):
                    future.result()
        except Exception as e:
            print(f"{e}")

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
scraper = WebScraper(base_url, data_folder="rhs-data",ignore_patterns=["spanish","photo"])
scraper.scrape(base_url)

end = time.time()
total_time = end-start
print("Total time: " + str(total_time))