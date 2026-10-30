from dotenv import load_dotenv
load_dotenv()

import json
from langchain.chat_models import init_chat_model
from langchain.messages import SystemMessage, HumanMessage

model = init_chat_model("gpt-4o", model_provider="openai")
json_model = model.bind(response_format={"type": "json_object"})

# 1. 角色人設 + 輸出格式規定
SYSTEM_PROMPT = """你是一個名叫小R的機器人陪伴角色。
個性：溫暖、好奇、說話簡短，每次回覆不超過兩句。
任務：判斷使用者這句話的情緒，並用符合角色個性的方式回應。

你擁有這段對話的完整紀錄。每次回覆前，請先回顧前面的對話：
- 使用者提到的人、事、物或喜好，若與先前對話有關，請在回應中自然帶出那些具體內容，
  不要當成第一次聽到；只引用對話紀錄中真正出現過的內容。
- 使用者用「那個」「上次」「還是一樣」等說法指涉先前內容時，從紀錄中找出所指的對象。
- 使用者已經回答過的問題，不要再問一次。
- 只有在紀錄中真的找不到時，才說不記得，並請對方再說一次。
- 使用者說過的事：依對話紀錄回答；紀錄中確實沒有，才說不記得。
- 你本身的知識：有把握就具體回答；沒把握就坦白說不確定，
   不要請使用者重複，也不要用籠統的說法帶過。
- 給建議時：參考使用者已表達的經驗與偏好，避免推薦他已經做過或不喜歡的選項。


請一律以 JSON 格式回覆，只能包含以下兩個欄位：
{"emotion": "開心" 或 "難過" 或 "生氣", "reply": "你要對使用者說的話"}
"""



messages = [SystemMessage(content=SYSTEM_PROMPT)]

print("和小R聊天（輸入 q 結束）")

while True:
    user_text = input("\n你：")
    if user_text.strip().lower() == "q":
        break

    messages.append(HumanMessage(content=user_text))

    response = json_model.invoke(messages)
    data = json.loads(response.content)

    print(f"［情緒：{data['emotion']}］")
    print(f"小R：{data['reply']}")

    messages.append(response)

print(f"\n本次對話共 {len(messages)} 則訊息")

