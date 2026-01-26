import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# 1. Configuración del Navegador (Chrome) para CI/CD y Local
options = Options()
options.add_argument('--headless') # Obligatorio para GitHub Actions
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--window-size=1920,1080')

driver = webdriver.Chrome(options=options)

# 2. Ruta absoluta al archivo login.html
file_path = "file://" + os.path.abspath("login.html")

# Llista de contrasenyes per a l'atac (el diccionari)
passwords = ['1234', 'qwerty', 'admin', 'password123', 'letmein']

try:
    for pwd in passwords:
        driver.get(file_path)
        # Espera un momento para asegurar que la página carga
        time.sleep(0.5)

        # Inyectar credenciales (Usuario: admin)
        driver.find_element(By.ID, "username").send_keys("admin")
        driver.find_element(By.ID, "password").send_keys(pwd)

        # Clicar botón de entrar
        driver.find_element(By.ID, "loginBtn").click()

        # Pequeña espera para que el script de la web procese el login
        time.sleep(0.5)

        # Comprobar si aparece el mensaje de éxito
        result_message = driver.find_element(By.ID, "message").text
        print(f"Provant contrasenya: {pwd} -> Resultat: {result_message}")

        if "ACCESS_GRANTED" in result_message:
            print("\n!!! VULNERABILITAT TROBADA !!!")
            print(f"La contrasenya és: {pwd}")

            # Captura de pantalla automática
            driver.save_screenshot('hacked.png')
            print("Evidència guardada a 'hacked.png'.")

            # SALIDA CRÍTICA: exit(1) hace que la pipeline de GitHub se ponga en ROJO
            print("Aturant pipeline per fallada de seguretat ...")
            os._exit(1)

except Exception as e:
    print(f"Error durant l'atac: {e}")
    os._exit(1)

finally:
    driver.quit()
