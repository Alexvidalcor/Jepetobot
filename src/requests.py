# Python libraries
import openai

# Custom modules
from src.modules.app_support import openaiToken

# Get OpenAI token
openai.api_key = openaiToken


def generate_response(prompt):
    completions = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are Jepetobot, an artificial intelligence. Answer as concisely as possible."},
            {"role": "user", "content": prompt}
        ],
        max_tokens = 500,
        n = 1,
        stop = None,
        temperature = 0.6,
    )
    return completions["choices"][0]["message"]["content"]



