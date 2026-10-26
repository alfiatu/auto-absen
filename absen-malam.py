import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def jalankan_absen_otomatis():
    options = Options()
    options.add_argument("--headless") # Wajib headless agar berjalan di cloud server tanpa layar
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    prefs = {
        "profile.default_content_setting_values.geolocation": 1
    }
    options.add_experimental_option("prefs", prefs)

    print("Menyiapkan browser...")
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    try:
        latitude_target = -7.953711600846924
        longitude_target = 112.60748217892687

        driver.execute_cdp_cmd("Emulation.setGeolocationOverride", {
            "latitude": latitude_target,
            "longitude": longitude_target,
            "accuracy": 100
        })

        print("Mengakses halaman login SIMA...")
        driver.get("https://sima.uin-malang.ac.id/login")

        print("Mengisi kredensial...")
        username_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "login-username"))
        )
        password_input = driver.find_element(By.ID, "login-password")

        # Mengambil data dari environment variables GitHub Secrets
        username_input.send_keys(os.environ.get("NIM_SIMA"))
        password_input.send_keys(os.environ.get("PASS_SIMA"))

        print("Mengklik tombol login...")
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit'] | //input[@type='submit'] | //button[contains(text(), 'Masuk') or contains(text(), 'Login')]"))
        )
        login_button.click()

        print("Menuju halaman absensi target...")
        target_url = "https://sima.uin-malang.ac.id/kemahadan/presensi/input/5?title=Presensi+Malam"
        
        time.sleep(3)
        driver.get(target_url)

        print("Memuat data presensi...")
        time.sleep(6)

        print("Mencari tombol Simpan Presensi...")
        tombol_simpan = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Simpan Presensi')]"))
        )
        
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", tombol_simpan)
        time.sleep(2)

        print("Mengeksekusi klik Simpan Presensi...")
        driver.execute_script("arguments[0].click();", tombol_simpan)

        print("Alhamdulillah, presensi berhasil disimpan secara otomatis di cloud!")
        time.sleep(5)

    except Exception as e:
        print(f"Terjadi kesalahan saat proses absen: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    jalankan_absen_otomatis()
