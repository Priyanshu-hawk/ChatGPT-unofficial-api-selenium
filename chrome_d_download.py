from sys import platform
import subprocess, requests, os
import requests, xml.etree.ElementTree as ET
try:
    import selenium
except ModuleNotFoundError:
    print("No selenium found, Installing selenium, Please Wait!!!")
    if platform == "linux":
        subprocess.call("pip3 install selenium", shell=True)
    if platform == "darwin":
        subprocess.call("pip3 install selenium", shell=True)
    if platform == "win32":
        subprocess.call("pip install selenium", shell=True)

curPlt = platform
# https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json - download -> chrome -> {versions}
version_dict = {'linux':0,
                'darwin':2,
                'win32':4
                } # need to improve this

def front_version_extractor(vrsn):
    vrsn = str(vrsn).split(".")
    n_version = ""
    for i in range(len(vrsn)-1):
        n_version+=vrsn[i]
    return n_version

def get_download_version(c_version):
    r = requests.get("https://chromedriver.storage.googleapis.com/?delimiter=/&prefix=")

    version_info = ET.fromstring(r.content)

    for i in version_info.iter('{http://doc.s3.amazonaws.com/2006-03-01}Prefix'):
        curr_version = i.text
        if curr_version != None:
            if front_version_extractor(c_version) == front_version_extractor(curr_version):
                return str(curr_version[:-1])
    
def json_version_extractor(vrsn):
    r = requests.get("https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json")
    data = r.json()

    for i in data['versions']:
        curr_version = i['version']
    
        if curr_version != None:
            if front_version_extractor(vrsn) == front_version_extractor(curr_version):
                down_link = i['downloads']['chromedriver'][version_dict[curPlt]]['url']
                return (str(curr_version), down_link)

def versionChk():
    chrome_version  = subprocess.run(['google-chrome',' --version'], capture_output=True).stdout.decode().split(" ")[2] # chrome version check
    chrome_driver_version = subprocess.run(['./chromedriver',' --version'], capture_output=True).stdout.decode().split(" ")[1] # chromeDriver check
    print(get_download_version(chrome_version), get_download_version(chrome_driver_version))
    return get_download_version(chrome_version) == get_download_version(chrome_driver_version)
    

# todl = subprocess.run(['google-chrome',' --version'], capture_output=True).stdout.decode()
# vrsn  = (todl.split(" "))[2]
# print(vrsn)

# print(json_version_extractor(vrsn))
# print(get_download_version('115.0.5763.0'))


