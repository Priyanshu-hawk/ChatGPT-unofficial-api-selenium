from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

# logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
#                   level=logging.INFO)  # For logging to console, Debugging purposes.

class HelperFn:
    def __init__(self, driver):
        self.driver = driver
    
    def wait_for_element(self, xpath, timeout=22):
        try:
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
            logging.info("# Element '%s' is present." % xpath)
        except TimeoutException:
            logging.error("# Element '%s' is not present." % xpath)
    
    def is_element_present(self, xpath):
        try:
            self.driver.find_element(By.XPATH, xpath)
            logging.info("# Element '%s' is present." % xpath)
        except NoSuchElementException:
            logging.error("# Element '%s' is not present." % xpath)
            return False
        return True

    def wait_for_element_visible(self, xpath, timeout=22):
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))
            logging.info("# Element '%s' is visible." % xpath)
        except TimeoutException:
            logging.error("# Element '%s' is not visible." % xpath)
    
    def is_element_visible(self, xpath):
        try:
            logging.info("# Element '%s' is visible." % xpath)
            return self.driver.find_element(By.XPATH, xpath).is_displayed()
        except NoSuchElementException:
            logging.error("# Element '%s' is not visible." % xpath)
            return False
    
    def find_element(self, xpath):
        try:
            element = self.driver.find_element(By.XPATH, xpath)
            logging.info("# Element '%s' is found." % xpath)
        except NoSuchElementException:
            logging.error("# Element '%s' is not found." % xpath)
            return False
        return element

    def find_elements(self, xpath):
        try:
            elements = self.driver.find_elements(By.XPATH, xpath)
            logging.info("# Element '%s' is found." % xpath)
        except NoSuchElementException:
            logging.error("# Element '%s' is not found." % xpath)
            return False
        return elements