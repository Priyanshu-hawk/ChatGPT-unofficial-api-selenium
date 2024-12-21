from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium.common.exceptions import TimeoutException

import time

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc

import os

import chrome_handler
import helper_funcs
import sys

# current file path
current_file_path = os.path.dirname(os.path.realpath(__file__))
user_data_folder = current_file_path + "/chromedata"
chrome_profile = "Default"

def load_chrome():
    options = Options()
    options.add_argument(f"--user-data-dir={user_data_folder}")
    options.add_argument(f'--profile-directory={chrome_profile}')

    global helper_fn, driver

    driver = uc.Chrome(options=options)
    helper_fn = helper_funcs.HelperFn(driver)


def start_chat_gpt():
    load_chrome()
    driver.maximize_window()
    driver.get("https://chatgpt.com/")
    time.sleep(3)

'''
This function only returns raw text, with no formatting... For formatted markdown text, I've made make_gpt_request_and_copy() 
'''
def make_gpt_request(text):
    time.sleep(1)
    text_area_xpath = "//*[@id='prompt-textarea']"
    helper_fn.wait_for_element(text_area_xpath)
    if helper_fn.is_element_present(text_area_xpath):
        text_area = helper_fn.find_element(text_area_xpath)
        text_area.send_keys(text)

        # send button
        send_btn_xpath = "//*[@data-testid='send-button']"
        
        # Wait until the button with data-testid="send-button" is present
        WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.XPATH, send_btn_xpath))
        )
        
        send_btn = helper_fn.find_element(send_btn_xpath)
        time.sleep(1)
        send_btn.click()

    helper_fn.wait_for_x_seconds(5)
    # waiting for response
    response_xpath_light = "//*[@class='markdown prose w-full break-words dark:prose-invert light']" # for light mode
    response_xpath_dark = "//*[@class='markdown prose w-full break-words dark:prose-invert dark']" # for dark mode
    regenrate_xpath = '//*[@id="__next"]/div[1]/div[2]/main/div[1]/div[2]/div[1]/div/form/div/div[2]/div/div/button'
    
    # Change this line to wait for send button instead of regenrate button
    WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.XPATH, send_btn_xpath))
    )

    response_xpath = response_xpath_dark if helper_fn.is_element_present(response_xpath_dark) else response_xpath_light # check for dark mode or light mode
    if helper_fn.is_element_present(response_xpath):
        helper_fn.wait_for_x_seconds(1)
        response = helper_fn.find_elements(response_xpath)[-1]
        return response.text # will return all the textual information under that particular xpath

