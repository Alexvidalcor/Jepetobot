# Python libraries
import openai

# Custom modules
from src.modules.app_support import openaiToken

# Get OpenAI token
openai.api_key = openaiToken


def generate_response(prompt, identity, temp):
    completions = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": identity},
            {"role": "user", "content": prompt}
        ],
        max_tokens = 500,
        n = 1,
        stop = None,
        temperature = temp,
    )
    return completions["choices"][0]["message"]["content"]



