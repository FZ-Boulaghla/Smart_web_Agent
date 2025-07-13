from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time


driver = webdriver.Chrome()

# Aller sur Google
driver.get("https://www.google.com")

time.sleep(2)

try:
    consent_btn = driver.find_element(By.XPATH, "//button[contains(., 'Accepter')]")
    consent_btn.click()
except:
    pass 

# Taper une recherche dans Google
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("Selenium Python")
search_box.submit()

time.sleep(3)

driver.quit()

print(" Test terminé avec succès !")
