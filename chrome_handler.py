import os
import subprocess
import time
import sys
import platform

def get_chrome_path():
    os_name = platform.system().lower()
    if os_name == "darwin":
        return "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    elif os_name == "windows":
        return "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
    elif os_name == "linux":
        return "/usr/bin/google-chrome"
    else:
        raise Exception(f"Unsupported OS: {os_name}")
    
def start_chrome():
    chrome_path = get_chrome_path()
    subprocess.Popen([f'{chrome_path}','--remote-debugging-port=9222','--user-data-dir=chromedata'],stdout = subprocess.PIPE, stderr = subprocess.PIPE)

def kill_chrome():
    subprocess.run(['killall','chrome'])

if __name__ == "__main__":
    if sys.argv[1] == "s":
        start_chrome()
    elif sys.argv[1] == "k":
        kill_chrome()