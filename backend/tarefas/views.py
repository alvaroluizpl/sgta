import json  # Módulo padrão do Python para trabalhar com JSON (serialização e desserialização)
from django.http import JsonResponse                      # Classe que serializa Python → JSON e retorna como resposta HTTP
from django.utils import timezone                         # Utilitário do Django para obter data/hora respeitando o fuso configurado
from django.views.decorators.csrf import csrf_exempt      # Desativa a verificação de token CSRF para APIs sem sessão de navegador

from .models import Tarefa             # Importa o model Tarefa deste mesmo app (ponto = pacote atual)


# ─── Funções auxiliares ───────────────────────────────────────────────────────

def _serializar_tarefa(tarefa):
    """
    Converte um objeto Tarefa (instância do model) em um dicionário Python.
    Usamos esta função em vez de .values() para controlar exatamente quais campos
    aparecem na resposta e como eles são formatados (ex.: nome do usuário em vez do ID).
    """
    return {
        'id': tarefa.id,                        # Chave primária gerada automaticamente pelo banco
        'titulo': tarefa.titulo,                # Texto curto que identifica a tarefa
        'descricao': tarefa.descricao,          # Texto longo com os detalhes da tarefa
        'status': tarefa.status,                # Ex.: 'ABERTA', 'CONCLUIDA'
        'prioridade': tarefa.prioridade,        # Ex.: 'URGENTE', 'NAO_URGENTE'
        'data_criacao': tarefa.data_criacao,    # Data/hora em que a tarefa foi criada
        'data_entrega': tarefa.data_entrega,    # Data limite para conclusão

        # Se a tarefa tiver um usuário responsável associado, exibe o nome dele.
        # O operador ternário (if/else em linha) evita AttributeError quando o
        # campo é NULL no banco — nesse caso retornamos None (que vira null no JSON).
        'usuario_responsavel': (
            tarefa.usuario_responsavel.nome
            if tarefa.usuario_responsavel else None
        ),
    }


def _queryset_para_lista(qs):
    """
    Aplica _serializar_tarefa em cada item de um QuerySet e retorna uma lista de dicionários.

    qs.select_related('usuario_responsavel') instrui o Django a fazer um SQL JOIN
    entre as tabelas 'tarefas' e 'usuarios' em uma única query, trazendo o usuário
    junto com cada tarefa. Sem isso, cada chamada a tarefa.usuario_responsavel.nome
    dispararia uma query extra no banco — o chamado problema N+1 queries.

    A list comprehension [ f(t) for t in ... ] percorre o QuerySet item a item,
    aplicando _serializar_tarefa(t) em cada tarefa 't', e coleta os resultados em uma lista.
    """
    return [_serializar_tarefa(t) for t in qs.select_related('usuario_responsavel')]


# ─── Views de leitura (GET) ───────────────────────────────────────────────────

def listar_tarefas(request):
    """
    Retorna todas as tarefas cadastradas no banco de dados.
    Endpoint: GET /api/tarefas/
    """
    # Busca todos os registros da tabela Tarefa.
    # select_related já faz o JOIN com usuarios para evitar N+1 queries.
    tarefas = Tarefa.objects.select_related('usuario_responsavel').all()

    # Serializa cada tarefa em dicionário e converte a lista para JSON.
    # safe=False é obrigatório quando o objeto raiz da resposta é uma lista
    # (por padrão, JsonResponse só aceita dicionário na raiz por segurança).
    return JsonResponse([_serializar_tarefa(t) for t in tarefas], safe=False)


def listar_tarefas_por_status(request, status):
    """
    Retorna somente as tarefas que possuem o status informado na URL.
    Endpoint: GET /api/tarefas/status/<status>/
    Exemplo: GET /api/tarefas/status/ABERTA/
    """
    # Extrai apenas os valores internos (primeiro elemento de cada tupla)
    # da lista STATUS_CHOICES: ['ABERTA', 'EM_ANDAMENTO', 'CONCLUIDA', 'CANCELADA']
    status_validos = [choice[0] for choice in Tarefa.STATUS_CHOICES]

    # Se o status recebido não estiver na lista, retorna erro HTTP 400 (Bad Request).
    if status not in status_validos:
        return JsonResponse({'erro': 'Status inválido.'}, status=400)

    # Filtra as tarefas pelo status e converte o QuerySet em lista JSON.
    return JsonResponse(
        _queryset_para_lista(Tarefa.objects.filter(status=status)),
        safe=False,
    )


def listar_tarefas_por_prioridade(request, prioridade):
    """
    Retorna somente as tarefas que possuem a prioridade informada na URL.
    Endpoint: GET /api/tarefas/prioridade/<prioridade>/
    Exemplo: GET /api/tarefas/prioridade/URGENTE/
    """
    # Extrai os valores válidos de prioridade: ['URGENTE', 'NAO_URGENTE']
    prioridades_validas = [choice[0] for choice in Tarefa.PRIORIDADE_CHOICES]

    # Valida a prioridade recebida antes de consultar o banco.
    if prioridade not in prioridades_validas:
        return JsonResponse({'erro': 'Prioridade inválida.'}, status=400)

    # Filtra as tarefas pela prioridade e converte o QuerySet em lista JSON.
    return JsonResponse(
        _queryset_para_lista(Tarefa.objects.filter(prioridade=prioridade)),
        safe=False,
    )


