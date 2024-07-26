import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urldefrag
import os
import json
import time

start = time.time()

base_url = "https://rhs.rocklinusd.org/"
domain = urlparse(base_url).netloc
data_folder = "raw-data"
status_file = os.path.join(data_folder, "scraped_links.json")
visited_links = {}

if not os.path.exists(data_folder):
    os.makedirs(data_folder)

if os.path.exists(status_file):
    with open(status_file, 'r', encoding='utf-8') as file:
        visited_links = json.load(file)
else:
    visited_links = {}

def scrape(url):
    if url in visited_links:
        return
    print(f"Scraping: {url}")

    try:
        response = requests.get(url)
        response.raise_for_status()
        visited_links[url] = "success"
    except requests.RequestException as e:
        print(f"Failed to retrieve {url}: {e}")
        visited_links[url] = "failed"
        return

    try:
        soup = BeautifulSoup(response.content, 'html.parser')
        links = extract_links(soup, url)
        process_page(soup, url)
        for link in links:
            if "spanish" in link.lower() or "photo" in link.lower():
                continue
            if link.lower().endswith(".jpg") or link.lower().endswith(".png") or link.lower().endswith(".bmp") or link.lower().endswith(".htm") or link.lower().endswith(".doc") or link.lower().endswith(".docx") or link.lower().endswith(".jpeg"):
                continue
            elif link.lower().endswith(".pdf"):
                response = requests.get(link)
                pdf = open(os.path.join(data_folder,url_to_filename(link).replace(".txt", "")), 'wb')
                pdf.write(response.content)
                pdf.close()
                continue
            save_status()
            scrape(link)
    except:
        print("An error occured, but ignored")

    save_status()

    def extract_links(soup, base_url):
        links = set()
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            full_url = normalize_url(urljoin(base_url, href))
            if is_valid_link(full_url):
                links.add(full_url)
            else:
                f = open("extra-links.txt", "a")
                f.write(full_url + "\n")
                f.close()
        return links

    def is_valid_link(url):
        parsed_url = urlparse(url)
        return parsed_url.netloc == domain

    def process_page(soup, url):
        for script in soup(["script", "style", "nav", "header", "footer"]):
            script.extract()
        main_text = soup.get_text(strip=True)
        main_content = soup.find("main")
        if main_content:
            main_text = main_content.get_text("\n",strip=True)
        filename = url_to_filename(url)
        with open(os.path.join(data_folder, filename), 'w', encoding='utf-8') as file:
            file.write(main_text)

    def url_to_filename(url):
        parsed_url = urlparse(url)
        path = parsed_url.path.strip("/").replace("/", "_")
        if not path:
            path = "index"
        return f"{parsed_url.netloc}_{path}.txt"

    def normalize_url(url):
        url, _ = urldefrag(url)
        parsed_url = urlparse(url)
        normalized_url = parsed_url._replace(scheme='https', netloc=parsed_url.netloc.lower(), path=parsed_url.path).geturl()
        return normalized_url

    def save_status(self):
        with open(status_file, 'w', encoding='utf-8') as file:
            json.dump(visited_links, file, indent=4)

end = time.time()
total_time = end-start
print("Total time: " + str(total_time))