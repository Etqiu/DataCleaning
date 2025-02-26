import pdfplumber 
import pytesseract 
import re  # regex 
from PIL import Image
import json 

def clean_text(text: str) -> str:
    text = re.sub(r'[^\w\s]', '', text) # Remove special characters
    text = re.sub(r'\s+', ' ', text).strip() # Normalize whitespace
    # Remove common research paper patterns
    text = re.sub(r'\[\d+\]', '', text) # Remove citation brackets like [1]
    text = re.sub(r'\(.*?et al., \d{4}\)', '', text) # Remove author citations
    return text

text_data = []
with pdfplumber.open('data/A review of deep learning-based stereo vision techniques.pdf') as pdf:
    for i, page in enumerate(pdf.pages): 
        text = page.extract_text() 
        text = clean_text(text)

        page_data = {
            "text": text, 
            "metadata": {
                "source": 'A review of deep learning-based stereo vision techniques.pdf',
                "section": f'Page {1 + i}'
                         }
        }
        text_data.append(page_data)

with open('text.json', 'w') as json_file: 
    json.dump(text_data, json_file, indent=4)
