import pdfplumber 
import pytesseract 

with pdfplumber.open('data/A review of deep learning-based stereo vision techniques.pdf') as pdf:
    for page in pdf.pages: 
        text = page.extract_text() 
        print(text)

 
