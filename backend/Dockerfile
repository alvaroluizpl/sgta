# Imagem base
# Define qual imagem do Docker Hub usamos como ponto de partida.
# "python:3.12-slim" é uma versão enxuta do Linux com Python 3.12 já instalado.
# "slim" significa que remove ferramentas desnecessárias, deixando a imagem menor.
FROM python:3.12-slim

# Variáveis de ambiente do Python
# Impede o Python de gerar arquivos .pyc (bytecode compilado) dentro do container.
# Esses arquivos são inúteis aqui porque o container não os reutiliza entre execuções.
ENV PYTHONDONTWRITEBYTECODE=1

# Desativa o buffer de saída do Python.
# Sem isso, os prints e logs do Django só apareceriam no terminal em blocos,
# dificultando acompanhar o que está acontecendo em tempo real.
ENV PYTHONUNBUFFERED=1

# Diretório de trabalho 
# Cria a pasta /app dentro do container e define ela como diretório atual.
# Todos os comandos seguintes (COPY, RUN, CMD) rodam a partir dessa pasta.
WORKDIR /app

# Instalação das dependências 
# Copia apenas o requirements.txt primeiro (antes do restante do código).
# Isso aproveita o cache do Docker: se o requirements.txt não mudou,
# o Docker pula o pip install nas próximas builds — muito mais rápido.
COPY requirements.txt .

# Instala todas as bibliotecas listadas no requirements.txt.
# --no-cache-dir evita salvar o cache do pip dentro da imagem, deixando-a menor.
RUN pip install --no-cache-dir -r requirements.txt

# Cópia do código-fonte 
# Copia todo o restante do projeto para dentro do container (pasta /app).
# O .dockerignore garante que venv/, __pycache__ e db.sqlite3 sejam ignorados.
COPY . .

# Ajuste do entrypoint para Windows 
# Arquivos .sh criados no Windows têm \r\n no final de cada linha (CRLF).
# O Linux só entende \n (LF). O sed remove o \r para evitar erros de execução.
# chmod +x dá permissão de execução ao script.
RUN sed -i 's/\r//' entrypoint.sh && chmod +x entrypoint.sh

# Porta exposta 
# Informa ao Docker que o container vai usar a porta 8000.
# Isso não publica a porta — apenas documenta e permite o mapeamento no compose.
EXPOSE 8000

# Inicialização do container 
# ENTRYPOINT define o script que roda SEMPRE que o container inicia.
# Ele executa as migrations e depois passa o controle para o CMD abaixo.
ENTRYPOINT ["sh", "entrypoint.sh"]

# CMD define o comando principal do container (o servidor Django).
# É passado como argumento para o ENTRYPOINT via "$@" no entrypoint.sh.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
