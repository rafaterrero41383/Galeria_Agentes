from fastapi import FastAPI
from pydantic import BaseModel
import os
import openai

# Carga tu API KEY como variable de entorno en Render
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()


class ChatRequest(BaseModel):
    message: str
    agent: str = "generic"


@app.post("/api/chat")
async def chat(req: ChatRequest):
    # Aquí puedes cambiar la lógica por agente
    system = f"Eres el agente {req.agent} de la AI Factory. Responde de forma técnica y precisa."

    response = openai.ChatCompletion.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": req.message},
        ]
    )

    reply = response["choices"][0]["message"]["content"]
    return {"reply": reply}
