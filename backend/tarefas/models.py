# models.py define a estrutura das tabelas do banco de dados para o app 'tarefas'.
# Cada classe que herda de models.Model vira uma tabela no banco.

from django.db import models       # Importa a base para criação de modelos Django
from usuarios.models import Usuario  # Importa o modelo Usuario para criar o relacionamento


class Tarefa(models.Model):
    # Lista de valores válidos para o campo 'status'.
    # Cada tupla tem: (valor salvo no banco, texto exibido ao usuário).
    STATUS_CHOICES = [
        ('ABERTA', 'Aberta'),
        ('EM_ANDAMENTO', 'Em andamento'),
        ('CONCLUIDA', 'Concluída'),
        ('CANCELADA', 'Cancelada'),
    ]

    # Lista de valores válidos para o campo 'prioridade'.
    PRIORIDADE_CHOICES = [
        ('URGENTE', 'Urgente'),
        ('NAO_URGENTE', 'Não urgente'),
    ]

    # Título da tarefa — texto curto, limitado a 255 caracteres.
    titulo = models.CharField(max_length=255)

    # Descrição detalhada da tarefa — texto livre, sem limite de tamanho.
    descricao = models.TextField()

    # Status atual da tarefa. Aceita apenas os valores definidos em STATUS_CHOICES.
    # O valor padrão é 'ABERTA', então toda tarefa criada começa nesse estado.
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ABERTA')

    # Nível de urgência da tarefa. Aceita apenas os valores de PRIORIDADE_CHOICES.
    # Não tem valor padrão: é obrigatório informar ao criar a tarefa.
    prioridade = models.CharField(max_length=20, choices=PRIORIDADE_CHOICES)

    # Data e hora de criação da tarefa.
    # auto_now_add=True faz o Django preencher automaticamente com o momento atual
    # no instante em que o registro é criado — o campo não pode ser editado depois.
    data_criacao = models.DateTimeField(auto_now_add=True)

    # Data (sem hora) em que a tarefa deve ser entregue.
    data_entrega = models.DateField()

    # Relacionamento com o model Usuario (chave estrangeira).
    # on_delete=models.SET_NULL: se o usuário for deletado, este campo vira NULL
    # em vez de apagar a tarefa junto.
    # null=True: permite o valor NULL no banco de dados.
    # blank=True: permite deixar o campo vazio nos formulários/validações Django.
    usuario_responsavel = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # Representação textual do objeto, usada no admin do Django e no shell.
    # Retorna o título da tarefa quando o objeto é convertido para string.
    def __str__(self):
        return self.titulo
