from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.environ['DATABASE_URL']
REDIS_HOST = os.environ['REDIS_HOST']
REDIS_PORT = int(os.environ['REDIS_PORT'])
REDIS_DB = int(os.environ['REDIS_DB'])
GMAIL_APP_PASSWORD = os.environ['GMAIL_APP_PASSWORD']
APP_EMAIL = os.environ['APP_EMAIL']
JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']
ENCODING_ALGORITHM = os.environ['ENCODING_ALGORITHM']
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ['ACCESS_TOKEN_EXPIRE_MINUTES'])
TOKEN_TYPE = os.environ['TOKEN_TYPE']
HASH_SCHEME = os.environ['HASH_SCHEME']
OTP_EXPIRY_MINUTES = int(os.environ['OTP_EXPIRY_MINUTES'])
SMTP_HOST = os.environ['SMTP_HOST']
SMTP_PORT = int(os.environ['SMTP_PORT'])