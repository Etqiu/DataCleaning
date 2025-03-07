from google import genai
from google.genai import types
from config import API_KEY
import time 
import random

client = genai.Client(api_key= API_KEY)


def generate_qa(text: str) -> str:
    """Generate a Q-A based on text with max output tokens being 500"""
    max_retries = 5  # Maximum number of retries
    base_delay = 1  # Base delay in seconds

    for attempt in range(max_retries):
        try:
            # Generate a question based on the input text
            question_response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=f'Generate a short question for the following text with no new lines: {text}',
                 config=types.GenerateContentConfig(
                 max_output_tokens=100)
                
            )
            question = question_response.text.strip()

            answer_response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=f'Provide a short answer for the question with no new lines: {question}',
                config=types.GenerateContentConfig(
                 max_output_tokens=100)
            )
            answer = answer_response.text.strip()

            return question, answer  # Return the generated question and answer as tuple
        except genai.errors.ClientError as e:
            if e.code == 429:  # Check for RESOURCE_EXHAUSTED error
                wait_time = base_delay * (2 ** attempt) + random.uniform(0, 1)  # Exponential backoff with jitter
                print(f"Rate limit exceeded. Retrying in {wait_time:.2f} seconds...")
                time.sleep(wait_time)  
                print(f"Attempt: {attempt}, Base Delay: {base_delay}, Wait Time: {wait_time:.2f}")
                base_delay = wait_time
            else:
                print(f"An error occurred: {e}")
                break  # Break the loop for other errors
        print("Max retries exceeded. Request failed.")
        return None, None 
    