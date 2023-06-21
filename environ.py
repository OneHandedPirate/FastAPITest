import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER = os.getenv('POSTGRES_USER', 'admin')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'admin')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'db')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
SK = os.getenv('SECRET_KEY', 'not_secured_secret_key')
JWT_EXPIRATION_TIME = int(os.getenv('JWT_EXPIRATION_TIME', '60'))
JTW_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
