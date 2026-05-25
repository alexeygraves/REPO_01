import os
import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

BASE_URL = "http://localhost:8000/?balance=30000&reserved=20001"
CARD = "1111111111111111"


@pytest.fixture(scope="module")
def driver():
    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1280,800")

    chrome_bin = os.environ.get("CHROME_BIN")
    if chrome_bin:
        opts.binary_location = chrome_bin

    chromedriver = os.environ.get("SE_CHROMEDRIVER")
    service = Service(executable_path=chromedriver) if chromedriver else None
    d = webdriver.Chrome(service=service, options=opts)
    d.implicitly_wait(3)
    yield d
    d.quit()


def open_form(driver, url=BASE_URL):
    """Load F-Bank, click the Ruble card, enter a valid 16-digit card number."""
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, "//h1[text()='F-Bank']")))
    rub = wait.until(EC.element_to_be_clickable((By.XPATH, "//h2[text()='Рубли']")))
    rub.click()
    card_input = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@placeholder='0000 0000 0000 0000']")
    ))
    card_input.send_keys(CARD)
    return wait


# TC-001
def test_page_loads(driver):
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, "//h1[text()='F-Bank']")))
    assert "F-Bank" in driver.title


# TC-002
def test_transfer_form_opens(driver):
    wait = open_form(driver)
    wait.until(EC.presence_of_element_located(
        (By.XPATH, "//h2[text()='Перевод на карту']")
    ))


# TC-003: amount=1000, commission=100, total=1100, available=9999 — transfer allowed
def test_valid_transfer_button_shown(driver):
    wait = open_form(driver)
    btn = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//*[normalize-space(text())='Перевести']")
    ))
    assert btn.is_displayed()


# TC-004 / BUG-001: commission formula is wrong
# code: Math.floor(amount / 100) * 10
# spec: Math.floor(amount * 0.1) = Math.floor(amount / 10)
# for amount=150 the code shows 10 instead of 15
def test_commission_formula_correct(driver):
    wait = open_form(driver)
    amount_input = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@placeholder='1000']")
    ))
    # triple-click selects all text cross-platform, then type replaces it
    ActionChains(driver).click(amount_input).key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).send_keys("150").perform()
    time.sleep(0.3)
    commission_el = driver.find_element(By.ID, "comission")
    assert commission_el.text == "15", (
        f"BUG-001: wrong commission for amount 150: "
        f"expected 15, got '{commission_el.text}'"
    )


# TC-005 / BUG-002: boundary condition — strict > instead of >=
# balance=1100, reserved=0 -> available=1100
# amount=1000, commission=100 -> total=1100 = available
# spec: amount+commission <= available means transfer IS allowed
# code: o-s-h-O > 0 means 0 > 0 is false -> rejects the transfer
def test_boundary_transfer_allowed(driver):
    wait = open_form(driver, url="http://localhost:8000/?balance=1100&reserved=0")
    wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@placeholder='1000']")
    ))
    # default amount is 1000 which creates the exact boundary case
    time.sleep(0.3)
    buttons = driver.find_elements(By.XPATH, "//*[normalize-space(text())='Перевести']")
    assert len(buttons) > 0 and buttons[0].is_displayed(), (
        "BUG-002: transfer rejected when amount+commission exactly equals available balance"
    )
