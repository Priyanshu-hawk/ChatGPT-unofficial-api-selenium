import os
import subprocess
import time
import sys

def start_chrome():
    subprocess.Popen(['google-chrome','--remote-debugging-port=9222','--user-data-dir=chromedata'],stdout = subprocess.PIPE, stderr = subprocess.PIPE)

def kill_chrome():
    subprocess.run(['killall','chrome'])

if __name__ == "__main__":
    if sys.argv[1] == "s":
        start_chrome()
    elif sys.argv[1] == "k":
        kill_chrome()