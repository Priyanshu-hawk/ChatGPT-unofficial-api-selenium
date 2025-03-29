import os
import time
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
import helper_fn
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p'
)

class ChromeDriverManager:
    def __init__(self):
        self.driver = None
        self.max_retries = 3
        self.retry_delay = 5
        self.setup_chrome_options()

    def setup_chrome_options(self):
        """Set up Chrome options for optimal stability."""
        self.options = uc.ChromeOptions()
        
        # Create user data directory if it doesn't exist
        user_data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'chrome_user_data')
        os.makedirs(user_data_dir, exist_ok=True)
        
        # Add user data directory argument
        self.options.add_argument(f'--user-data-dir={user_data_dir}')
        
        # Existing options
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--disable-software-rasterizer')
        self.options.add_argument('--disable-extensions')
        self.options.add_argument('--disable-notifications')
        self.options.add_argument('--disable-popup-blocking')
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--start-maximized')
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_argument('--disable-logging')
        self.options.add_argument('--log-level=3')
        self.options.add_argument('--silent')
        self.options.add_argument('--disable-automation')
        self.options.add_argument('--disable-infobars')
        self.options.add_argument('--disable-blink-features')
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_argument('--disable-web-security')
        self.options.add_argument('--allow-running-insecure-content')

    def initialize_driver(self):
        """Initialize Chrome driver with retries."""
        for attempt in range(self.max_retries):
            try:
                if self.driver:
                    try:
                        self.driver.quit()
                    except:
                        pass
                
                self.driver = uc.Chrome(options=self.options)
                self.driver.set_page_load_timeout(30)
                helper_fn.set_driver(self.driver)  # Set the driver in helper_fn
                logging.info("Chrome driver initialized successfully")
                return True
            except Exception as e:
                logging.error(f"Attempt {attempt + 1} failed to initialize Chrome driver: {str(e)}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                else:
                    logging.error("Failed to initialize Chrome driver after all retries")
                    raise

    def ensure_driver_alive(self):
        """Check if driver is alive and reconnect if necessary."""
        try:
            # Try to get window handles to check if driver is responsive
            self.driver.window_handles
            return True
        except:
            logging.warning("Chrome driver appears to be dead, attempting to reconnect...")
            return self.initialize_driver()

    def quit(self):
        """Safely quit the Chrome driver."""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None

# Initialize the global ChromeDriverManager
driver_manager = ChromeDriverManager()
driver = None

def initialize_chrome():
    """Initialize Chrome and navigate to ChatGPT."""
    global driver
    try:
        if driver_manager.initialize_driver():
            driver = driver_manager.driver
            driver.get("https://chat.openai.com/")
            logging.info("Successfully navigated to ChatGPT")
            return True
        return False
    except Exception as e:
        logging.error(f"Failed to initialize Chrome: {str(e)}")
        return False

def ensure_chrome_alive():
    """Ensure Chrome is alive and reconnect if necessary."""
    global driver
    if driver_manager.ensure_driver_alive():
        driver = driver_manager.driver
        return True
    return False

def is_response_complete():
    """Check if the response is complete using multiple methods."""
    try:
        # Method 1: Check for the presence of typing indicators
        typing_indicators = driver.find_elements(By.XPATH, "//div[contains(@class, 'result-streaming')]")
        if not typing_indicators:
            logging.info("No typing indicators found")
            return True
            
        # Method 2: Check if the response text has stopped changing
        response_container_xpath = "//div[contains(@class, 'markdown prose w-full break-words')]"
        current_response = driver.find_elements(By.XPATH, response_container_xpath)[-1].text
        time.sleep(2)  # Brief wait
        new_response = driver.find_elements(By.XPATH, response_container_xpath)[-1].text
        if current_response == new_response and current_response != "":
            logging.info("Response text has stabilized")
            return True
        
        logging.info("Response still in progress...")
        return False
        
    except Exception as e:
        logging.warning(f"Error checking response completion: {str(e)}")
        return False

def make_gpt_request_and_copy(text):
    """
    Function to interact with ChatGPT web interface and copy formatted response
    Args:
        text: Query text to send to ChatGPT
    Returns:
        str: Formatted response text from clipboard
    """
    global driver

    try:
        if not ensure_chrome_alive():
            raise Exception("Failed to ensure Chrome is alive")

        logging.info("Starting GPT request process...")
        # Initial pause to ensure page is loaded
        time.sleep(1.5)
        
        try:
            # 1. Check for "Stay logged out" button first
            logging.info("Step 1a: Checking for 'Stay logged out' button...")
            try:
                stay_logged_out_xpath = "//a[contains(text(), 'Stay logged out')]"
                if helper_fn.is_element_present(stay_logged_out_xpath, timeout=1):
                    logging.info("'Stay logged out' button found, clicking it...")
                    helper_fn.click_element(stay_logged_out_xpath)
                    time.sleep(1)
                    logging.info("Clicked 'Stay logged out'")
            except Exception as logout_error:
                logging.warning(f"Stay logged out check encountered an error: {str(logout_error)}")
            
            # 1b. Text input logic
            logging.info("Step 1b: Finding text input area...")
            text_area_xpath = "//*[@id='prompt-textarea']"
            if helper_fn.send_keys(text_area_xpath, text):
                logging.info("Text input successful")
            else:
                raise Exception("Failed to input text")

        except Exception as e:
            logging.error(f"Error in Step 1 (Text Input): {str(e)}")
            raise
        
        try:
            # 2. Find and click send button
            logging.info("Step 2: Finding and clicking send button...")
            send_btn_xpath = "//*[@data-testid='send-button']"
            if helper_fn.click_element(send_btn_xpath):
                logging.info("Send button clicked")
            else:
                raise Exception("Failed to click send button")

        except Exception as e:
            logging.error(f"Error in Step 2 (Send Button): {str(e)}")
            raise
        
        try:
            # 3. Wait for response container
            logging.info("Step 3: Waiting for response container...")
            try:
                canvas_button_xpath = "//button[contains(., 'Answer in chat instead')]"
                if helper_fn.is_element_present(canvas_button_xpath, timeout=5):
                    logging.info("Canvas mode detected, switching to chat mode...")
                    helper_fn.click_element(canvas_button_xpath)
                    time.sleep(2)
                    logging.info("Switched to chat mode")
                else:
                    logging.info("Already in chat mode")
            except Exception as canvas_error:
                logging.warning(f"Canvas check encountered an error: {str(canvas_error)}")

            # 4. Wait for response to appear and complete
            logging.info("Step 4: Waiting for response...")
            try:
                # First, wait for response container to appear
                response_container_xpath = "//div[contains(@class, 'markdown prose w-full break-words')]"
                if helper_fn.wait_for_element(response_container_xpath, timeout=30):
                    logging.info("Initial response detected")

                    # Wait for response completion with timeout
                    start_time = time.time()
                    timeout = 180  # 3 minutes timeout
                    last_length = 0
                    stable_count = 0
                    
                    while time.time() - start_time < timeout:
                        if not ensure_chrome_alive():
                            raise Exception("Chrome driver died during response wait")
                            
                        try:
                            # Get current response
                            responses = helper_fn.find_elements(response_container_xpath)
                            if responses:
                                current_text = responses[-1].text
                                current_length = len(current_text)
                                
                                logging.debug(f"Current response length: {current_length}, Last length: {last_length}")
                                
                                # If text length hasn't changed and response seems complete
                                if current_length > 0 and current_length == last_length:
                                    if is_response_complete():
                                        stable_count += 1
                                        logging.info(f"Response stable for {stable_count} checks")
                                        if stable_count >= 3:  # Require 3 consecutive stable checks
                                            time.sleep(2)  # Final verification wait
                                            if current_length == len(responses[-1].text):
                                                logging.info("Response completion confirmed")
                                                break
                                    else:
                                        stable_count = 0  # Reset stable count if response is not complete
                                else:
                                    stable_count = 0  # Reset stable count if length changed
                                
                                last_length = current_length
                            
                        except Exception as e:
                            logging.warning(f"Error while checking response: {str(e)}")
                            stable_count = 0  # Reset stable count on error
                            
                        time.sleep(2)  # Increased wait time to reduce CPU usage
                    
                    if time.time() - start_time >= timeout:
                        logging.warning("Response timeout reached")
                        raise TimeoutException("Response generation timed out")
                        
                else:
                    raise Exception("Response container not found")
                    
            except TimeoutException as te:
                logging.error(f"Timeout while waiting for response: {str(te)}")
                raise
            except Exception as e:
                logging.error(f"Error in Step 4 (Response Detection): {str(e)}")
                raise

            # Short wait for UI to stabilize
            time.sleep(2)

        except Exception as e:
            logging.error(f"Error in Step 3 (Response Container): {str(e)}")
            raise

        # 5. Get response text directly
        logging.info("Step 5: Getting response text...")
        try:
            response_elements = helper_fn.find_elements(response_container_xpath)
            if response_elements:
                last_response = response_elements[-1]
                # Use JavaScript to get formatted text
                formatted_text = driver.execute_script("""
                    var element = arguments[0];
                    var text = '';
                    var lastWasNewline = false;
                    var lastWasSpace = false;
                    
                    function extractText(node) {
                        if (node.nodeType === Node.TEXT_NODE) {
                            var content = node.textContent.trim();
                            if (content) {
                                if (lastWasNewline) {
                                    text += '\\n';
                                }
                                text += content;
                                lastWasNewline = false;
                                lastWasSpace = false;
                            }
                        } else if (node.nodeName === 'PRE') {
                            // Handle code blocks
                            if (lastWasNewline) {
                                text += '\\n';
                            }
                            text += '```\\n' + node.textContent + '\\n```\\n';
                            lastWasNewline = true;
                            lastWasSpace = false;
                        } else if (node.nodeName === 'CODE') {
                            // Handle inline code
                            text += '`' + node.textContent + '`';
                            lastWasNewline = false;
                            lastWasSpace = false;
                        } else if (node.nodeName === 'STRONG' || node.nodeName === 'B') {
                            // Handle bold text
                            if (!lastWasSpace) {
                                text += ' ';
                            }
                            text += '**' + node.textContent + '**';
                            lastWasNewline = false;
                            lastWasSpace = true;
                        } else if (node.nodeName === 'EM' || node.nodeName === 'I') {
                            // Handle italic text
                            if (!lastWasSpace) {
                                text += ' ';
                            }
                            text += '*' + node.textContent + '*';
                            lastWasNewline = false;
                            lastWasSpace = true;
                        } else if (node.nodeName === 'BLOCKQUOTE') {
                            // Handle blockquotes
                            if (lastWasNewline) {
                                text += '\\n';
                            }
                            text += '> ' + node.textContent.trim().replace(/\\n/g, '\\n> ') + '\\n';
                            lastWasNewline = true;
                            lastWasSpace = false;
                        } else if (node.nodeName === 'HR') {
                            // Handle horizontal rules
                            if (lastWasNewline) {
                                text += '\\n';
                            }
                            text += '\\n---\\n\\n';
                            lastWasNewline = true;
                            lastWasSpace = false;
                        } else if (node.nodeName === 'UL' || node.nodeName === 'OL') {
                            // Handle lists
                            if (lastWasNewline) {
                                text += '\\n';
                            }
                            var items = node.getElementsByTagName('li');
                            for (var i = 0; i < items.length; i++) {
                                text += (node.nodeName === 'OL' ? (i + 1) + '. ' : '- ') + items[i].textContent.trim() + '\\n';
                            }
                            lastWasNewline = true;
                            lastWasSpace = false;
                        } else if (node.nodeName === 'P') {
                            // Handle paragraphs
                            if (lastWasNewline) {
                                text += '\\n';
                            }
                            for (var child of node.childNodes) {
                                extractText(child);
                            }
                            text += '\\n';
                            lastWasNewline = true;
                            lastWasSpace = false;
                        } else if (node.nodeName === 'BR') {
                            // Handle line breaks
                            text += '\\n';
                            lastWasNewline = true;
                            lastWasSpace = false;
                        } else {
                            // Process child nodes
                            for (var child of node.childNodes) {
                                extractText(child);
                            }
                        }
                    }
                    
                    extractText(element);
                    
                    // Clean up excessive newlines
                    text = text.replace(/\\n{3,}/g, '\\n\\n');
                    
                    // Ensure proper spacing around horizontal rules
                    text = text.replace(/\\n---\\n/g, '\\n\\n---\\n\\n');
                    
                    // Clean up any double spaces
                    text = text.replace(/  +/g, ' ');
                    
                    return text.trim();
                """, last_response)
                logging.info("Successfully extracted response text")
                return formatted_text
            else:
                raise Exception("No response elements found")
        except Exception as e:
            logging.error(f"Error extracting response text: {str(e)}")
            raise

    except Exception as e:
        logging.error(f"Process failed: {str(e)}")
        if not ensure_chrome_alive():
            logging.error("Chrome driver died during process")
        return f"Error occurred: {str(e)}"

def cleanup():
    """Clean up resources."""
    driver_manager.quit()

if __name__ == "__main__":
    initialize_chrome()
    try:
        response = make_gpt_request_and_copy("Hello, how are you?")
        print(response)
    finally:
        cleanup()
