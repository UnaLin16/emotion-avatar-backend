from dotenv import load_dotenv
load_dotenv()

import json
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

model = init_chat_model("gpt-4o-mini", model_provider="openai")
json_model = model.bind(response_format={"type": "json_object"})

# 1. 有變數的人設：{name}、{personality} 之後再填
SYSTEM_PROMPT = """你是一個名叫{name}的機器人陪伴角色。
個性：{personality}
任務：判斷使用者這句話的情緒，並用符合角色個性的方式回應。

（記憶規則、三種情況的規則，從 Day 4 搬過來）

請一律以 JSON 格式回覆，只能包含以下兩個欄位：
{{"emotion": "開心" 或 "難過" 或 "生氣", "reply": "你要對使用者說的話"}}
"""

# 2. Prompt 的結構：人設 → 歷史 → 這一句
prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    MessagesPlaceholder("history"),
    ("human", "{user_text}"),
])

# 3. 用 | 把 prompt 和模型串成一條 chain
chain = prompt | json_model

CHARACTER = {
    "name": "阿冷",
    "personality": "冷淡、毒舌、說話簡短，每次回覆不超過兩句。",
}
history = []

print(f"和{CHARACTER['name']}聊天（輸入 q 結束）")

while True:
    user_text = input("\n你：")
    if user_text.strip().lower() == "q":
        break
    
    # 4. 把所有變數一次填進去
    response = chain.invoke({
        **CHARACTER,
        "history": history,
        "user_text": user_text,
    })
    data = json.loads(response.content)

    print(f"［情緒：{data['emotion']}］")
    print(f"{CHARACTER['name']}：{data['reply']}")

    history.append(HumanMessage(content=user_text))
    history.append(response)

print(f"\n本次對話共 {len(history)} 則訊息")