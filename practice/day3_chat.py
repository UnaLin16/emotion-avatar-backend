import json
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# 1. 角色人設 + 輸出格式規定
SYSTEM_PROMPT = """你是一個名叫小R的機器人陪伴角色。
個性：溫暖、好奇、說話簡短，每次回覆不超過兩句。
任務：判斷使用者這句話的情緒，並用符合角色個性的方式回應。

你擁有這段對話的完整紀錄。每次回覆前，請先回顧前面的對話：
- 使用者提到的人、事、地點、喜好，若與前面談過的內容有關，請自然地接續，
  例如「你上次說的觀音山」，而不是當成第一次聽到。
- 使用者用「那個」「上次」「還是一樣」等說法指涉先前內容時，從紀錄中找出所指的對象。
- 使用者已經回答過的問題，不要再問一次。
- 只有在紀錄中真的找不到時，才說不記得，並請對方再說一次。

請一律以 JSON 格式回覆，只能包含以下兩個欄位：
{"emotion": "開心" 或 "難過" 或 "生氣", "reply": "你要對使用者說的話"}
"""

# 2. 對話歷史：一開始只有人設
messages = [{"role": "system", "content": SYSTEM_PROMPT}]

print("和小R聊天（輸入 q 結束）")

while True:
    user_text = input("\n你：")
    if user_text.strip().lower() == "q":
        break

    # 3. 使用者的話加進歷史
    messages.append({"role": "user", "content": user_text})

    # 4. 把「整份歷史」送給模型
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        response_format={"type": "json_object"},
    )
    raw = response.choices[0].message.content
    data = json.loads(raw)

    print(f"［情緒：{data['emotion']}］")
    print(f"小R：{data['reply']}")

    # 5. 模型的回覆也加進歷史
    messages.append({"role": "assistant", "content": raw})

print(f"\n本次對話共 {len(messages)} 則訊息")