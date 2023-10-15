from zipfile import ZipFile
from sys import platform
import os
import subprocess

def move_to_base_project():
    if platform == "linux" or platform == "darwin":
        subprocess.call("mv chromedriver*/* .",shell=True)
    if platform == "win32":
        subprocess.call("move chromedriver*\\* .",shell=True)

def sys_chk_with_path():
    if platform == "linux":
        with ZipFile("chromeDriver_zips/chromedriver_linux64.zip") as toUnzip:
            toUnzip.extractall('.')
        move_to_base_project()
        subprocess.call("chmod +x chromedriver",shell=True)
    if platform == "win32":
        with ZipFile("chromeDriver_zips\\chromedriver_win32.zip") as toUnzip:
            toUnzip.extractall('.')
        move_to_base_project()
    if platform == "darwin":
        with ZipFile("chromeDriver_zips/chromedriver_mac64.zip") as toUnzip:
            toUnzip.extractall('.')
        move_to_base_project()
        subprocess.call("chmod +x chromedriver",shell=True)

if platform == "linux" or platform == "darwin":
    if "chromedriver" not in os.listdir():
        sys_chk_with_path()
if platform == "win32":
    if "chromedriver.exe" not in os.listdir():
        sys_chk_with_path()