def chromeDriverDownloader():
    if curPlt == 'linux':
        print("[+] Detected System: Linux")
        if not os.path.exists('./chromedriver'):
            try:
                todl = subprocess.run(['google-chrome',' --version'], capture_output=True).stdout.decode()
                vrsn  = (todl.split(" "))[2]

                if front_version_extractor(vrsn) == front_version_extractor("115.0.5762.4"):
                    print("[-]Error Found: manual download required, please download it or update your chrome version!!")
                    exit(0)

                if front_version_extractor(vrsn) < front_version_extractor("115.0.5763.0"):
                    print("Downloading Chromedriver for your system of version:",get_download_version(vrsn))
                    url = "https://chromedriver.storage.googleapis.com/"+get_download_version(vrsn)+"/chromedriver_linux64.zip"
                    r = requests.get(url, allow_redirects=True)
                    
                    if "chromeDriver_zips" not in os.listdir():
                        print("Creating chromeDriver_zips folder")
                        os.mkdir("chromeDriver_zips")

                    open("chromeDriver_zips/chromedriver_linux64.zip","wb").write(r.content)
                else: # if version > 115.x.x.x
                    print("Downloading Chromedriver for your system of version:",json_version_extractor(vrsn)[0])
                    url = json_version_extractor(vrsn)[1]
                    r = requests.get(url, allow_redirects=True)
                    
                    if "chromeDriver_zips" not in os.listdir():
                        print("Creating chromeDriver_zips folder")
                        os.mkdir("chromeDriver_zips")

                    open("chromeDriver_zips/chromedriver_linux64.zip","wb").write(r.content)
            except FileNotFoundError as fnf:
                print("[-]Error Found:",fnf)
                print("[+] Google Chrome is not installed, Please install it!! - https://www.google.com/chrome/")
                exit(0)
            except Exception as e:
                print("[-]Error Found:",e)
                exit(0)
        else:
            if versionChk():
                print("[+] 'Google Chrome' and 'Chromedriver' Version Matched!!")
            else:
                # print("[-] chromedriver version not matched, please install it - https://chromedriver.chromium.org/") # rare case
                print("Removing old chromedrivers!")
                subprocess.run(['rm','chromedriver'])
                subprocess.run(['rm','-rf','chromeDriver_zips'])
                subprocess.run(['mkdir','chromeDriver_zips'])
                chromeDriverDownloader()
    if curPlt == 'darwin':
        print("[+] Detected System: Apple Mac")
        if not os.path.exists('./chromedriver'):
            try:
                todl = subprocess.run(['google-chrome',' --version'], capture_output=True).stdout.decode()
                vrsn  = (todl.split(" "))[2]
                print("Downloading Chromedriver for your system of version:",get_download_version(vrsn))
                url = "https://chromedriver.storage.googleapis.com/"+get_download_version(vrsn)+"/chromedriver_mac64.zip"
                r = requests.get(url, allow_redirects=True)
                
                if "chromeDriver_zips" not in os.listdir():
                    print("Creating chromeDriver_zips folder")
                    os.mkdir("chromeDriver_zips")

                open("chromeDriver_zips/chromedriver_mac64.zip","wb").write(r.content)
            except FileNotFoundError as fnf:
                print("[-]Error Found:",fnf)
                print("[+] Google Chrome is not installed, Please install it!! - https://www.google.com/chrome/")
                exit(0)
        else:
            if versionChk():
                print("'Google Chrome' and 'Chromedriver' Version Matched!!")
            else:
                # print("[-] chromedriver version not matched, please install it - https://chromedriver.chromium.org/") # rare case
                print("Removing old chromedrivers!")
                subprocess.run(['rm','chromedriver'])
                subprocess.run(['rm','-rf','chromeDriver_zips'])
                subprocess.run(['mkdir','chromeDriver_zips'])
                chromeDriverDownloader()
    if curPlt == 'win32':
        print("[+] Detected System: Windows")
        if not os.path.exists('./chromedriver'):
            try:
                todl = os.popen('reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version')
                vrsn = todl.read().split(" ")[-1].strip()
                print("Downloading Chromedriver for your system of version:",get_download_version(vrsn))
                url = "https://chromedriver.storage.googleapis.com/"+get_download_version(vrsn)+"/chromedriver_win32.zip"
                r = requests.get(url, allow_redirects=True)

                if "chromeDriver_zips" not in os.listdir():
                    print("Creating chromeDriver_zips folder")
                    os.mkdir("chromeDriver_zips")

                open("chromeDriver_zips/chromedriver_win32.zip","wb").write(r.content)
            except FileNotFoundError as fnf:
                print("[-]Error Found:",fnf)
                print("[+] Google Chrome is not installed, Please install it!! - https://www.google.com/chrome/")
                exit(0)
        else:
            if versionChk():
                print("'Google Chrome' and 'Chromedriver' Version Matched!!")
            else:
                # print("[-] chromedriver version not matched, please install it - https://chromedriver.chromium.org/") # rare case
                print("Removing old chromedrivers!")
                subprocess.run(['del','chromedriver'])
                subprocess.run(['rmdir','/S','/Q','chromeDriver_zips'])
                subprocess.run(['mkdir','chromeDriver_zips'])
                chromeDriverDownloader()
chromeDriverDownloader()

subprocess.call

print("Unzipping chromedriver")

from unzipper import *