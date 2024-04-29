import os
from dotenv import load_dotenv

load_dotenv()


HOST = "localhost"
MILVUS_PORT = "19530"
MILVUS_USER = "user"
MILVUS_PASSWORD = "Milvus"

MYSQL_USER = "root"
MYSQL_PASSWORD = "MTK022024"
MYSQL_DB = "activity_DB"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ENGINE = "text-embedding-3-large"
