import requests
from bs4 import BeautifulSoup

url = "https://docs.google.com/document/d/1VmGf6cu_DeplgjwzSiVuakIIkajq6H1i-p89ClGcqFU/edit?usp=sharing"


def process_page(soup, url):
    for script in soup(["script", "style", "nav", "header", "footer"]):
        script.extract()
    main_text = soup.get_text(strip=True)
    main_content = soup.find("main")
    if main_content:
        main_text = main_content.get_text("\n",strip=True)
    with open("test.txt", 'w', encoding='utf-8') as file:
        file.write(main_text)

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
process_page(soup,url)