import pytest
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
from datetime import datetime

# === Setup directories ===
log_file = "logs/test_log.log"
os.makedirs("logs", exist_ok=True)
os.makedirs("screenshots", exist_ok=True)

# === Configure logging ===
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

@pytest.fixture
def setup(request):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()  # ✅ Requirement #1
    logging.info("Browser started.")
    yield driver

    # === Take screenshot on failure ===
    if request.node.rep_call.failed:
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot_name = f"screenshots/failure_{request.node.name}_{timestamp}.png"
            driver.save_screenshot(screenshot_name)
            logging.error(f"Test failed: {request.node.name}")
            logging.error(f"Screenshot saved to: {screenshot_name}")
        except Exception as e:
            logging.error(f"Error taking screenshot: {e}")

    #driver.quit()
    #logging.info("Browser closed.")

# Hook for capturing test result
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
