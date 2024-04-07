# ChatGPT Unofficial API Selenium

## ⭐ Video.

**Link** - https://youtu.be/cMCn2cljlls

## ⭐ Why this API?

This is an unofficial API for ChatGPT using Selenium. it is not recommended to use this API for production. This API is only for testing purposes.

This API is for projects that just need to use the ChatGPT API for testing purposes. And don't want to pay for the official API just for testing.

#### **Note**: This API is extremely slow than the official API. So, it is not recommended to use this API for production. This API is only for testing purposes.

## ⭐ File Structure


### 1. Chromedriver handler
* **chrome_d_download.py** # use to download chrome driver.
* **unzipper.py** # use to unzip chrome driver.

### 2. Use to handle remote chrome browser.
* **chrome_handler.py** # use to handle chrome browser.

### 3. Use to handle ChatGPT and core functions.
* **api_backend.py** # use to handle ChatGPT with selenium.
* **helper_funcs.py** # use to handle core functions of selenium.

## ⭐ Installation.

### 1. Create a virtual environment and activate it.
#### For Linux
```
python3 -m venv venv
source venv/bin/activate
```
#### For Windows
```
python -m venv venv
venv\Scripts\activate
```

### 2. Install requirements
```
pip install -r req.txt
```

### 3. Download chrome driver (this will automatically download chrome driver for your OS)
```
python chrome_d_download.py
```

## ⭐ Loggging in to chatgpt with remote chrome browser.

### 1. Start the remote chrome browser.
```
python chrome_handler.py s
```

***Now you can see a chrome browser window opened. You can use this browser to login to chatgpt. And accept the promepts which are asking for your permission on chatapt page.***

#### https://chat.openai.com/chat paste this link to the remote chrome browser and login to chatgpt.

### 2. Close the remote chrome browser.
```
python chrome_handler.py k
```

## ⭐ Using the API.

### 1. Directly using the API via terminal.
```
python api_backend.py
```
This will open in a terminal where you can type your message and get the response from chatgpt.

To exit the program, in terminal type `i quit!` **(sorry for being weird)** and press enter.

### 2. Using the API in your project via function calls.
```
import api_backend
```

To Start start remote chrome browser and go to chatgpt site. **(Only once)**
```
api_backend.start_chat_gpt()
```

To get response from chatgpt and store it in a variable. **(You can use this function as many times as you want)**
```
variable = api_backend.make_gpt_request("what is gpt model?")
```

To close the remote chrome browser. **(Only once)**
```
api_backend.stop_chat_gpt()
```
#### **Note**: You can run `testing_api.py` file to see how to use the API in your project.

## ⭐ Extras.

* `gmail_xpath` in `start_chat_gpt` function in `api_backend.py` file is the xpath of which search by email holder's name this can be changed to the users name. this will enable auto login to chatgpt if the user is already logged in to `google` in the remote chrome browser.

## ⭐ Improvements.

* `make_gpt_request()` should fuction should be improved to handle errors.
* `make_gpt_request()` should return good formatted response in json format.
* Instead of using `time.sleep()` we should use `implicit wait` and `explicit wait` in selenium.
* We can use `threading` if we want to use the API in multiple projects at the same time.
* The speef of the API should be improved. We can use requests module to improve the speed of the API. Or we can use `asyncio` to improve the speed of the API.

## ⭐ License.

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⭐ Contributing.

You can contribute to this project by making a pull request. If you want to contribute to this project, you can fork this project and make a pull request.

Any type of contribution is welcome. You can contribute to this project by improving the code, adding new features, fixing bugs, etc.

Thank you.

## Star History

<a href="https://star-history.com/#Priyanshu-hawk/ChatGPT-unofficial-api-selenium&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=Priyanshu-hawk/ChatGPT-unofficial-api-selenium&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=Priyanshu-hawk/ChatGPT-unofficial-api-selenium&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=Priyanshu-hawk/ChatGPT-unofficial-api-selenium&type=Date" />
 </picture>
</a>
