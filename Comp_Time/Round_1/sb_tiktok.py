import json
from seleniumbase import SB
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

FILE_DIR = "./TikTok"

def main():
    url = f"https://www.tiktok.com/login/phone-or-email/email"
    
    with SB(uc=True, headed=True) as sb:
     
        # Thie section is only for saving cookies
        sb.uc_open_with_reconnect(url, 4)
        sb.type("input[name='username']","siamai462")
        sb.type("input[type='password']","zucced#990")
        sb.click("button[type='submit']")
        
        sb.driver.sleep(20)
        sb.save_cookies(name="tiktok_cookies.txt")
            
        
if __name__ == "__main__":
    main()