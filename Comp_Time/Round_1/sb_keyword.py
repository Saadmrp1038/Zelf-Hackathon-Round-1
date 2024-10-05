import json
from seleniumbase import SB
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

FILE_DIR = "./Comp_Time/Round_1"

KEYWORDS = [
    "beautiful destinations",
    "places to visit",
    "places to travel",
    "places that don't feel real",
    "travel hacks",
]

CHOSEN_INDEX = 0

def scroll_to_most_bottom(sb, delay=1, max_tries=5):

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
                print("Attempt: :",attempt)
        else:
            attempt = 0
        
        last_height = new_height

def main():
    url = f"https://www.tiktok.com"
    
    chrome_args = [
        "--autoplay-policy=no-user-gesture-required", 
        "--disable-gpu", 
        "--disable-extensions", 
    ]
    
    
    with SB(uc=True, headed=True, incognito=True, chromium_arg=chrome_args) as sb:
        
        for i in range(0,5):
            CHOSEN_INDEX = i
            sb.uc_open_with_reconnect(url, 4)
    
            search_box = sb.wait_for_element("input[type='search']", timeout=300)
            search_box.send_keys(KEYWORDS[CHOSEN_INDEX])
            search_box.send_keys(Keys.RETURN)
            
            sb.driver.sleep(10)
            
            # Switch to videos tab
            try:
                users_tab = sb.find_element(By.CSS_SELECTOR, "div[aria-controls='tabs-0-panel-search_video']")
                users_tab.click()
                print("Clicked on the 'Videos' tab successfully.")
            except Exception as e:
                print(f"Error clicking the 'Videos' tab: {e}")

            sb.driver.sleep(3)
            
            scroll_to_most_bottom(sb)
            
            video_elements = sb.find_elements(By.CSS_SELECTOR, "div.css-1soki6-DivItemContainerForSearch.e19c29qe19")
            print(f"Videos Count: {len(video_elements)}") 
            
            videos = []
            
            for video_element in video_elements:
                try:

                    try:
                        video_link = video_element.find_element(By.CSS_SELECTOR, "div.css-13fa1gi-DivWrapper.e1cg0wnj1 > a").get_attribute("href")
                    except Exception:
                        video_link = "No video link available"
                    
                    try:
                        thumbnail_url = video_element.find_element(By.CSS_SELECTOR, "picture img").get_attribute("src")
                    except Exception:
                        thumbnail_url = "No thumbnail available"
                    
                    try:
                        caption = video_element.find_element(By.CSS_SELECTOR, "h1.css-6opxuj-H1Container.ejg0rhn1 > span.css-j2a19r-SpanText.efbd9f0").text
                    except Exception:
                        caption = "No caption available"
                    
                    try:
                        thumbnail_alt = video_element.find_element(By.CSS_SELECTOR, "picture img").get_attribute("alt")
                    except Exception:
                        thumbnail_alt = "No thumbnail alt available"
                    
                    try:
                        hashtags = [hashtag.text for hashtag in video_element.find_elements(By.CSS_SELECTOR, "h1.css-6opxuj-H1Container.ejg0rhn1 > a[data-e2e='search-common-link' ")]
                    except Exception:
                        hashtags = []
                    
                    try:
                        user_link = video_element.find_element(By.CSS_SELECTOR, "a[href^='/@']").get_attribute("href")
                    except Exception:
                        user_link = "No user link available"
                    
                    try:
                        username = video_element.find_element(By.CSS_SELECTOR, "p[data-e2e='search-card-user-unique-id']").text
                    except Exception:
                        username = "No username found"
                    
                    try:
                        like_count = video_element.find_element(By.CSS_SELECTOR, "strong.css-ws4x78-StrongVideoCount").text
                    except Exception:
                        like_count = "No like count available"
                    
                    try:
                        post_date = video_element.find_element(By.CSS_SELECTOR, "div.css-dennn6-DivTimeTag").text
                    except Exception:
                        post_date = "No post date available"
                        
                    try:
                        profile_picture_url = video_element.find_element(By.CSS_SELECTOR, 'div.css-dq7zy8-DivUserInfo.etrd4pu5 span.css-tuohvl-SpanAvatarContainer.e1e9er4e0 > img').get_attribute('src')
                    except Exception:
                        profile_picture_url = "No profile picture available" 
                        
                    if video_link == "No video link available" or caption == "No caption available" or username == "No username found" or user_link=="No user link available":
                        continue
                    
                    video = {
                        "video_url": video_link,
                        "thumbnail": thumbnail_url,
                        "video_caption": caption,
                        "author_username": username,
                        "author_profile_link": user_link,
                        "video_like_count": like_count,
                        "post_date": post_date,
                        "profile_picture_link": profile_picture_url,
                    }
                    videos.append(video)
                    
                except Exception as e:
                    print(f"Error extracting data for a video: {e}")
                    continue
            
            print(f"Final Count {KEYWORDS[CHOSEN_INDEX]}: ",len(videos))
            # Save the extracted data to a JSON file
            with open(FILE_DIR + f"/keyword_results/keyword_{KEYWORDS[CHOSEN_INDEX]}.json", "w", encoding="utf-8") as f:
                json.dump(videos, f, ensure_ascii=False, indent=4)
        
if __name__ == "__main__":
    main()