import pytest
import csv
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.form_page import FormPage
from selenium.webdriver.common.by import By

def read_test_data(file_path):
    """Read CSV data with proper header normalization"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Test data file not found: {file_path}")
        
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = [name.strip() for name in reader.fieldnames]  # Normalize headers
        return [
            {k.strip(): v if v and v.strip() != '' else None for k, v in row.items()}
            for row in reader
        ]

test_data = read_test_data("test_data/form_data.csv")

@pytest.mark.parametrize("test_case", test_data)
class TestForm:
    def setup_method(self):
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(2)
        self.page = FormPage(self.driver)
        
    def teardown_method(self):
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()
            
    def test_element_sequence_until_success(self, test_case):
        """Test elements sequentially until successful submission"""
        self.page.load(test_case["url"])
        max_attempts = 5
        current_element_index = 0
        
        # Define the testing sequence
        elements_sequence = [
            ('country', test_case.get('country')),
            ('title', test_case.get('title')),
            ('first_name', test_case.get('first_name')),
            ('last_name', test_case.get('last_name')),
            ('dob', test_case.get('dob')),
            ('doj', test_case.get('doj')),
            ('email', test_case.get('email')),
            ('phone_code', test_case.get('phone_code')),
            ('phone_number', test_case.get('phone_number')),
            ('email_radio', 'email' if test_case.get('preferred_communication') == 'Email' else None),
            ('phone_radio', 'phone' if test_case.get('preferred_communication') == 'Phone' else None)
        ]
        
        while current_element_index < len(elements_sequence):
            element_name, value = elements_sequence[current_element_index]
            attempt = 0
            success = False
            
            while attempt < max_attempts and not success:
                try:
                    # Clear form before each attempt
                    self.page.clear_form()
                    
                    # Fill all elements up to current index
                    for i in range(current_element_index + 1):
                        name, val = elements_sequence[i]
                        self.page.fill_element(name, val)
                    
                    # Submit and check for success
                    self.page.submit_form()
                    success = self.page.is_success_displayed()
                    
                    if not success:
                        print(f"Attempt {attempt + 1} with {element_name} failed")
                        self.driver.save_screenshot(
                            f"screenshots/attempt_{current_element_index}_{element_name}_{attempt + 1}.png"
                        )
                    
                except Exception as e:
                    print(f"Error during attempt {attempt + 1} for {element_name}: {str(e)}")
                    self.driver.save_screenshot(
                        f"screenshots/error_{current_element_index}_{element_name}_{attempt + 1}.png"
                    )
                
                attempt += 1
            
            if success:
                print(f"Success achieved after filling up to {element_name}")
                break
            else:
                print(f"Moving to next element after failing with {element_name}")
                current_element_index += 1
        
        # Final attempt with all fields filled
        if not success:
            self.page.clear_form()
            for element_name, value in elements_sequence:
                self.page.fill_element(element_name, value)
            self.page.submit_form()
            success = self.page.is_success_displayed()
        
        assert success, "Failed to achieve successful submission after testing all elements"