def make_gpt_request_and_copy(text):
    """
    Function to interact with ChatGPT web interface and copy formatted response
    Args:
        text: Query text to send to ChatGPT
    Returns:
        str: Formatted response text from clipboard
    """

    try:
        print("Starting GPT request process...")
        # Initial pause to ensure page is loaded
        time.sleep(1.5)
        
        try:
            # 1. Check for "Stay logged out" button first
            print("Step 1a: Checking for 'Stay logged out' button...")
            try:
                stay_logged_out_xpath = "//a[contains(text(), 'Stay logged out')]"
                stay_logged_out = WebDriverWait(driver, 1).until(
                    EC.presence_of_element_located((By.XPATH, stay_logged_out_xpath))
                )
                print("🔒 'Stay logged out' button found, clicking it...")
                stay_logged_out.click()
                time.sleep(1)
                print("✓ Clicked 'Stay logged out'")
            except TimeoutException:
                print("💡 No 'Stay logged out' button found, continuing...")
            except Exception as logout_error:
                print(f"⚠️ Stay logged out check encountered an error: {str(logout_error)}")
            
            # 1b. Original text input logic
            print("Step 1b: Finding text input area...")
            text_area_xpath = "//*[@id='prompt-textarea']"
            helper_fn.wait_for_element(text_area_xpath)
            if helper_fn.is_element_present(text_area_xpath):
                text_area = helper_fn.find_element(text_area_xpath)
                text_area.send_keys(text)
                print("✓ Text input successful")
            else:
                raise Exception("Text area not found")
        except Exception as e:
            print(f"❌ Error in Step 1 (Text Input): {str(e)}")
            raise
        
        try:
            # 2. Find and click send button
            print("Step 2: Finding and clicking send button...")
            send_btn_xpath = "//*[@data-testid='send-button']"
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, send_btn_xpath))
            )
            send_btn = helper_fn.find_element(send_btn_xpath)
            time.sleep(1)
            send_btn.click()
            print("✓ Send button clicked")
        except Exception as e:
            print(f"❌ Error in Step 2 (Send Button): {str(e)}")
            raise
        
        try:
            # 3. Wait for response container
            print("Step 3: Waiting for response container...")
            """
            There is a new mode, in ChatGPT --> Canvas, it is answered in canvas (detected by the text ),
            then change it to chat mode here.
            """
            try:
                canvas_button = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Answer in chat instead')]"))
                )
                print("📝 Canvas mode detected, switching to chat mode...")
                canvas_button.click()
                # Wait for transition
                time.sleep(2)
                print("✓ Switched to chat mode")
            except TimeoutException:
                print("💬 Already in chat mode")
            except Exception as canvas_error:
                print(f"⚠️ Canvas check encountered an error: {str(canvas_error)}")
                # Continue anyway as this might be a false negative
            
            # Short wait for UI to stabilize
            time.sleep(2)

            response_container_xpath = "//div[contains(@class, 'markdown prose w-full break-words')]"
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, response_container_xpath))
            )
            print("✓ Response container found")
        except Exception as e:
            print(f"❌ Error in Step 3 (Response Container): {str(e)}")
            raise

        # 4. Wait for response to appear and complete
        print("Step 4: Waiting for response...")
        try:
            # First, wait for response container to appear
            response_container_xpath = "//div[contains(@class, 'markdown prose w-full break-words')]"
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, response_container_xpath))
            )
            print("✓ Initial response detected")

            try:
                # Then wait for the typing indicator to disappear
                typing_indicator_xpath = "//div[contains(@class, 'result-streaming')]"
                WebDriverWait(driver, 180).until_not(
                    EC.presence_of_element_located((By.XPATH, typing_indicator_xpath))
                )
                print("✓ Response completion confirmed")
            except TimeoutException:
                print("⚠️ Response timeout - ChatGPT may have entered power saving mode")
                print("ℹ️ Please check your browser tab - ChatGPT requires tab focus to continue processing")
                raise Exception("ChatGPT entered power saving mode - Please ensure the browser tab is active")
                    

            
            # Short wait for UI to stabilize
            time.sleep(2)

        except Exception as e:
            print(f"❌ Error in Step 4 (Response Detection): {str(e)}")
            raise

        # 5. Find and handle copy button
        print("Step 5: Locating copy button...")
        try:
            copy_button_xpath = "//*[@data-testid='copy-turn-action-button']"
            
            # Wait for copy buttons with multiple conditions
            WebDriverWait(driver, 1000).until(
                EC.presence_of_all_elements_located((By.XPATH, copy_button_xpath))
            )
            
            # Get all copy buttons
            copy_buttons = driver.find_elements(By.XPATH, copy_button_xpath)
            
            if not copy_buttons:
                raise Exception("No copy buttons found after waiting")
                
            # Get the last copy button
            last_copy_button = copy_buttons[-1]
            
            # Scroll to button and ensure it's in view
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", last_copy_button)
            time.sleep(1)
            
            # Try multiple click methods
            try:
                # Try regular click first
                last_copy_button.click()
            except:
                try:
                    # Try JavaScript click if regular click fails
                    driver.execute_script("arguments[0].click();", last_copy_button)
                except Exception as js_error:
                    print(f"❌ Both click methods failed: {str(js_error)}")
                    raise
            
            time.sleep(1)
            import pyperclip
            clipboard_content = pyperclip.paste()
            print("✓ Content successfully copied")
            return clipboard_content

        except Exception as copy_error:
            print(f"❌ Error in copy button handling: {str(copy_error)}")
            
            # Fallback: Get text directly from the response
            print("Attempting fallback method...")
            try:
                response_elements = driver.find_elements(By.XPATH, response_container_xpath)
                if response_elements:
                    last_response = response_elements[-1]
                    # Use JavaScript to get formatted text
                    formatted_text = driver.execute_script("""
                        var element = arguments[0];
                        var text = '';
                        function extractText(node) {
                            if (node.nodeType === Node.TEXT_NODE) {
                                text += node.textContent + '\\n';
                            } else if (node.nodeName === 'PRE') {
                                text += '```\\n' + node.textContent + '\\n```\\n';
                            } else if (node.nodeName === 'CODE') {
                                text += '`' + node.textContent + '`';
                            } else {
                                for (var child of node.childNodes) {
                                    extractText(child);
                                }
                            }
                        }
                        extractText(element);
                        return text.trim();
                    """, last_response)
                    print("✓ Fallback method successful")
                    return formatted_text
                else:
                    raise Exception("No response elements found")
            except Exception as fallback_error:
                print(f"❌ Fallback method failed: {str(fallback_error)}")

                # Fallback : Second Method
                print("Attempting fallback method...")
                try:
                    response_elements = driver.find_elements(
                        By.XPATH, 
                        "//div[contains(@class, 'markdown prose w-full break-words')]"
                    )
                    if response_elements:
                        fallback_text = response_elements[-1].text
                        print("✓ Fallback method successful")
                        return fallback_text
                    else:
                        print("❌ Fallback method failed: No response elements found")
                except Exception as fallback_error:
                    print(f"❌ Fallback method failed: {str(fallback_error)}")

    except Exception as e:
        print(f"❌ Process failed: {str(e)}")
        return f"Error occurred: {str(e)}"

def stop_chat_gpt():
    driver.close()
    driver.quit()

    # chrome_handler.kill_chrome()
    
if __name__ == "__main__":
    start_chat_gpt()
    
    try:
        while True:
            req = input("Enter text: ")
            if req == "!quit":
                break
            resp = make_gpt_request_and_copy(req)
            print(resp)
    except KeyboardInterrupt:
        print("KeyboardInterrupt detected, exiting...")
    finally:
        stop_chat_gpt()
