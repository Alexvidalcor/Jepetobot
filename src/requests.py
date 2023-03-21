# Python libraries
import openai

# Custom modules
from main import *
from src.permissions import UsersFirewall
from src.modules.app_support import openaiToken
from src.db import OperateDb

# Get OpenAI token
openai.api_key = openaiToken


def GenerateResponse(prompt, identity, temp):
    # Import latest connection object
    from src.db import con, cur
    
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

    answerProvided = completions["choices"][0]["message"]["content"]
    

    OperateDb(con, cur, values=("bot", answerProvided), option="insert")

    return answerProvided


@UsersFirewall
async def AiReply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Reply the user message.
    await update.message.reply_text(GenerateResponse(update.message.text, settings["Identity"], settings["Temperature"]))

    


