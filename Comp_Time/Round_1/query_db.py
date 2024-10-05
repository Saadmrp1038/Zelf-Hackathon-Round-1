import json
import os
from supabase import create_client
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_ANON_KEY")

supabase = create_client(url, key)

res1 = supabase.table("authors").select("*").gte("follower_count", 100000).execute()

res2 = supabase.table("authors").select("*").gte("like_count", 1000000).execute()

# print("Users with more than 100k follower: ")
with open("100k_followe.json", "w", encoding="utf-8") as f:
        json.dump(res1.data, f, ensure_ascii=False, indent=4)

# print("Users with more than 1M follower: ")
with open("1M_like.json", "w", encoding="utf-8") as f:
        json.dump(res2.data, f, ensure_ascii=False, indent=4)