import os

from dotenv import load_dotenv

config = load_dotenv('.env')

env = os.environ

SPANNER_INSTANCE = env.get("SPANNER_INSTANCE")
SPANNER_DATABASE = env.get("SPANNER_DATABASE")
PROJECT_ID = env.get("PROJECT_ID")

JWT_EXPIRY = int(env.get("JWT_EXPIRY"))
GOOGLE_APPLICATION_CREDENTIALS = env.get("GOOGLE_APPLICATION_CREDENTIALS")
