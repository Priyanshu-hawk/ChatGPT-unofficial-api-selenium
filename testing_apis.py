import api_backend

api_backend.start_chat_gpt()
a = api_backend.make_gpt_request("Heleo sir")
print(a)
api_backend.stop_chat_gpt()