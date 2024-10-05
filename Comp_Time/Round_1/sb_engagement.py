import json
from seleniumbase import SB
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

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
    url = f"https://www.tiktok.com/@linustech/video/7414190815712431365"
    
    chrome_args = [
        "--autoplay-policy=no-user-gesture-required", 
        "--disable-gpu", 
        "--disable-extensions", 
    ]
    
    with SB(uc=True, headed=True, incognito=True, chromium_arg=chrome_args) as sb:
        sb.uc_open_with_reconnect(url, 2)
        sb.load_cookies(name="tiktok_cookies.txt")
        sb.refresh_page()
        
        sb.driver.sleep(5)
        
        # Give Like
        like_button = sb.wait_for_element(By.CSS_SELECTOR,"button.css-nmbm7z-ButtonActionItem.edu4zum0 > span[data-e2e='like-icon']", timeout=300)
        like_button.click()
        sb.driver.sleep(5)
        
        # Give Comment
        # comment_box = sb.wait_for_element("div.css-12kupwv-DivContentContainer.ege8lhx2 > div.css-1senhbu-DivLeftContainer.ege8lhx3 > div.css-x4xlc7-DivCommentContainer.ejcng160 > div.css-u4nl1j-DivCommentBarContainer.eqi68xd0 > div > div > div.css-1vplah5-DivLayoutContainer.e1rzzhjk1 > div > div.css-19usix4-DivInputEditorContainer.e1rzzhjk3 > div > div > div.DraftEditor-editorContainer > div > div > div > div > span > br", timeout=300)
        # comment_box.click()
        # comment_box.send_keys("Wow")
        # comment_box.send_keys(Keys.RETURN)
        
        
if __name__ == "__main__":
    main()