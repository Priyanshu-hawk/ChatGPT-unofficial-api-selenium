from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
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
            resp = make_gpt_request(req)
            print(resp)
    except KeyboardInterrupt:
        print("KeyboardInterrupt detected, exiting...")
    finally:
        stop_chat_gpt()
