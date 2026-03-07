# Usa a imagem oficial do Python 3.12 (leve e segura)
FROM python:3.12-slim

# Define a pasta onde o projeto vai rodar dentro do Container
WORKDIR /app

# Impede o Python de gerar arquivos .pyc / __pycache__ no disco
ENV PYTHONDONTWRITEBYTECODE=1
# Impede o Python de colocar mensagens no buffer (mostra logs na mesma hora)
ENV PYTHONUNBUFFERED=1

# Instala ferramentas do sistema que o pandas/scikit ocasionalmente precisam para compilar
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia os requisitos primeiro (isso usa o cache do Docker, evitando instalar tudo a cada mudança no seu código)
COPY requirements.txt .

# Instala as bibliotecas Python
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copia todo o restante do projeto para dentro do Container
COPY . .

# Comando default: Abre o Jupyter Lab (ótimo para estudos!) para você acessar pelo navegador
CMD ["jupyter", "lab", "--ip='0.0.0.0'", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token='senha123'"]
