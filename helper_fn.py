from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging
import pyperclip
from selenium.webdriver.common.keys import Keys

# Global variables
driver = None
DEFAULT_TIMEOUT = 10

def set_driver(webdriver):
    """Set the global driver instance."""
    global driver
    driver = webdriver

def wait_for_element(xpath, timeout=DEFAULT_TIMEOUT):
    """Wait for an element to be present and visible."""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return element
    except TimeoutException:
        logging.warning(f"Timeout waiting for element: {xpath}")
        return None
    except Exception as e:
        logging.error(f"Error waiting for element {xpath}: {str(e)}")
        return None

def is_element_present(xpath, timeout=DEFAULT_TIMEOUT):
    """Check if an element is present on the page."""
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return True
    except (TimeoutException, NoSuchElementException):
        return False
    except Exception as e:
        logging.error(f"Error checking element presence {xpath}: {str(e)}")
        return False

def find_element(xpath, timeout=DEFAULT_TIMEOUT):
    """Find an element by xpath with wait."""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return element
    except TimeoutException:
        logging.warning(f"Element not found: {xpath}")
        return None
    except Exception as e:
        logging.error(f"Error finding element {xpath}: {str(e)}")
        return None

def find_elements(xpath, timeout=DEFAULT_TIMEOUT):
    """Find all elements matching xpath with wait."""
    try:
        elements = WebDriverWait(driver, timeout).until(
            EC.presence_of_all_elements_located((By.XPATH, xpath))
        )
        return elements
    except TimeoutException:
        logging.warning(f"No elements found: {xpath}")
        return []
    except Exception as e:
        logging.error(f"Error finding elements {xpath}: {str(e)}")
        return []

def click_element(xpath, timeout=DEFAULT_TIMEOUT):
    """Click an element with wait and retry."""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        element.click()
        return True
    except Exception as e:
        logging.error(f"Error clicking element {xpath}: {str(e)}")
        try:
            # Fallback to JavaScript click
            element = find_element(xpath)
            if element:
                driver.execute_script("arguments[0].click();", element)
                return True
        except Exception as js_error:
            logging.error(f"JavaScript click failed for {xpath}: {str(js_error)}")
        return False

def send_keys(xpath, text, timeout=DEFAULT_TIMEOUT):
    """Send keys to an element with wait using clipboard to handle non-BMP characters."""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        element.clear()
        
        # Store current clipboard content
        original_clipboard = pyperclip.paste()
        
        # Copy text to clipboard
        pyperclip.copy(text)
        
        # Use Ctrl+V to paste
        element.send_keys(Keys.CONTROL + 'v')
        
        # Restore original clipboard content
        pyperclip.copy(original_clipboard)
        
        return True
    except Exception as e:
        logging.error(f"Error sending keys to element {xpath}: {str(e)}")
        return False

def wait_for_text_present(xpath, text, timeout=DEFAULT_TIMEOUT):
    """Wait for text to be present in element."""
    try:
        return WebDriverWait(driver, timeout).until(
            EC.text_to_be_present_in_element((By.XPATH, xpath), text)
        )
    except TimeoutException:
        logging.warning(f"Text '{text}' not found in element: {xpath}")
        return False
    except Exception as e:
        logging.error(f"Error waiting for text in element {xpath}: {str(e)}")
        return False

def wait_for_element_invisible(xpath, timeout=DEFAULT_TIMEOUT):
    """Wait for an element to become invisible."""
    try:
        return WebDriverWait(driver, timeout).until(
            EC.invisibility_of_element_located((By.XPATH, xpath))
        )
    except TimeoutException:
        logging.warning(f"Element still visible: {xpath}")
        return False
    except Exception as e:
        logging.error(f"Error waiting for element invisibility {xpath}: {str(e)}")
        return False

def get_element_text(xpath, timeout=DEFAULT_TIMEOUT):
    """Get text from an element with wait."""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return element.text
    except Exception as e:
        logging.error(f"Error getting text from element {xpath}: {str(e)}")
        return None

def is_element_enabled(xpath, timeout=DEFAULT_TIMEOUT):
    """Check if an element is enabled."""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return element.is_enabled()
    except Exception as e:
        logging.error(f"Error checking if element is enabled {xpath}: {str(e)}")
        return False

def scroll_into_view(xpath, timeout=DEFAULT_TIMEOUT):
    """Scroll element into view."""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        return True
    except Exception as e:
        logging.error(f"Error scrolling element into view {xpath}: {str(e)}")
        return False 