from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# Démarrer ChromeDriver (assure-toi que chromedriver.exe est bien dans le dossier ou dans le PATH)
driver = webdriver.Chrome()

# Aller sur Google
driver.get("https://www.google.com")

# Attendre un peu que la page se charge
time.sleep(2)

# Accepter les cookies si le bouton est là (optionnel)
try:
    consent_btn = driver.find_element(By.XPATH, "//button[contains(., 'Accepter')]")
    consent_btn.click()
except:
    pass  # Aucun bouton trouvé, on continue

# Taper une recherche dans Google
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("Selenium Python")
search_box.submit()

# Attendre quelques secondes
time.sleep(3)

# Fermer le navigateur
driver.quit()

print("✅ Test terminé avec succès !")
