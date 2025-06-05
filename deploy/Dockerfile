# Usa uma imagem base oficial do Python.
FROM python:3.10-slim
# Define o diretório de trabalho dentro do contêiner.
# É uma boa prática ter um diretório de trabalho específico para sua aplicação.
WORKDIR /app

# Copia o .env primeiro para que as chaves estejam disponíveis para o build
COPY .env .

# Copia o requirements.txt da raiz do projeto para o diretório de trabalho no contêiner.
# Note o uso de "../requirements.txt" porque o Dockerfile está na pasta "deploy".
COPY ../deploy/requirements.txt .

# Instala as dependências.
RUN pip install --no-cache-dir -r requirements.txt

# Copia as pastas de código e dados
COPY ../src ./src
COPY ../data ./data

# Expõe a porta que a aplicação FastAPI vai escutar.
EXPOSE 8085

# Comando para rodar a aplicação quando o contêiner for iniciado.
# O caminho mudou para "src.api:app" porque o arquivo agora está em "src/api.py".
# "src" é o nome da pasta e "api" é o nome do arquivo Python (api.py).
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8085"]