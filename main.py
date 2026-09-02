from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

# 允許前端網頁跨網域呼叫這個API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

class TextInput(BaseModel):
    text: str

@app.post("/detect")
def detect_emotion(input: TextInput):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "你是情緒分析專家，只能回答「開心」、「難過」或「生氣」三個詞之一，不能有其他文字。"},
            {"role": "user", "content": f"請判斷這句話的情緒：{input.text}"}
        ]
    )
    emotion = response.choices[0].message.content.strip()
    return {"emotion": emotion}