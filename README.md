# 🤖 Assistente Virtual

Projeto final do curso: desenvolvimento de um **assistente virtual inteligente**, usando **LangChain**, **OpenAI**, **FAISS**, **FastAPI** e **Docker**.

---

## 📌 Objetivo

Criar um assistente que auxilia clientes em:

- 🛍️ Busca inteligente de produtos
- 📦 Consulta de pedidos
- 📜 Informações sobre políticas da loja
- 🎯 Recomendações personalizadas

---

## ⚙️ Tecnologias Utilizadas

| Tecnologia      | Finalidade                              |
|-----------------|------------------------------------------|
| **LangChain**   | Orquestração do RAG e LLM                |
| **OpenAI API**  | Geração de respostas                     |
| **FAISS**       | Busca vetorial local                     |
| **FastAPI**     | Backend da aplicação                     |
| **Docker**      | Containerização e deploy                 |
| **dotenv**      | Variáveis de ambiente (.env)             |

---

## 🏗️ Estrutura do Projeto

```
meu-assistente-virtual/
├── src/
│ ├── api.py # FastAPI com endpoint /api/assistenteDigital
│ ├── assistente.py # Lógica de decisão e roteamento
│ ├── rag_system.py # Lógica RAG por tipo de pergunta
│ ├── prompts.py # Templates de prompt
│ └── static/
│     ├── index.html
│     ├── css/
│     │   └── style.css
│     └── js/
│         └── script.js
├── data/
│ ├── produtos.json # Catálogo de produtos
│ ├── pedidos.json # Base simulada de pedidos
│ └── politicas.md # Texto com políticas da loja
├── deploy/
│ ├── Dockerfile # Imagem Docker
│ └── docker-compose.yml # Orquestração local
├── requirements.txt # Dependências do projeto
├── .env # OPENAI_API_KEY
└── README.md # Documentação
```

---

## 🔑 Endpoints

### `POST /api/assistenteDigital`

Consulta principal do assistente. Recebe uma mensagem e retorna uma resposta inteligente.

**Body JSON:**
```
json
{
  "mensagem": "Quero um notebook até R$ 3.000"
}
```

**Resposta JSON:**
```
json
{
  "resposta": "Olá! Encontrei ótimas opções para você..."
}
```

## 🧠 Funcionalidades

### 1. Busca Inteligente de Produtos

- Busca semântica com LangChain + FAISS
- Filtros por:
  - Preço (ex: “até R$ 1.500”)
  - Sistema operacional (ex: Android, iOS)
- Retorno de sugestões personalizadas com:
  - Nome
  - Descrição
  - Preço
  - Vantagens

### 2. Consulta de Pedidos

- Validação se o número do pedido existe
- Consulta por:
  - Status
  - Data da compra
  - Previsão de entrega
  - Produtos comprados
- Resposta humanizada com tratamento de casos inválidos

### 3. Políticas da Loja

- Responde sobre:
  - Trocas e devoluções
  - Garantias
  - Formas de pagamento
  - Prazos de entrega
- Fonte: `politicas.md`

### 4. Recomendações Personalizadas

- Interpreta preferências do cliente com base na mensagem
- Sugere produtos por categoria ou interesse (ex: “tecnologia”, “culinária”)
- Usa linguagem simpática e contextualizada

---

## 🧠 Prompt Engineering

Cada tipo de pergunta usa um prompt específico:

- `prompt_produto`: resposta completa e formatada para busca de produtos
- `prompt_pedido`: detalhes de pedidos com base nos dados reais
- `prompt_politica`: orientações da loja de forma cordial
- `prompt_classificacao`: classifica a intenção da pergunta para direcionamento correto

---

## 🧪 Exemplos de Uso

| Entrada do Cliente                                           | Resposta Esperada                                |
|--------------------------------------------------------------|--------------------------------------------------|
| "Quero um smartphone Android, até R$ 1.500"                  | Lista de smartphones Android compatíveis         |
| "Como faço para trocar um produto?"                         | Explicação sobre trocas e prazos                 |
| "Meu pedido #12345 já saiu para entrega?"                   | Status atual e previsão de entrega               |
| "Que presente vocês sugerem para quem gosta de cozinhar?"   | Produtos relacionados à culinária                |
| "Oi, tudo bem? Estou procurando um presente para minha mãe" | Saudação + sugestões personalizadas              |

---

## 🚀 Como Executar Localmente

### 1. Configurar `.env`

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```
env
OPENAI_API_KEY=sua-chave-aqui
```

### 2. Executar com Docker Compose
```
docker compose -f deploy/docker-compose.yml up --build -d
```

A API estará disponível em:
http://localhost:8085/api/assistenteDigital

### 3. Executar com Docker Compose

Para usar a interface gráfica basta entrar no link.
http://localhost:8085/

### 4. Render

Para usar a interface gráfica basta entrar no link.
https://meu-assistente-virtual.onrender.com/

A API estará disponível em:
https://meu-assistente-virtual.onrender.com/api/assistenteDigital

---

## 🙌 Autor

Desenvolvido por **Lucio Lucas Moreira da Silva**. 
Contato: [lucio.silva@gx2.com.br](mailto:lucio.silva@gx2.com.br)