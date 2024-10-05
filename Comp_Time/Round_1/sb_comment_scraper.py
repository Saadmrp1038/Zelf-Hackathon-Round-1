import json
from seleniumbase import SB
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

FILE_DIR = "./Comp_Time/Round_1"

def scroll_to_load_all_comments(sb, delay=1, max_tries=5):
    last_comment_count = 0
    tries = 0

    while tries < max_tries:
        current_comment_elements = sb.find_elements(By.CSS_SELECTOR, "div.css-13wx63w-DivCommentObjectWrapper.ezgpko42")
        current_comment_count = len(current_comment_elements)
        
        sb.scroll_to_bottom()
        sb.driver.sleep(delay)

        if current_comment_count == last_comment_count:
            tries += 1
            print(f"No new comments, attempt: {tries}")
        else:
            tries = 0 

        last_comment_count = current_comment_count

        print(f"Comments loaded: {current_comment_count}")

    return current_comment_elements 
        
def main():
    url = f"https://www.tiktok.com/@linustech/video/7414190815712431365"
    
    chrome_args = [
        "--autoplay-policy=no-user-gesture-required", 
        "--disable-gpu", 
        "--disable-extensions", 
    ]
    
    with SB(uc=True, headed=True, incognito=True, chromium_arg=chrome_args) as sb:
        sb.uc_open_with_reconnect(url, 2)
        sb.driver.sleep(10)
        
        scroll_to_load_all_comments(sb)
        
        
        comment_elements = sb.find_elements(By.CSS_SELECTOR,"div.css-13wx63w-DivCommentObjectWrapper.ezgpko42")
        print("Comment Count: ", len(comment_elements))
        
        comments = []
        for index,comment in enumerate(comment_elements):

            try:
                user_element = comment.find_element(By.CSS_SELECTOR, "div.css-13x3qpp-DivUsernameContentWrapper a")
                username = user_element.find_element(By.CSS_SELECTOR, "span").text
                user_profile_link = user_element.get_attribute("href")  # Get the href attribute for user profile link
            except:
                username = "Not Found"
                user_link = "Not Found"
            
            try:
                comment_text = comment.find_element(By.CSS_SELECTOR, "span[data-e2e='comment-level-1']").text
            except:
                comment_text = "Not Found"

            comment = {
                "username": username,
                "user_profile_link": user_profile_link,
                "comment_text": comment_text
            }
            
            comments.append(comment)
            print(index)
        
        with open(f"{FILE_DIR}/comments.json", "w",) as f:
            json.dump(comments, f, indent=4)
        
if __name__ == "__main__":
    main()