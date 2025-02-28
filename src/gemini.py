from google import genai
from google.genai import types

client = genai.Client(api_key="AIzaSyBYgynwsUk3xEsksG7yF07ZuVfbketG-RM")



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
