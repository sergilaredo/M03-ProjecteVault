import os
import time
import sys  # <--- IMPORT IMPORTANT
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options # <--- Necessari per mode headless

# 1. Configuració
ruta_fitxer = os.path.abspath("login.html")
target_url = f"file://{ruta_fitxer}"
passwords = ['1234', 'qwerty', 'admin', 'password123', 'letmein']

# 2. Configuració del Navegador (MODE HEADLESS)
print("[*] Configurant navegador en mode headless...")
chrome_options = Options()
chrome_options.add_argument("--headless=new") # Execució sense pantalla
chrome_options.add_argument("--no-sandbox")

try:
    driver = webdriver.Chrome(options=chrome_options)
except:
    # Fallback bàsic per si no troba Chrome (per local)
    driver = webdriver.Firefox()

# 3. Bucle d'atac
print(f"[*] Iniciant atac contra: {target_url}")

for password in passwords:
    # ... (aquesta part del bucle és igual que abans) ...
    driver.get(target_url)
    
    # Localitzar elements
    driver.find_element(By.ID, "username").clear()
    driver.find_element(By.ID, "username").send_keys("admin")
    
    driver.find_element(By.ID, "password").clear()
    driver.find_element(By.ID, "password").send_keys(password)
    
    driver.find_element(By.ID, "loginBtn").click()
    time.sleep(0.5) # Espera breu
    
    missatge = driver.find_element(By.ID, "message").text
    
    if "ACCESS_GRANTED" in missatge:
        print(f"\n[!!!] VULNERABILITAT CRÍTICA DETECTADA! Password: {password}")
        print("[!!!] Aturant la pipeline per seguretat.")
        driver.quit()
        sys.exit(1) # <--- AQUESTA LÍNIA FA QUE LA PIPELINE SIGUI VERMELLA 🔴
    else:
        print(f"[-] Accés denegat amb: {password}")

driver.quit()
print("[*] No s'han trobat vulnerabilitats.")
sys.exit(0) # Tot correcte
