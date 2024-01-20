from api_backend import start_chat_gpt, make_gpt_request, stop_chat_gpt

start_chat_gpt()
a = make_gpt_request("This just a test prompt ChatGPT")
print(a)
stop_chat_gpt()