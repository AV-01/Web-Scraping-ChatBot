import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urldefrag
import os
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock


start = time.time()

base_url = "https://rhs.rocklinusd.org/"
domain = urlparse(base_url).netloc
data_folder = "test-data"
status_file = os.path.join(data_folder, "scraped_links.json")
visited_links = {}
lock = Lock()

if not os.path.exists(data_folder):
    os.makedirs(data_folder)

if os.path.exists(status_file):
    with open(status_file, 'r', encoding='utf-8') as file:
        visited_links = json.load(file)
else:
    visited_links = {}

# Make sure the url is from the same domain as the original base_url
def is_valid_link(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc == domain

# Extract all the links from a website
def extract_links(soup):
    links = set()
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        full_url = urljoin(base_url, href)
        if is_valid_link(full_url):
            links.add(full_url)
        else:
            f = open("extra-links.txt", "a")
            f.write(full_url + "\n")
            f.close()
    return links

# Turn url to filename
def url_to_filename(url):
    parsed_url = urlparse(url)
    path = parsed_url.path.strip("/").replace("/", "_")
    if not path:
        path = "index"
    return f"{parsed_url.netloc}_{path}.txt"

# Saves the visited links file to the visited_links json file
def save_status():
    with open(status_file, 'w', encoding='utf-8') as file:
        json.dump(visited_links, file, indent=4)

def download_pdf(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        filename = url_to_filename(url).replace(".txt", ".pdf")
        with open(os.path.join(data_folder, filename), 'wb') as pdf_file:
            pdf_file.write(response.content)
        with lock:
            visited_links[url] = "success"
    except requests.RequestException as e:
        print(f"Failed to download PDF {url}: {e}")
        with lock:
            visited_links[url] = "failed"

# Takes the page, gets all the text, and saves it to a txt file
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

def scrape(url):
    with lock:
        if url in visited_links:
            return
        visited_links[url] = "pending"
    print(f"Scraping: {url}")

    try:
        response = requests.get(url)
        response.raise_for_status()
        with lock:
            visited_links[url] = "success"
    except requests.RequestException as e:
        print(f"Failed to retrieve {url}: {e}")
        with lock:
            visited_links[url] = "failed"
        return

    try:
        soup = BeautifulSoup(response.content, 'html.parser')
        links = extract_links(soup)
        process_page(soup, url)
        futures = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            for link in links:
                if "spanish" in link.lower() or "photo" in link.lower():
                    continue
                if link.lower().endswith(".jpg") or link.lower().endswith(".png") or link.lower().endswith(".bmp") or link.lower().endswith(".htm") or link.lower().endswith(".doc") or link.lower().endswith(".docx") or link.lower().endswith(".jpeg"):
                    continue
                if link.lower().endswith(".pdf"):
                    futures.append(executor.submit(download_pdf, link))
                else:
                    futures.append(executor.submit(scrape, link))
            for future in as_completed(futures):
                future.result()
    except:
        print("An error occured, but ignored")

    save_status()


scrape(base_url)

end = time.time()
total_time = end-start

print("Total time: " + str(total_time))