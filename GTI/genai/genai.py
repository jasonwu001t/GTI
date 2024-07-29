# genai.py
import openai
from GTI.auth_handler import OpenAIAuth

class GenAI:
    def __init__(self):
        auth = OpenAIAuth()
        openai.api_key = auth.get_api_key()

    def generate_text(self, prompt, max_tokens=150):
        response = openai.Completion.create(
            engine="davinci",
            prompt=prompt,
            max_tokens=max_tokens
        )
        return response.choices[0].text.strip()

if __name__ == "__main__":
    genai = GenAI()
    
    # Example usage
    prompt = "Explain the concept of artificial intelligence."
    generated_text = genai.generate_text(prompt)
    print(generated_text)
