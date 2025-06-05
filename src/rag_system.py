import json
import os
import re
from typing import List, Dict, Any
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import TextLoader
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.schema import Document
from langchain.text_splitter import CharacterTextSplitter
from dotenv import load_dotenv
from .prompts import prompt_produto, prompt_pedido, prompt_politica
from langchain.chains import RetrievalQAWithSourcesChain
from datetime import datetime, timedelta

# Carregar variáveis de ambiente
load_dotenv()
OpenAI()
OpenAIEmbeddings()

# Carrega dados de produtos
def extrair_filtros(pergunta: str):
    filtros = {}
    pergunta = pergunta.lower()

    # Exemplo de filtro: sistema operacional
    if "android" in pergunta:
        filtros["sistema_operacional"] = "android"
    elif "iphone" in pergunta or "ios" in pergunta:
        filtros["sistema_operacional"] = "ios"

    # Filtro por preço máximo
    match = re.search(r"até\s*r?\$?\s*([\d.,]+)", pergunta)
    if match:
        preco_str = match.group(1).replace(".", "").replace(",", ".")
        try:
            filtros["preco_max"] = float(preco_str)
        except:
            pass

    return filtros

def carregar_produtos(pergunta: str):
    filtros = extrair_filtros(pergunta)

    with open("data/produtos.json", encoding="utf-8") as f:
        produtos = json.load(f)

    documentos = []

    for p in produtos:
        if not p["disponivel"]:
            continue

        atende = True

        if "sistema_operacional" in filtros:
            so = p["especificacoes"].get("sistema_operacional", "").lower()
            if filtros["sistema_operacional"] not in so:
                atende = False

        if "preco_max" in filtros:
            if p["preco"] > filtros["preco_max"]:
                atende = False

        if atende:
            texto = f"Nome: {p['nome']}\nDescrição: {p['descricao']}\nPreço: R$ {p['preco']:.2f}\nCategoria: {p['categoria']}\nEspecificações: {p['especificacoes']}"
            documentos.append(Document(page_content=texto))

    return documentos

# Carrega dados dos pedidos
def carregar_pedidos():
    with open("data/pedidos.json", encoding="utf-8") as f:
        dados = json.load(f)
    textos = []
    for pedido in dados:
        data_atual = datetime.now()
        data_previsao = datetime.strptime(pedido['previsao_entrega'], "%Y-%m-%d")
        status = pedido['status']
        if status != "Cancelado" and status != "Entregue":
            if data_previsao.date() < data_atual.date():
                pedido_com_atraso = "Sim"
            else:
                pedido_com_atraso = "Não"
        else:
            pedido_com_atraso = "Não"   
            
        texto = f"ID do Pedido ou #: {pedido['pedido_id']}\nStatus: {pedido['status']}\nData da compra: {pedido['data_compra']}\nPrevisão de entrega: {data_previsao}\nProdutos: {pedido['produtos']}\nPedido com atraso: {pedido_com_atraso}"
        textos.append(Document(page_content=texto))
    return textos

# Carrega dados das politicas
def carregar_politicas() -> List[Document]:
    loader = TextLoader("data/politicas.md") 
    documents = loader.load()
    return documents

# Gera resposta Produtos
def buscar_produtos(pergunta: str) -> str:
    documentos = carregar_produtos(pergunta)
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs_divididos = splitter.split_documents(documentos)

    embeddings = OpenAIEmbeddings()
    vetor = FAISS.from_documents(docs_divididos, embeddings)

    qa = RetrievalQA.from_chain_type(
        llm=OpenAI(temperature=0, max_tokens=1024),
        retriever=vetor.as_retriever(),
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt_produto}
    )

    resposta = qa.run(pergunta)
    return resposta

# Gera resposta Pedidos
def buscar_pedidos(pergunta: str) -> str:
    numero = extrair_numero_pedido(pergunta)    
    if numero and not pedido_existe(numero):
        return f"Desculpe, não encontrei nenhum pedido com o número #{numero}. Por favor, verifique se o número está correto."
   
    documentos = carregar_pedidos()
    splitter = CharacterTextSplitter(chunk_size=800, chunk_overlap=0)
    docs_divididos = splitter.split_documents(documentos)

    embeddings = OpenAIEmbeddings()
    vetor = FAISS.from_documents(docs_divididos, embeddings)

    qa = RetrievalQA.from_chain_type(
        llm=OpenAI(temperature=0),
        retriever=vetor.as_retriever(),
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt_pedido}
    )

    resposta = qa.run(pergunta)
    return resposta

# Gera resposta para Politicas
def buscar_politicas(pergunta: str) -> str:
    documentos = carregar_politicas()
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200) 
    docs_divididos = splitter.split_documents(documentos)

    embeddings = OpenAIEmbeddings()
    vetor = FAISS.from_documents(docs_divididos, embeddings)

    qa = RetrievalQA.from_chain_type(
        llm=OpenAI(temperature=0), 
        retriever=vetor.as_retriever(),
        chain_type="stuff", 
        chain_type_kwargs={"prompt": prompt_politica}
    )

    resposta = qa.run(pergunta)
    return resposta

#validações
def pedido_existe(numero: str) -> bool:
    with open("data/pedidos.json", encoding="utf-8") as f:
        pedidos = json.load(f)
    return any(p["pedido_id"] == numero for p in pedidos)

def extrair_numero_pedido(texto: str) -> str:
    match = re.search(r"#?(\d{3,})", texto)
    return match.group(1) if match else None
