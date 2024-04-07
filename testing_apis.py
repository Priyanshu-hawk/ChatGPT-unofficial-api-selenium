from api_backend import load_chrome, start_chat_gpt, make_gpt_request, stop_chat_gpt

start_chat_gpt()
a = make_gpt_request("This just a test promt for the prosing")
print(a)
stop_chat_gpt()