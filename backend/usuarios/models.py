# models.py define a estrutura da tabela de usuários no banco de dados.
# A classe Usuario herda de models.Model, o que faz o Django criar e gerenciar
# a tabela correspondente automaticamente via migrations.

from django.db import models  # Importa a base para criação de modelos Django


class Usuario(models.Model):
    # Nome completo do usuário — texto curto, limitado a 255 caracteres.
    nome = models.CharField(max_length=255)

    # Endereço de e-mail do usuário.
    # EmailField valida automaticamente o formato do e-mail (ex.: precisa ter '@').
    # unique=True garante que não existam dois usuários com o mesmo e-mail no banco.
    email = models.EmailField(unique=True)

    # Indica se o usuário está ativo no sistema.
    # BooleanField armazena True ou False.
    # default=True: todo usuário criado começa ativo por padrão.
    ativo = models.BooleanField(default=True)

    # Data e hora em que o usuário foi cadastrado.
    # auto_now_add=True: o Django preenche este campo automaticamente com o
    # momento exato da criação — não é possível alterar o valor depois.
    data_criacao = models.DateTimeField(auto_now_add=True)

    # Representação textual do objeto, exibida no admin do Django e no shell.
    # Retorna o nome do usuário quando o objeto é convertido para string.
    def __str__(self):
        return self.nome
