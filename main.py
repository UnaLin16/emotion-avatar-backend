from dotenv import load_dotenv
load_dotenv()

from typing import Literal
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

app = FastAPI()

# 允許前端網頁跨網域呼叫這個API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# 前端傳進來的格式（沒變）
class TextInput(BaseModel):
    text: str


# 模型輸出的格式（新增）
class EmotionResult(BaseModel):
    """使用者文字的情緒分類結果"""
    emotion: Literal["開心", "難過", "生氣"] = Field(
        description="這句話表達的情緒"
    )


model = init_chat_model("gpt-4o-mini", model_provider="openai", temperature=0)
classifier = model.with_structured_output(EmotionResult)

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是情緒分析專家。判斷使用者這句話的情緒，"
               "只能從「開心」「難過」「生氣」三者中選一個。"),
    ("human", "{text}"),
])

chain = prompt | classifier


@app.post("/detect")
def detect_emotion(input: TextInput):
    result = chain.invoke({"text": input.text})
    return {"emotion": result.emotion}