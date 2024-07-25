from PyPDF2 import PdfReader
import os
import time

start = time.time()
directory = 'data/'
output_file = 'cleansed-data/all-data-pdf.txt'


def add_to_file(lines, filename = ""):
    with open(output_file, 'a', encoding='utf-8') as file:
        file.write(filename.replace(".pdf","")+"\n")
        file.write(lines + '\n')

for filename in os.listdir(directory):
    if filename.endswith('.pdf'):
        print("Cleansing: " + filename)
        try:
            pdf_reader = PdfReader("data/"+filename)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
                add_to_file(text.strip(), filename)
        except:
            continue

end = time.time()
total_time = end-start
print("Total time: " + str(total_time))