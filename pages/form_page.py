from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
import time

class FormPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
        
        # Define all element locators
        self.locators = {
            'country': (By.XPATH, '//*[@id="root"]/div[2]/div/div/form/div[1]/select'),
            'title': (By.XPATH, '//*[@id="root"]/div[2]/div/div/form/div[2]/select'),
            'first_name': (By.XPATH, '//*[@id="root"]/div[2]/div/div/form/div[3]/div[1]/input'),
            'last_name': (By.XPATH, '//*[@id="root"]/div[2]/div/div/form/div[3]/div[2]/input'),
            'dob': (By.XPATH, '//*[@id="root"]/div[2]/div/div/form/div[4]/div[1]/div/input'),
            'doj': (By.XPATH, '//*[@id="root"]/div[2]/div/div/form/div[5]/input'),
            'email': (By.XPATH, '//*[@id="root"]/div[2]/div/div/form/div[6]/input'),
            'phone_code': (By.XPATH, '//*[@id="root"]/div[2]/div/div/form/div[7]/div/div[1]/select'),
            'phone_number': (By.XPATH, '//*[@id="root"]/div[2]/div/div/form/div[7]/div/div[2]/input'),
            'email_radio': (By.XPATH, '//*[@id="root"]/div[2]/div/div/form/div[8]/div/div[1]/input'),
            'phone_radio': (By.XPATH, '//*[@id="root"]/div[2]/div/div/form/div[8]/div/div[2]/input'),
            'submit': (By.XPATH, '//*[@id="root"]/div[2]/div/div/form/div[9]/button[2]'),
            'clear': (By.XPATH, '//*[@id="root"]/div[2]/div/div/form/div[9]/button[1]'),
            'success_message': (By.XPATH, '//*[@id="root"]/div[2]/div/div/div/div[2]/div')
        }

    def load(self, url):
        """Load the page and maximize window"""
        self.driver.get(url)
        self.driver.maximize_window()
        self.wait.until(EC.presence_of_element_located(self.locators['country']))
        
    def _scroll_and_wait(self, element):
        """Scroll to element and wait for it to be clickable"""
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", element)
        time.sleep(0.3)
        return self.wait.until(EC.element_to_be_clickable(element))
        
    def _safe_click(self, element):
        """Robust click handling with multiple strategies"""
        try:
            element.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", element)
            
    def fill_element(self, element_name, value):
        """Fill a form element based on its type"""
        locator = self.locators[element_name]
        element = self._scroll_and_wait(self.wait.until(EC.presence_of_element_located(locator)))
        
        if 'select' in locator[1]:  # Handle dropdowns
            if value:
                Select(element).select_by_visible_text(str(value))
            else:
                Select(element).select_by_index(1)  # Default to first option
        elif 'input' in locator[1] and 'radio' not in element_name:  # Handle text inputs
            element.clear()
            if value:
                element.send_keys(str(value))
        elif 'radio' in element_name:  # Handle radio buttons
            if value and str(value).strip().lower() in ['email', 'phone']:
                self._safe_click(element)
                
    def submit_form(self):
        """Click submit button"""
        self._safe_click(self._scroll_and_wait(self.wait.until(
            EC.presence_of_element_located(self.locators['submit'])
        )))
        
    def clear_form(self):
        """Click clear button to reset all fields"""
        self._safe_click(self._scroll_and_wait(self.wait.until(
            EC.presence_of_element_located(self.locators['clear'])
        )))
        
    def is_success_displayed(self, timeout=5):
        """Check if success message is visible"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.locators['success_message'])
            ).is_displayed()
        except TimeoutException:
            return False