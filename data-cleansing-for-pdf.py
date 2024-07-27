from PyPDF2 import PdfReader
import os
import time

start = time.time()
directory = 'raw-data/'
output_file = 'cleansed-data/all-data-pdf.txt'


def add_to_file(lines, filename = ""):
    with open(output_file, 'a', encoding='utf-8') as file:
        file.write(filename.replace(".pdf","")+"\n")
        file.write(lines + '\n')

for filename in os.listdir(directory):
    if filename.endswith('.pdf'):
        if "spanish" in filename.lower() or "map" in filename.lower() or "w-9" in filename.lower() or "swim" in filename.lower() or "table" in filename.lower():
            continue
        print("Cleansing: " + filename)
        try:
            pdf_reader = PdfReader("raw-data/"+filename)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
                add_to_file(text.strip(), filename)
        except Exception as e:
            print(e)
            continue

lines_seen = set() # holds lines already seen
outfile = open("cleansed-data/all-data-pdf-final.txt", "w", encoding="utf-8")
for line in open("cleansed-data/all-data-pdf.txt", "r", encoding="utf-8"):
    if line not in lines_seen: # not a duplicate
        outfile.write(line)
        lines_seen.add(line)
outfile.close()

end = time.time()
total_time = end-start
print("Total time: " + str(total_time))