from telegram import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    Update,
    WebAppInfo,
    ReplyKeyboardRemove
    )

from telegram.ext import CallbackContext, ContextTypes


crawler_url = "https://newscrawler-1.onrender.com/"

async def launch_web_ui(update: Update, callback: CallbackContext):
    kb = [
        [KeyboardButton("Launch News Crawler", web_app=WebAppInfo(crawler_url))]
    ]
    await update.message.reply_text("Let's crawl news...", reply_markup=ReplyKeyboardMarkup(kb))

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""This bot can be used to crawl news from myanmar now.
                                     You need to provide url that you want to crawl and
                                    make sure these are myanmar now's urls""",
                                    reply_markup=ReplyKeyboardRemove());

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused {context.error}")
