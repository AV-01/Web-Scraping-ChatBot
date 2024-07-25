import os
import time

start = time.time()
directory = 'data/'
output_file = 'cleansed-data/all-data.txt'

if not os.path.exists(output_file):
    os.makedirs("cleansed-data/")

def read_file(filename):
    lines = set()
    with open(os.path.join(directory, filename), 'r') as file:
        for line in file:
            lines.add(line.strip())
    return lines

def add_to_file(lines):
    with open(output_file, 'a') as file:
        for line in lines:
            file.write(line + '\n')

for filename in os.listdir(directory):
    if filename.endswith('.txt'):
        print("Cleansing: " + filename)
        lines = read_file(filename)
        add_to_file(lines)

end = time.time()
total_time = end-start
print("Total time: " + total_time)