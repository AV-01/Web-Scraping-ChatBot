import requests
from bs4 import BeautifulSoup


# Making a GET request
r = requests.get('https://rhs.rocklinusd.org/Counseling/Class-of-2025/index.html')

# check status code for response received
# success code - 200
print(r)

# Parsing the HTML
soup = BeautifulSoup(r.content, 'html.parser')

# s = soup.find('div', class_='col')
content = soup.find_all('href')
# s1 = soup.find('div', class_='col')

print(content)
