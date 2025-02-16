import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv(dotenv_path=".env")

# Configuaracion de Supabase
SUPABASE_URL = os.getenv("URL")
SUPABASE_KEY = os.getenv("PUBLIC_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
