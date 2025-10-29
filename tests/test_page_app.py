import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import subprocess
import urllib.request


def wait_for_server(url, timeout=10):
    start = time.time()
    while time.time() - start < timeout:
        try:
            urllib.request.urlopen(url)
            return True
        except Exception:
            time.sleep(0.5)
    raise RuntimeError("❌ Flask сервер не запустился вовремя")

# @pytest.mark.skipif(os.getenv("CI") == "true", reason="⏭️ Selenium UI-тест пропущен на CI")
def test_form_submission():
    server = subprocess.Popen(
        ["python", "-m", "app.app"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=os.environ.copy()
    )
    print("📦 Полученные env:", os.getenv("SENDER_EMAIL"), os.getenv("SMTP_SERVER"))

    wait_for_server("http://127.0.0.1:5000/")
    # 1️⃣ Запускаем локальный сервер Flask перед тестом

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # ✅ Универсальный вариант: CI или локально
    chrome_path = os.getenv("CHROME_BIN")
    if chrome_path:
        options.binary_location = chrome_path

    driver = webdriver.Chrome(options=options)

    driver.get("http://127.0.0.1:5000/")

    # 2️⃣ Заполняем поля
    driver.find_element(By.NAME, "name").send_keys("Игорь")
    driver.find_element(By.NAME, "email").send_keys("test@example.com")
    driver.find_element(By.NAME, "message").send_keys("Это тестовое сообщение")

    # 3️⃣ Отправляем форму
    driver.find_element(By.TAG_NAME, "form").submit()
    time.sleep(20)# ждём загрузку страницы
    print("📄 Текущий URL:", driver.current_url)
    print("🧩 Заголовок страницы:", driver.title)
    screenshot_path = "screenshot.png"
    driver.save_screenshot(screenshot_path)
    print(f"📸 Скриншот сохранён: {screenshot_path}")

    # 4️⃣ Проверяем результат
    html = driver.page_source.lower()
    assert any(word in html for word in ["успешно", "успех"]), "❌ Форма не отправилась!"
    print("✅ Форма успешно отправлена!")

    print("✅ UI-тест успешно прошёл!")
    driver.quit()
    server.terminate()
    server.wait(timeout=3)