def buscar_tarefa_por_id(request, tarefa_id):
    """
    Retorna os dados de uma única tarefa identificada pelo ID na URL.
    Endpoint: GET /api/tarefas/<tarefa_id>/
    Exemplo: GET /api/tarefas/5/
    """
    try:
        # .get(id=tarefa_id) busca exatamente um registro pelo ID.
        # Lança Tarefa.DoesNotExist se não encontrar nenhum registro com aquele ID.
        tarefa = Tarefa.objects.select_related('usuario_responsavel').get(
            id=tarefa_id
        )
        # Retorna o dicionário serializado da tarefa como JSON (HTTP 200 por padrão).
        return JsonResponse(_serializar_tarefa(tarefa))

    except Tarefa.DoesNotExist:
        # Quando o ID não existe no banco, retornamos HTTP 404 (Not Found)
        # com uma mensagem de erro explicativa.
        return JsonResponse({'erro': 'Tarefa não encontrada.'}, status=404)


def listar_tarefas_atrasadas(request):
    """
    Retorna tarefas cujo prazo de entrega já passou e que ainda não foram concluídas.
    Endpoint: GET /api/tarefas/atrasadas/
    """
    # timezone.now() retorna o datetime atual respeitando o fuso do settings.
    # .date() extrai apenas a parte da data (ano, mês, dia), descartando hora/minuto.
    hoje = timezone.now().date()

    qs = Tarefa.objects.filter(
        data_entrega__lt=hoje   # __lt = "less than" (menor que): data_entrega < hoje
    ).exclude(
        status='CONCLUIDA'      # .exclude() remove da consulta tarefas já finalizadas
    )

    # Converte o QuerySet filtrado em lista JSON.
    return JsonResponse(_queryset_para_lista(qs), safe=False)


def buscar_tarefas_por_titulo(request, termo):
    """
    Busca tarefas cujo título contenha o termo informado na URL.
    A busca é parcial e ignora maiúsculas/minúsculas (case-insensitive).
    Endpoint: GET /api/tarefas/busca/<termo>/
    Exemplo: GET /api/tarefas/busca/reuniao/ → encontra "Reunião de planejamento"
    """
    # titulo__icontains: 'i' = case-insensitive, 'contains' = contém o trecho.
    # Equivale a: WHERE LOWER(titulo) LIKE LOWER('%termo%') no SQL.
    return JsonResponse(
        _queryset_para_lista(Tarefa.objects.filter(titulo__icontains=termo)),
        safe=False,
    )


def listar_tarefas_por_status_e_prioridade(request, status, prioridade):
    """
    Retorna tarefas que combinam simultaneamente o status E a prioridade informados.
    Endpoint: GET /api/tarefas/status/<status>/prioridade/<prioridade>/
    Exemplo: GET /api/tarefas/status/ABERTA/prioridade/URGENTE/
    """
    # Valida os dois parâmetros antes de qualquer consulta ao banco.
    status_validos = [choice[0] for choice in Tarefa.STATUS_CHOICES]
    prioridades_validas = [choice[0] for choice in Tarefa.PRIORIDADE_CHOICES]

    if status not in status_validos:
        return JsonResponse({'erro': 'Status inválido.'}, status=400)

    if prioridade not in prioridades_validas:
        return JsonResponse({'erro': 'Prioridade inválida.'}, status=400)

    # .filter() com múltiplos argumentos aplica AND entre as condições:
    # WHERE status = 'X' AND prioridade = 'Y'
    qs = Tarefa.objects.filter(status=status, prioridade=prioridade)
    return JsonResponse(_queryset_para_lista(qs), safe=False)


# ─── Escrita (POST / PUT / DELETE) ───────────────────────────────────────────

