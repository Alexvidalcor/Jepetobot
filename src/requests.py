# Python libraries
import openai

# Custom modules
from main import *
from src.permissions import UsersFirewall
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
        temperature = float(temp),
    )
    return completions["choices"][0]["message"]["content"]

@UsersFirewall
async def AiReply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Reply the user message.
    await update.message.reply_text(generate_response(update.message.text, settings["Identity"], settings["Temperature"]))

