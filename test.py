import requests
from bs4 import BeautifulSoup


# Making a GET request
r = requests.get('https://rhs.rocklinusd.org/RegistrarTranscripts/index.html')

# check status code for response received
# success code - 200
print(r)

# Parsing the HTML
soup = BeautifulSoup(r.content, 'html.parser')

# s = soup.find('div', class_='col')
content_h1 = soup.find_all('h1')
content_h2 = soup.find_all('h2')
content_h3 = soup.find_all('h3')
content_h4 = soup.find_all('h4')
content_h5 = soup.find_all('h5')
content_h6 = soup.find_all('h6')
content_p = soup.find_all('p')
content_div = soup.find_all('div')

all_content = [content_h1, content_h2, content_h3, content_h4, content_h5, content_h6, content_p, content_div]
# s1 = soup.find('div', class_='col')

for content in all_content:
    for words in content:
        print(words.get_text().strip())
# print(all_content[0][0].get_text())
