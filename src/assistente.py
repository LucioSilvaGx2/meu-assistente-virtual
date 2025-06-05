from .rag_system import buscar_produtos, buscar_pedidos, buscar_politicas
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from .prompts import prompt_classificacao
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

#Identificar por qual motivo o usuário está entrando em contato
def classificar_intencao_llm(pergunta: str) -> str:
    llm = OpenAI(temperature=0)
    chain = LLMChain(llm=llm, prompt=prompt_classificacao)
    resposta = chain.run(pergunta).strip().lower()

    if resposta in ["produto", "pedido", "politica"]:
        return resposta
    return "desconhecido"

def responder_usuario(mensagem: str) -> str:
    intencao = classificar_intencao_llm(mensagem)
    if intencao == "produto":
        return buscar_produtos(mensagem)

    if intencao == "pedido":
        return buscar_pedidos(mensagem)
    
    if intencao == "politica":
        return buscar_politicas(mensagem)

    return "Desculpe, não consegui entender sua intenção com essa pergunta."
