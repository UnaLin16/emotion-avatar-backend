# emotion-avatar-backend

情緒感知 3D 角色 Demo 的後端 API。接收一段中文文字，回傳情緒標籤。

**主專案（前端 + 完整說明）** → https://github.com/UnaLin16/emotion-avatar
**線上 Demo** → https://emotion-avatar.vercel.app

---

## API 規格

### `POST /detect`

**Request**

```json
{ "text": "今天考試考差了心情很差" }
```

**Response**

```json
{ "emotion": "難過" }
```

`emotion` 只會是 `開心`、`難過`、`生氣` 三者之一。

### 快速測試

FastAPI 自動生成的互動測試頁：

```
https://emotion-avatar-backend.onrender.com/docs
```

開啟後展開 `POST /detect` → `Try it out` → 改掉 `string` → `Execute`。

> ⏳ 免費方案閒置後會休眠，首次呼叫需等 30–60 秒喚醒，屬正常現象。

---

## 技術組成

| 項目 | 內容 |
|---|---|
| 框架 | FastAPI |
| 伺服器 | uvicorn |
| 模型 | OpenAI `gpt-4o-mini` |
| 部署 | Render（Free tier） |

情緒分類的做法是以 system prompt 限制輸出範圍，而非使用專門的情緒分類模型：

```python
{"role": "system", "content": "你是情緒分析專家，只能回答「開心」、「難過」或「生氣」三個詞之一，不能有其他文字。"}
```

選型理由見主專案 README 的〈技術決策說明〉。

---

## 本機執行

```bash
git clone https://github.com/UnaLin16/emotion-avatar-backend.git
cd emotion-avatar-backend
pip install -r requirements.txt
```

設定金鑰（PowerShell）：

```powershell
$env:OPENAI_API_KEY="sk-..."
```

啟動：

```bash
uvicorn main:app --reload --port 8000
# → http://127.0.0.1:8000/docs
```

---

## 部署設定（Render）

```
Language         Python 3
Root Directory   留空
Build Command    pip install -r requirements.txt
Start Command    uvicorn main:app --host 0.0.0.0 --port $PORT
Instance Type    Free
Environment      OPENAI_API_KEY = sk-...
```

兩個容易踩的地方：

- **`--port $PORT` 不可寫死。** 雲端平台每次開機分配的埠號不同，寫死會導致部署失敗。
- **金鑰只放在平台的環境變數，不進版控。** 程式碼裡只有 `os.environ.get("OPENAI_API_KEY")`。

---

## 已知限制

- **只有三種情緒**，且無強度維度。
- **CORS 目前設為 `allow_origins=["*"]`**，開放所有來源。這在 Demo 階段可接受，正式環境應限定前端網域。
- **無速率限制**，任何人都能呼叫這支 API 並消耗 OpenAI 額度。
- **冷啟動延遲**：免費方案休眠後首次呼叫需 30–60 秒。這對「即時互動」的使用情境是實質限制，討論見主專案 README〈已知限制〉5.3。
