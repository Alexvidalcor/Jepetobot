# Custom importation
from src.modules import stats
from src.env.app_secrets_env import idAdminAllowed, idUsersAllowed
from main import Update, ContextTypes


# User logging decorator
def UsersFirewall(originalFunction):
    async def CheckPermissions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if update.message != None:
            user = update.message.from_user
            if user["id"] in idUsersAllowed and stats.CheckTokenLimit(user["username"], user["id"]) == None or stats.CheckTokenLimit(user["username"], user["id"]):
                return await originalFunction(update, context)
            await update.message.reply_html(
                rf"Hi {user.mention_html()}! You don't have permissions or have exceeded a maximum token limit. ({user['id']})"
            )
        else:
            return await originalFunction(update, context) 

    return CheckPermissions


# Adminlogging decorator
def AdminFirewall(originalFunction):
    async def CheckPermissions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if update.message != None:
            admin = update.message.from_user
            if admin["id"] in idAdminAllowed:
                return await originalFunction(update, context)
            await update.message.reply_html(
                rf"Hi {admin.mention_html()}!, you don't have admin permissions {admin['id']}"
            )
        else:
            return await originalFunction(update, context) 

    return CheckPermissions






