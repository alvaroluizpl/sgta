#!/bin/sh
# O comando acima avisa o sistema que isso é um script shell (sh).
# Usamos sh e não bash porque a imagem python:3.12-slim garante o sh,
# mas não necessariamente o bash. O Dockerfile também chama com "sh entrypoint.sh".

echo "Verificando o banco de dados..."
# (Aqui poderia ter um código para testar a conexão com o banco)

echo "Aplicando as migrações no banco de dados..."
python manage.py migrate

echo "Iniciando o servidor Python..."

# significa, em termos simples: "Terminei de preparar o terreno. Agora, pegue o comando principal que o usuário queria rodar e execute-o."
exec "$@"
