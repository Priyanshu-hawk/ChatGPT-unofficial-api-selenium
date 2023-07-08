from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

from selenium.webdriver.remote.webdriver import WebDriver
import os

import chrome_handler
import helper_funcs
import sys

chrome_handler.start_chrome()

service = Service(os.getcwd() + "/chromedriver")

chrome_options = webdriver.ChromeOptions()

chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
# chrome_options.add_argument("--headless")

driver = webdriver.Chrome(service=service, options=chrome_options)
driver.maximize_window()
driver.get("https://chat.openai.com/chat")

helper_fn = helper_funcs.HelperFn(driver)

def start_chat_gpt():
    #if login page is present
    time.sleep(2)
    login_msg_xpath = "//*[contains(text(), 'Log in with your OpenAI account to continue')]"
    login_page = helper_fn.is_element_present(login_msg_xpath)
    if login_page:
        login_btn_xpath = "//*[@class='btn relative btn-primary']//*[contains(text(), 'Log in')]"
        helper_fn.wait_for_element(login_btn_xpath)
        login_button = helper_fn.find_element(login_btn_xpath)
        login_button.click()
        
        time.sleep(2)
        #google login
        google_btn_xpath = "//*[@data-provider='google']"
        helper_fn.wait_for_element(google_btn_xpath)
        google_btn = helper_fn.find_element(google_btn_xpath)
        google_btn.click()

        time.sleep(2)
        #select mail
        gmail_xpath = "//*[contains(text(), 'PRIYANSHU PATEL')]"
        helper_fn.wait_for_element(gmail_xpath)
        gmail = helper_fn.find_element(gmail_xpath)
        gmail.click()

    else:
        print("Already logged in")

def make_gpt_request(text):

    time.sleep(3)
    text_area_xpath = "//*[@id='prompt-textarea']"
    helper_fn.wait_for_element(text_area_xpath)
    if helper_fn.is_element_present(text_area_xpath):
        text_area = helper_fn.find_element(text_area_xpath)
        text_area.send_keys(text)

        #send button
        send_btn_xpath = "/html/body/div[1]/div[1]/div[2]/div/main/div[3]/form/div/div/button"
        helper_fn.wait_for_element(send_btn_xpath)
        send_btn = helper_fn.find_element(send_btn_xpath)
        time.sleep(2)
        send_btn.click()

    time.sleep(5)
    #waiting for response
    response_xpath = "//*[@class='markdown prose w-full break-words dark:prose-invert light']"
    regenrate_xpath = "//*[contains(text(), 'Regenerate response')]"
    helper_fn.wait_for_element(regenrate_xpath,120)
    if helper_fn.is_element_present(response_xpath):
        response = helper_fn.find_elements(response_xpath)[-1]
        # print(response.text)
        return response.text # will return all the texual information under that perticular xpath



def stop_chat_gpt():
    driver.close()
    chrome_handler.kill_chrome()
    
if __name__ == "__main__":
    start_chat_gpt()

    while True:
        req = input("Enter text: ")
        if req == "i quit!":
            break
        resp = make_gpt_request(req)
        print(resp)
        
    stop_chat_gpt()