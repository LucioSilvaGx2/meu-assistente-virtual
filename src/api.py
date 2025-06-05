from fastapi import FastAPI
from pydantic import BaseModel
from .assistente import responder_usuario # Importa a função responder_usuario do módulo assistente
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

app = FastAPI()

class Pergunta(BaseModel):
    mensagem: str

app.mount("/static", StaticFiles(directory="src/static"), name="static")

# 2. Rota para servir o index.html diretamente
@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("src/static/index.html", "r", encoding="utf-8") as f:
        return f.read()


@app.post("/api/assistenteDigital")
async def perguntar(pergunta: Pergunta):
    resposta = responder_usuario(pergunta.mensagem)
    return {"resposta": resposta}
