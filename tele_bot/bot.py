from telegram.ext import ApplicationBuilder, CommandHandler

from .credentials import BOT_TOKEN, BOT_USERNAME
from .handlers import error, help_cmd, launch_web_ui

if __name__ == '__main__':
    # create the bot from the token
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler('start', launch_web_ui))
    application.add_handler(CommandHandler('help', help_cmd))

    application.add_error_handler(error)

    # and send the bot on its way!
    print(f"Your bot is listening! Navigate to http://t.me/{BOT_USERNAME} to interact with it!")
    application.run_polling()
