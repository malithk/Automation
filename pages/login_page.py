from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)  # ⏳ Wait time increased to 20 seconds
        self.username_input = (By.XPATH, '//*[@id="formBasicEmail"]')
        self.password_input = (By.XPATH, '//*[@id="formBasicPassword"]')
        self.login_button = (By.XPATH, '//*[@id="root"]/div[3]/div[1]/div/div/div/form/button')
        self.message_box = (By.XPATH, '//*[@id="root"]/div[3]/div[1]/div/div/div/div[3]')

    def load(self):
        self.driver.get("https://testerbud.com/practice-login-form")
        self.driver.maximize_window()  # ✅ Maximize window immediately after page opens
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # ⬇️ Scroll to bottom

    def login(self, username, password):
        # Wait for and fill username
        username_field = self.wait.until(EC.presence_of_element_located(self.username_input))
        username_field.clear()
        username_field.send_keys(username)

        # Wait for and fill password
        password_field = self.wait.until(EC.presence_of_element_located(self.password_input))
        password_field.clear()
        password_field.send_keys(password)

        # Wait for login button and scroll to it
        login_btn = self.wait.until(EC.element_to_be_clickable(self.login_button))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", login_btn)

        try:
            # First try regular Selenium click
            login_btn.click()
        except Exception as e:
            # Fallback to JS click if standard click fails
            print(f"[WARN] Standard click failed: {e} — trying JS click.")
            self.driver.execute_script("arguments[0].click();", login_btn)

    def get_message(self):
        try:
            # Wait for the message to appear
            message_element = self.wait.until(EC.presence_of_element_located(self.message_box))
            return message_element.text.strip()
        except Exception as e:
            print(f"[WARN] Could not retrieve message element: {e}")
            return ""
