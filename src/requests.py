# Python libraries
import openai

#Custom modules
from src.modules.app_support import openaiToken

# Get OpenAI token 
openai.api_key = openaiToken

def generate_response(prompt):
    completions = openai.Completion.create(
        engine = "text-davinci-003",
        prompt = prompt,
        max_tokens = 200,
        n = 1,
        stop = None,
        temperature=1,
    )
    return completions["choices"][0]["text"]

