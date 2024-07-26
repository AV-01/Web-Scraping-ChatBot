import requests
from bs4 import BeautifulSoup
import os
import time

start = time.time()

lines_seen = set() # holds lines already seen
outfile = open("extra-links-final.txt", "w", encoding="utf-8")
for line in open("extra-links.txt", "r", encoding="utf-8"):
    if line not in lines_seen: # not a duplicate
        outfile.write(line)
        lines_seen.add(line)
outfile.close()

end = time.time()
total_time = end-start
print("Total time: " + str(total_time))