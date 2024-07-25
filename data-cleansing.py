import os
import time

start = time.time()
directory = 'data/'
output_file = 'cleansed-data/all-data.txt'

if not os.path.exists(output_file):
    os.makedirs("cleansed-data/")

def read_file(filename):
    lines = set()
    with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
        for line in file:
            lines.add(line.strip().replace(u'\xa0', u' '))
    return lines

def add_to_file(lines, filename = ""):
    with open(output_file, 'a', encoding='utf-8') as file:
        file.write(filename+"\n")
        for line in lines:
            file.write(line + '\n')

for filename in os.listdir(directory):
    if "xlsx" in filename or "photo" in filename.lower() or "spanish" in filename.lower() or "jpeg" in filename:
        continue
    if filename.endswith('.txt'):
        print("Cleansing: " + filename)
        lines = read_file(filename)
        add_to_file(lines, filename)

lines_seen = set() # holds lines already seen
outfile = open("cleansed-data/all-data-cleansed.txt", "w", encoding="utf-8")
for line in open("cleansed-data/all-data.txt", "r", encoding="utf-8"):
    if line not in lines_seen: # not a duplicate
        outfile.write(line)
        lines_seen.add(line)
outfile.close()


end = time.time()
total_time = end-start
print("Total time: " + str(total_time))