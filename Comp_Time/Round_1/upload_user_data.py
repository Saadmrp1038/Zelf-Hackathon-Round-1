import json
import os
from supabase import create_client
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_ANON_KEY")

supabase = create_client(url, key)

INPUT_FILE_PATH ="./Comp_Time/Round_1/users.json"

def main():

    data = []
    with open(INPUT_FILE_PATH, 'r') as json_file:
        file_content = json.load(json_file)
        for f in file_content:
            tmp = None
            
            # print(f["follower_count"], f["following_count"], f["like_count"])
            
            tmp = f["follower_count"]
            tmp = str(f["follower_count"])
            if "K" in tmp:
                tmp = tmp.split("K")[0]
                tmp = float(tmp) * 1000
                tmp = int(tmp)
            elif "M" in  tmp:
                tmp = tmp.split("M")[0]
                tmp = float(tmp) * 1000000
                tmp = int(tmp)
            elif "B" in  tmp:
                tmp = tmp.split("B")[0]
                tmp = float(tmp) * 1000000000
                tmp = int(tmp)
            else:
                tmp = float(tmp)
                tmp = int(tmp)
            f["follower_count"] = tmp
            
            tmp = str(f["following_count"])
            if "K" in tmp:
                tmp = tmp.split("K")[0]
                tmp = float(tmp) * 1000
                tmp = int(tmp)
            elif "M" in tmp:
                tmp = tmp.split("M")[0]
                tmp = float(tmp) * 1000000
                tmp = int(tmp)
            elif "B" in tmp:
                tmp = tmp.split("B")[0]
                tmp = float(tmp) * 1000000000
                tmp = int(tmp)
            else:
                tmp = float(tmp)
                tmp = int(tmp)
            f["following_count"] = tmp
            
            tmp = str(f["like_count"])
            if "K" in tmp:
                tmp = tmp.split("K")[0]
                tmp = float(tmp) * 1000
                tmp = int(tmp)
            elif "M" in tmp:
                tmp = tmp.split("M")[0]
                tmp = float(tmp) * 1000000
                tmp = int(tmp)
            elif "B" in tmp:
                tmp = tmp.split("B")[0]
                tmp = float(tmp) * 1000000000
                tmp = int(tmp)
            else:
                tmp = float(tmp)
                tmp = int(tmp)
            f["like_count"] = tmp
            
            # print(f["follower_count"], f["following_count"], f["like_count"])
            
            data.append({
                "username": f["username"],
                "nickname": f["nickname"],
                "follower_count": f["follower_count"],
                "following_count": f["following_count"],
                "like_count": f["like_count"],
                "bio": f["bio"],
                "profile_picture_link": f["profile_picture_link"]
            })
            
                                
    try:
        response = (
            supabase.table("authors")
            .insert(data)
            .execute()
        )
    except Exception as e:
        print(e)
    
if __name__ == "__main__":
    main()