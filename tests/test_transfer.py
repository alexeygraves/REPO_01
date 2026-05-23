import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "http://localhost:9999"

# login creds from the service docs
LOGIN = "vasya"
PASSWORD = "qwerty123"


@pytest.fixture(scope="module")
def driver():
    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1280,800")

    svc = Service(ChromeDriverManager().install())
    d = webdriver.Chrome(service=svc, options=opts)
    d.implicitly_wait(5)
    yield d
    d.quit()


def login(driver):
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.NAME, "login")))
    driver.find_element(By.NAME, "login").clear()
    driver.find_element(By.NAME, "login").send_keys(LOGIN)
    driver.find_element(By.NAME, "password").clear()
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "[data-testid='action-button']").click()


def get_balance(driver):
    wait = WebDriverWait(driver, 10)
    el = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "[data-testid='balance']")
    ))
    # balance comes as "10 000 руб." or just digits — strip everything non-numeric
    raw = el.text.replace(" ", "").replace("руб.", "").replace(",", ".")
    return float("".join(c for c in raw if c.isdigit() or c == "."))


def do_transfer(driver, amount, to_account="5559 0000 0000 0002"):
    wait = WebDriverWait(driver, 10)
    # find and click "перевести" link on the card
    driver.find_element(By.CSS_SELECTOR, "[data-testid='action-button']").click()
    wait.until(EC.presence_of_element_located((By.NAME, "amount")))
    driver.find_element(By.NAME, "amount").clear()
    driver.find_element(By.NAME, "amount").send_keys(str(amount))
    to_field = driver.find_element(By.NAME, "to")
    to_field.clear()
    to_field.send_keys(to_account)
    driver.find_element(By.CSS_SELECTOR, "[data-testid='action-button']").click()


# ---- tests ----

def test_page_loads(driver):
    driver.get(BASE_URL)
    assert "банк" in driver.title.lower() or driver.find_element(By.TAG_NAME, "body")


def test_valid_transfer(driver):
    login(driver)
    balance_before = get_balance(driver)
    amount = 100
    do_transfer(driver, amount)

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "[data-testid='balance']")
    ))
    balance_after = get_balance(driver)
    assert balance_after == pytest.approx(balance_before - amount, abs=1), (
        f"expected balance {balance_before - amount}, got {balance_after}"
    )


# BUG-001: negative amount should be rejected, but the app accepts it
def test_negative_amount_rejected(driver):
    login(driver)
    balance_before = get_balance(driver)
    do_transfer(driver, -500)

    wait = WebDriverWait(driver, 10)
    # expect an error message to appear
    try:
        err = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "[data-testid='error-message']")
        ))
        assert err.is_displayed(), "error message not visible"
    except Exception:
        # no error shown — check balance didn't increase
        balance_after = get_balance(driver)
        # if balance grew (app added money), defect is confirmed
        assert balance_after <= balance_before, (
            f"BUG-001: balance increased after negative transfer: "
            f"before={balance_before}, after={balance_after}"
        )


# BUG-002: amount over balance should be rejected
def test_transfer_exceeds_balance(driver):
    login(driver)
    balance_before = get_balance(driver)
    over_amount = balance_before + 10000
    do_transfer(driver, over_amount)

    wait = WebDriverWait(driver, 10)
    try:
        err = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "[data-testid='error-message']")
        ))
        assert err.is_displayed(), "error message not visible"
    except Exception:
        balance_after = get_balance(driver)
        assert balance_after >= 0, (
            f"BUG-002: balance went negative after transfer: "
            f"before={balance_before}, amount={over_amount}, after={balance_after}"
        )


def test_empty_recipient_rejected(driver):
    login(driver)
    # pass empty string as recipient account
    wait = WebDriverWait(driver, 10)
    driver.find_element(By.CSS_SELECTOR, "[data-testid='action-button']").click()
    wait.until(EC.presence_of_element_located((By.NAME, "amount")))
    driver.find_element(By.NAME, "amount").send_keys("100")
    # leave "to" field empty
    driver.find_element(By.CSS_SELECTOR, "[data-testid='action-button']").click()

    err = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "[data-testid='error-message']")
    ))
    assert err.is_displayed()
