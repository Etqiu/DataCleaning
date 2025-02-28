import pdfplumber 
import pytesseract 
import re  # regex 
from PIL import Image
import json 
from gemini import questionGenerator as question 
from gemini import answerGenerator as answer 


def clean_text(text: str) -> str:
    text = re.sub(r'[^\w\s]', '', text) # Remove special characters
    text = re.sub(r'\s+', ' ', text).strip() # Normalize whitespace
    # Remove common research paper patterns
    text = re.sub(r'\[\d+\]', '', text) # Remove citation brackets like [1]
    text = re.sub(r'\(.*?et al., \d{4}\)', '', text) # Remove author citations
    text = re.sub(r'^(Author:|Date:)\s.*$', '', text)
    text = re.sub(r'Page \d of \d+', '', text) # remove page of # 
   ## text = re.sub(r'https?[^ ]*', '', text) ## remove https

    return text

text_data = []
with pdfplumber.open('data/A review of deep learning-based stereo vision techniques.pdf') as pdf:
    for i, page in enumerate(pdf.pages): 
        text = page.extract_text() 
        text = clean_text(text)
        insert_question = question(text)
        if i == 2: 
            break
        page_data = {
            "text": text, 
            "question" : insert_question,
            "answer": answer(insert_question),
            "source": 'A review of deep learning-based stereo vision techniques.pdf',
            "metadata": {
                "section": f'Page {1 + i}'
                         }
        }
        text_data.append(page_data)

with open('text.json', 'w') as json_file: 
    json.dump(text_data, json_file, indent=4)
