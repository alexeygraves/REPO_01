import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

os.makedirs("screenshots", exist_ok=True)

opts = Options()
opts.add_argument("--headless")
opts.add_argument("--no-sandbox")
opts.add_argument("--disable-dev-shm-usage")
opts.add_argument("--window-size=1280,800")
driver = webdriver.Chrome(options=opts)
driver.implicitly_wait(3)

try:
    # BUG-001: wrong commission for amount 150 (shows 10 instead of 15)
    driver.get("http://localhost:8000/?balance=30000&reserved=0")
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, "//h1[text()='F-Bank']")))
    rub = wait.until(EC.element_to_be_clickable((By.XPATH, "//h2[text()='Рубли']")))
    rub.click()
    card_input = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@placeholder='0000 0000 0000 0000']")
    ))
    card_input.send_keys("1111111111111111")
    amount_input = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@placeholder='1000']")
    ))
    ActionChains(driver).click(amount_input).key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).send_keys("150").perform()
    time.sleep(0.5)
    driver.save_screenshot("screenshots/bug-001.png")
    print("bug-001.png saved")

    # BUG-002: boundary condition — amount+commission == balance, transfer blocked
    driver.get("http://localhost:8000/?balance=1100&reserved=0")
    wait.until(EC.presence_of_element_located((By.XPATH, "//h1[text()='F-Bank']")))
    rub = wait.until(EC.element_to_be_clickable((By.XPATH, "//h2[text()='Рубли']")))
    rub.click()
    card_input = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@placeholder='0000 0000 0000 0000']")
    ))
    card_input.send_keys("1111111111111111")
    time.sleep(0.5)
    driver.save_screenshot("screenshots/bug-002.png")
    print("bug-002.png saved")

finally:
    driver.quit()
