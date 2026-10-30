from dotenv import load_dotenv
load_dotenv()

from langchain.chat_models import init_chat_model

model = init_chat_model("gpt-4o-mini", model_provider="openai")

response = model.invoke("用一句話介紹台灣的秋天")

print(type(response))
print(response.content)
print(response.usage_metadata)