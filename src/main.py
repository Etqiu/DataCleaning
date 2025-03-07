import pdfplumber 
import pytesseract 
import re  # regex 
from PIL import Image
import json 
from gemini import generate_qa  
from gemini import answerGenerator as answer 
import pymupdf4llm
import time 
import os

start_time = time.time()

def clean_text(text: str) -> str:
    """
    Using common regex patterns to extract text
    """
    text = re.sub(r'[^\w\s]', '', text) # Remove special characters
    text = re.sub(r'\s+', ' ', text).strip() # Normalize whitespace
    # Remove common research paper patterns
    text = re.sub(r'\[\d+\]', '', text) # Remove citation brackets like [1]
    text = re.sub(r'\(.*?et al., \d{4}\)', '', text) # Remove author citations
    text = re.sub(r'^(Author:|Date:)\s.*$', '', text)
    text = re.sub(r'Page \d of \d+', '', text) # remove page of # 
   ## text = re.sub(r'https?[^ ]*', '', text) ## remove https
    text = text.strip()
    return text

def process_pdfs(pdf_files, output_json):
    """
    Goes through pdf_files, a list of directories 
    for the pdfs, and the name of the output
    """
    for i in range(len(pdf_files)):
        text_data = []
        with pdfplumber.open(pdf_files[i]) as pdf:
            pdf_name = os.path.basename(pdf_files[i]).replace('.pdf', '')

            for j, page in enumerate(pdf.pages): 
                text = page.extract_text() 
                text = clean_text(text)
                #q_a = generate_qa(text[:1000]) # the first 1000 characters, generate q and a
                #ans = q_a[1] 
                #ques = q_a[0] 
                #if j == 2: # trying out a few entries
                 #   break
                page_data = {
                   "text": text, 
                  #  "question" : ques,
                   # "answer": ans,
                 "source": str(pdf.path),
                    "metadata": {
                        "section": f'Page {1 + j}'
                         }
                }
                text_data.append(page_data) 

            with open(pdf_name + ' ' +  output_json, 'w') as json_file:  # make new json file called text.json
                json.dump(text_data, json_file, indent=4) #  put the textdata in json file

def get_directory_pdfs(directory: str) -> list: 
    """
    Returns a list of items paths inside the directories
    """
    pdfs = []
    for pdf in os.listdir(directory):
        pdfs.append(directory + pdf)
    return pdfs

def extract_as_md(pdf_path): 
    """Extract text from pdf into markdown (Credit: Sean)"""
    md_text = pymupdf4llm.to_markdown(pdf_path, write_images=False)  # Extract structured text
    return md_text


process_pdfs(get_directory_pdfs('data'), 'text.json') 
end_time = time.time() 
runtime = end_time - start_time
print(f'Runtime: {runtime:.6f} seconds')


#TODO use the new module for pdf extraction. 