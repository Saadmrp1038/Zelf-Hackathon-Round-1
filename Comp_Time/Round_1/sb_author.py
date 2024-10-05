import json
import os
from seleniumbase import SB
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from concurrent.futures import ProcessPoolExecutor, as_completed
from functools import partial

INPUT_FILE_PATHS =[
    "./Comp_Time/Round_1/hashtag_results",
    "./Comp_Time/Round_1/keyword_results"
]

FILE_DIR = "./Comp_Time/Round_1"

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
    
    author_profile_links = set()

    for file_path in json_files:
        with open(file_path, 'r') as json_file:
            file_content = json.load(json_file)
            for f in file_content:
                author_profile_links.add(f["author_profile_link"])
                
    print(len(author_profile_links))
    
    chrome_args = [
        "--autoplay-policy=no-user-gesture-required", 
        "--disable-gpu", 
        "--disable-extensions", 
    ]
    
    users = []
    with SB(uc=True, headed=False, incognito=True, chromium_arg=chrome_args) as sb:
        url = None
        for index, profile_link in enumerate(author_profile_links):
            
            url = profile_link
        
            sb.open(url)
            # sb.driver.sleep(2)
            
            profile_block_element = sb.find_element(By.CSS_SELECTOR, "div.e1457k4r14.css-cooqqt-DivShareLayoutHeader-StyledDivShareLayoutHeaderV2-CreatorPageHeader.enm41492")
            
            try:
                username = profile_block_element.find_element(By.CSS_SELECTOR, 'h1[data-e2e="user-title"]').text
            except NoSuchElementException:
                username = "Not found"
                
            try:
                nickname = profile_block_element.find_element(By.CSS_SELECTOR, 'h2[data-e2e="user-subtitle"]').text
            except NoSuchElementException:
                nickname = "Not found"
                
            try:
                follower_count = profile_block_element.find_element(By.CSS_SELECTOR, 'strong[title="Followers"]').text
            except NoSuchElementException:
                follower_count = "Not found"
                
            try:
                following_count = profile_block_element.find_element(By.CSS_SELECTOR, 'strong[title="Following"]').text
            except NoSuchElementException:
                following_count = "Not found"
                
            try:
                like_count = profile_block_element.find_element(By.CSS_SELECTOR, 'strong[title="Likes"]').text
            except NoSuchElementException:
                like_count = "Not found"
                
            try:
                bio = profile_block_element.find_element(By.CSS_SELECTOR, 'h2[data-e2e="user-bio"]').text
            except NoSuchElementException:
                bio = "Not found"
                
            try:
                profile_image_element = profile_block_element.find_element(By.CSS_SELECTOR, 'img.css-1zpj2q-ImgAvatar.e1e9er4e1')
                profile_picture_link = profile_image_element.get_attribute('src')
            except NoSuchElementException:
                profile_picture_link = "Not found"
                
            
            if username == "Not found" or follower_count == "Not Found" or following_count == "Not Found" or like_count == "Not Found":
                continue
            
            user = {
                "username": username,
                "nickname": nickname,
                "follower_count": follower_count,
                "following_count": following_count,
                "like_count": like_count,
                "bio": bio,
                "profile_picture_link": profile_picture_link
            }
            
            users.append(user)
            with open(FILE_DIR + "/users.json", "w", encoding="utf-8") as f:
                json.dump(users, f, ensure_ascii=False, indent=4)
                
            print(index)
            
    
    
if __name__ == "__main__":
    main()