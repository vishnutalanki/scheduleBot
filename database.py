import os
import asyncpg
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

# Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Create Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Async DB connection
async def get_db_connection():
    return await asyncpg.connect(SUPABASE_URL, ssl="require")