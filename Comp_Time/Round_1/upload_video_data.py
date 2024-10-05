import json
import os
from supabase import create_client
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_ANON_KEY")

supabase = create_client(url, key)

INPUT_FILE_PATHS =[
    "./Comp_Time/Round_1/hashtag_results",
    "./Comp_Time/Round_1/keyword_results"
]

def get_all_json_files_in_folders(folder_paths):
    all_files = []
    for folder in folder_paths:
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file.endswith(".json"):
                    all_files.append(os.path.join(root, file))
    return all_files


def main():
    json_files = get_all_json_files_in_folders(INPUT_FILE_PATHS)
    print(len(json_files))
    
    # files_to_process = []
    video_urls = set()
    
    data = []
    for file_path in json_files:
        with open(file_path, 'r') as json_file:
            file_content = json.load(json_file)
            for f in file_content:
                
                if f["video_url"] in video_urls:
                    continue
                
                data.append({
                    "video_url": f["video_url"],
                    "thumbnail": f["thumbnail"],
                    "video_caption": f["video_caption"],
                    "author_username": f["author_username"],
                    "author_profile_link": f["author_profile_link"],
                    "profile_picture_link": f["profile_picture_link"]
                })
                    
                video_urls.add(f["video_url"])
                
        print(file_path)
    
    try:
        response = (
            supabase.table("videos")
            .insert(data)
            .execute()
        )
    except Exception as e:
        print(e)
    
if __name__ == "__main__":
    main()