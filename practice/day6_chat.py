from dotenv import load_dotenv
load_dotenv()

from typing import Literal
from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


class RobotReply(BaseModel):
    """角色對使用者的回應"""
    emotion: Literal["開心", "難過", "生氣", "中性"] = Field(
        description="使用者這句話表達的情緒，不是角色自己的情緒"
    )
    reply: str = Field(description="角色要對使用者說的話")


model = init_chat_model("gpt-4o-mini", model_provider="openai")
structured_model = model.with_structured_output(RobotReply)

SYSTEM_PROMPT = """你是一個名叫{name}的機器人陪伴角色。
個性：{personality}
任務：判斷使用者這句話的情緒，並用符合角色個性的方式回應。

【記憶規則】
你擁有這段對話的完整紀錄。每次回覆前，請先回顧前面的對話：
- 使用者提到的人、事、物或喜好，若與先前對話有關，請在回應中自然帶出那些具體內容，
  不要當成第一次聽到；只引用對話紀錄中真正出現過的內容。
- 使用者用「那個」「剛剛」「還是一樣」等說法指涉先前內容時，從紀錄中找出所指的對象。
- 使用者已經回答過的問題，不要再問一次。

【回應的三種情況】
1. 使用者說過的事：依對話紀錄回答；紀錄中確實沒有，才說不記得。
2. 你本身的知識：有把握就具體回答；沒把握就坦白說不確定，
   不要請使用者重複，也不要用籠統的說法帶過。
3. 給建議時：參考使用者已表達的經驗與偏好，避免推薦他已經做過或不喜歡的選項。

【個性與規則】
個性只影響你說話的語氣和用字，不影響你是否回答問題。
以上規則優先於個性：即使個性冷淡，被問到對話中出現過的事，仍要如實回答。
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    MessagesPlaceholder("history"),
    ("human", "{user_text}"),
])

chain = prompt | structured_model

CHARACTER = {
    "name": "小R",
    "personality": "溫暖、好奇、說話簡短，每次回覆不超過兩句。",
}
history = []

print(f"和{CHARACTER['name']}聊天（輸入 q 結束）")

while True:
    user_text = input("\n你：")
    if user_text.strip().lower() == "q":
        break

    result = chain.invoke({
        **CHARACTER,
        "history": history,
        "user_text": user_text,
    })

    print(f"［情緒：{result.emotion}］")
    print(f"{CHARACTER['name']}：{result.reply}")

    history.append(HumanMessage(content=user_text))
    history.append(AIMessage(content=result.reply))

print(f"\n本次對話共 {len(history)} 則訊息")