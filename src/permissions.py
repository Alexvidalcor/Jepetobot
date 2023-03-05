from main import *

# User logging decorator
def UsersFirewall(originalFunction):
    async def CheckPermissions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user = update.message.from_user
        if user["id"] in idUsersAllowed:
            return await originalFunction(update, context)
        await update.message.reply_html(
            rf"Hi {user.mention_html()}!, you don't have permissions {user['id']}"
        )
    return CheckPermissions