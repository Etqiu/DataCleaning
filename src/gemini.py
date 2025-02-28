from google import genai
from google.genai import types
from config import API_KEY
import time 
import random

client = genai.Client(api_key= API_KEY)
max_retries = 5 
base_delay = 1 

def questionGenerator(text: str) -> str:
    
    response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=f'Write a short question for this text:{text}' ,

    )
    return response.text

def answerGenerator(question: str) -> str: 
    response =  client.models.generate_content(
    model="gemini-2.0-flash",
    contents=f'Write a short answer for this text, with no newlines:{question}', 
    config=types.GenerateContentConfig(
        max_output_tokens=500)
    ) 
    return response.text

print(answerGenerator('hello!'))