@csrf_exempt
def criar_tarefa(request):
    """
    Cria uma nova tarefa a partir dos dados enviados no corpo da requisição.
    Endpoint: POST /api/tarefas/criar/

    Campos obrigatórios no JSON: titulo, descricao, prioridade, data_entrega
    Campos opcionais: status (padrão 'ABERTA'), usuario_responsavel_id
    """
    if request.method != 'POST':
        # Rejeita qualquer método diferente de POST com HTTP 405 (Method Not Allowed).
        return JsonResponse({'erro': 'Método não permitido.'}, status=405)

    # request.body contém o corpo bruto da requisição em bytes.
    # json.loads() converte esses bytes em um dicionário Python.
    dados = json.loads(request.body)

    # Valida os campos obrigatórios. Se algum estiver ausente, retorna HTTP 400.
    campos_obrigatorios = ['titulo', 'descricao', 'prioridade', 'data_entrega']
    for campo in campos_obrigatorios:
        if campo not in dados:
            return JsonResponse({'erro': f'Campo obrigatório ausente: {campo}'}, status=400)

    # Valida se a prioridade enviada é um dos valores aceitos pelo model.
    prioridades_validas = [choice[0] for choice in Tarefa.PRIORIDADE_CHOICES]
    if dados['prioridade'] not in prioridades_validas:
        return JsonResponse({'erro': 'Prioridade inválida.'}, status=400)

    # Valida o status somente se ele foi enviado (é opcional).
    if 'status' in dados:
        status_validos = [choice[0] for choice in Tarefa.STATUS_CHOICES]
        if dados['status'] not in status_validos:
            return JsonResponse({'erro': 'Status inválido.'}, status=400)

    # Cria a instância do model com os dados recebidos.
    # .get() no dicionário aceita um segundo argumento: o valor padrão caso a chave não exista.
    tarefa = Tarefa(
        titulo=dados['titulo'],
        descricao=dados['descricao'],
        prioridade=dados['prioridade'],
        data_entrega=dados['data_entrega'],
        status=dados.get('status', 'ABERTA'),
        # usuario_responsavel_id recebe o ID numérico do usuário (ou None se não informado).
        # Usar _id diretamente evita uma query extra para buscar o objeto Usuario.
        usuario_responsavel_id=dados.get('usuario_responsavel_id'),
    )

    # .save() executa o INSERT no banco de dados e preenche tarefa.id com o novo ID gerado.
    tarefa.save()

    # Recarrega a tarefa do banco com o JOIN do usuário para serializar o nome corretamente.
    tarefa = Tarefa.objects.select_related('usuario_responsavel').get(id=tarefa.id)

    # Retorna a tarefa criada com HTTP 201 (Created), o código correto para criação de recurso.
    return JsonResponse(_serializar_tarefa(tarefa), status=201)


@csrf_exempt
def atualizar_tarefa(request, tarefa_id):
    """
    Atualiza os dados de uma tarefa existente identificada pelo ID na URL.
    Endpoint: PUT /api/tarefas/<tarefa_id>/atualizar/

    Apenas os campos enviados no JSON serão alterados (atualização parcial).
    """
    if request.method != 'PUT':
        return JsonResponse({'erro': 'Método não permitido.'}, status=405)

    # Busca a tarefa no banco. Retorna 404 se o ID não existir.
    try:
        tarefa = Tarefa.objects.get(id=tarefa_id)
    except Tarefa.DoesNotExist:
        return JsonResponse({'erro': 'Tarefa não encontrada.'}, status=404)

    dados = json.loads(request.body)

    # Atualiza somente os campos que foram enviados no corpo da requisição.
    # Campos não enviados permanecem com o valor atual da tarefa no banco.
    if 'titulo' in dados:
        tarefa.titulo = dados['titulo']

    if 'descricao' in dados:
        tarefa.descricao = dados['descricao']

    if 'data_entrega' in dados:
        tarefa.data_entrega = dados['data_entrega']

    if 'status' in dados:
        status_validos = [choice[0] for choice in Tarefa.STATUS_CHOICES]
        if dados['status'] not in status_validos:
            return JsonResponse({'erro': 'Status inválido.'}, status=400)
        tarefa.status = dados['status']

    if 'prioridade' in dados:
        prioridades_validas = [choice[0] for choice in Tarefa.PRIORIDADE_CHOICES]
        if dados['prioridade'] not in prioridades_validas:
            return JsonResponse({'erro': 'Prioridade inválida.'}, status=400)
        tarefa.prioridade = dados['prioridade']

    if 'usuario_responsavel_id' in dados:
        # Aceita None para remover o vínculo com o usuário responsável.
        tarefa.usuario_responsavel_id = dados['usuario_responsavel_id']

    # .save() executa o UPDATE no banco com todos os campos alterados acima.
    tarefa.save()

    # Recarrega do banco com o JOIN para serializar o nome do usuário corretamente.
    tarefa = Tarefa.objects.select_related('usuario_responsavel').get(id=tarefa_id)

    return JsonResponse(_serializar_tarefa(tarefa))


@csrf_exempt
def remover_tarefa(request, tarefa_id):
    """
    Remove permanentemente uma tarefa identificada pelo ID na URL.
    Endpoint: DELETE /api/tarefas/<tarefa_id>/remover/
    """
    if request.method != 'DELETE':
        return JsonResponse({'erro': 'Método não permitido.'}, status=405)

    # Busca a tarefa no banco. Retorna 404 se o ID não existir.
    try:
        tarefa = Tarefa.objects.get(id=tarefa_id)
    except Tarefa.DoesNotExist:
        return JsonResponse({'erro': 'Tarefa não encontrada.'}, status=404)

    # .delete() executa o DELETE no banco e remove o registro permanentemente.
    tarefa.delete()

    # Retorna HTTP 200 confirmando a remoção com o ID que foi deletado.
    return JsonResponse({'mensagem': f'Tarefa {tarefa_id} removida com sucesso.'})
