import os
if os.path.exists(".env"):
    from dotenv import load_dotenv
    load_dotenv()

BOT_TOKEN = os.getenv('TELE_BOT_TOKEN')
BOT_USERNAME = os.getenv('TELE_BOT_USERNAME')
