import json
from seleniumbase import SB
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

FILE_DIR = "./Comp_Time/Round_1"

HASHTAGS = [
    "traveltok",
    "wanderlust", 
    "backpackingadventures" ,
    "luxurytravel" ,
    "hiddengems" ,
    "solotravel",
    "roadtripvibes" ,
    "travelhacks" ,
    "foodietravel" ,
    "sustainabletravel"
]

CHOSEN_INDEX = 9

def scroll_to_most_bottom(sb, delay=1, max_tries=15):

    last_height = sb.driver.execute_script("return document.documentElement.scrollHeight")
    attempt = 0

    while True:

        sb.scroll_to_bottom()
        sb.driver.sleep(delay)
        
        new_height = sb.driver.execute_script("return document.documentElement.scrollHeight")
        print(last_height, new_height)
        if new_height == last_height:
            if attempt > max_tries:
                break
            else:
                attempt += 1
                if attempt % 3 == 0:
                    sb.scroll_to_top()
                    sb.driver.sleep(2)
                print("Attempt: :",attempt)
        else:
            attempt = 0
        
        last_height = new_height

def main():
    url = f"https://www.tiktok.com/tag/{HASHTAGS[CHOSEN_INDEX]}"
    
    chrome_args = [
        "--autoplay-policy=no-user-gesture-required", 
        "--disable-gpu", 
        "--disable-extensions", 
    ]
    
    with SB(uc=True, headed=True, incognito=True, chromium_arg=chrome_args) as sb:
        
        sb.uc_open_with_reconnect(url, 4)
  
        # search_box = sb.wait_for_element("input[type='search']", timeout=300)
        # search_box.send_keys(HASHTAGS[CHOSEN_INDEX])
        # search_box.send_keys(Keys.RETURN)
        
        sb.driver.sleep(10)
        
        scroll_to_most_bottom(sb)
        
        video_elements = sb.find_elements(By.CSS_SELECTOR, "div.css-x6y88p-DivItemContainerV2.e19c29qe17")
        print(f"Videos Count: {len(video_elements)}") 
        
        videos = []
        
        for video_element in video_elements:
            try:
                try:
                    video_link = video_element.find_element(By.CSS_SELECTOR, 'a.css-1g95xhm-AVideoContainer').get_attribute('href')
                except Exception:
                    video_link = "No video link available"
                
                try:
                    thumbnail_url = video_element.find_element(By.CSS_SELECTOR, 'img[alt]').get_attribute('src')
                except Exception:
                    thumbnail_url = "No thumbnail available"
                
                try:
                    caption = video_element.find_element(By.CSS_SELECTOR, 'span.css-j2a19r-SpanText.efbd9f0').text
                except Exception:
                    caption = "No caption available"
                
                try:
                    hashtags = [tag.text for tag in video_element.find_elements(By.CSS_SELECTOR, 'a[data-e2e="search-common-link"]')]
                except Exception:
                    hashtags = []
                
                try:
                    username = video_element.find_element(By.CSS_SELECTOR, 'p.user-name').text
                except Exception:
                    username = "No username found"
                
                try:
                    user_profile_link = video_element.find_element(By.CSS_SELECTOR, 'a[title]').get_attribute('href')
                except Exception:
                    user_profile_link = "No user profile link available"
                
                try:
                    profile_picture_url = video_element.find_element(By.CSS_SELECTOR, 'img.css-1zpj2q-ImgAvatar').get_attribute('src')
                except Exception:
                    profile_picture_url = "No profile picture available"
                
                if video_link == "No video link available" or caption == "No caption available" or username == "No username found" or user_profile_link=="No user profile link available":
                    continue
                
                video = {
                    "video_url": video_link,
                    "thumbnail": thumbnail_url,
                    "video_caption": caption,
                    "author_username": username,
                    "author_profile_link": user_profile_link,
                    "profile_picture_link": profile_picture_url,
                }
                videos.append(video)
                
            except Exception as e:
                print(f"Error extracting data for a video: {e}")
                continue
        
        print("Final Count: ",len(videos))
        # Save the extracted data to a JSON file
        with open(FILE_DIR + f"/hashtag_results/hashtag_{HASHTAGS[CHOSEN_INDEX]}.json", "w", encoding="utf-8") as f:
            json.dump(videos, f, ensure_ascii=False, indent=4)
        
if __name__ == "__main__":
    main()