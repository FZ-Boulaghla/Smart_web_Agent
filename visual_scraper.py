from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
import pytesseract
import time
import uuid
import os

os.makedirs("screenshots", exist_ok=True)

def extract_text_visual(url):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        time.sleep(3)
        screenshot_path = f"screenshots/{uuid.uuid4()}.png"
        driver.save_screenshot(screenshot_path) # full page screen options

        img = Image.open(screenshot_path)
        text = pytesseract.image_to_string(img) #search pytesseract for the ppt 
        # add full page screens
        return {
            "url": url,
            "ocr_text": text
        }
    finally:
        driver.quit()
