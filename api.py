from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os

# Nuevo cliente OpenAI v1
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    agent: str = "generic"

@app.post("/api/chat")
async def chat(req: ChatRequest):
    system_message = f"Eres el agente {req.agent} de la AI Factory. Responde de forma técnica, precisa y estructurada."

    # Llamado correcto con la nueva API
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": req.message}
        ]
    )

    reply = response.choices[0].message.content
    return {"reply": reply}
