# views.py define as funções que respondem às requisições HTTP do app 'usuarios'.
# Cada função recebe um objeto 'request' (a requisição) e retorna um JsonResponse
# (a resposta em formato JSON enviada ao cliente).

from django.http import JsonResponse  # Classe que converte Python → JSON e retorna como resposta HTTP
from .models import Usuario            # Importa o model Usuario deste mesmo app (ponto = pacote atual)


def listar_usuarios(request):
    """
    Retorna todos os usuários cadastrados no banco de dados.
    Endpoint: GET /api/usuarios/
    """
    # Usuario.objects.all() busca todos os registros da tabela de usuários.
    # .values() converte cada registro em um dicionário Python automaticamente,
    # incluindo todos os campos do model (id, nome, email, ativo, data_criacao).
    usuarios = Usuario.objects.all().values()

    # list(usuarios) converte o QuerySet (que é lazy — só executa a query quando
    # necessário) em uma lista de dicionários concreta, executando o SQL no banco.
    # JsonResponse(..., safe=False) serializa a lista para JSON e a retorna.
    # safe=False é necessário porque o objeto raiz é uma lista, não um dicionário.
    return JsonResponse(list(usuarios), safe=False)


def buscar_usuario_por_id(request, id):
    """
    Retorna os dados de um único usuário identificado pelo ID na URL.
    Endpoint: GET /api/usuarios/<id>/
    Exemplo: GET /api/usuarios/3/
    """
    try:
        # .values() retorna os dados como dicionário em vez de instância do model.
        # .get(id=id) busca exatamente um registro pelo ID primário.
        # Lança Usuario.DoesNotExist se nenhum usuário com esse ID existir.
        usuario = Usuario.objects.values().get(id=id)

        # Retorna o dicionário do usuário como JSON (HTTP 200 por padrão).
        # safe=False é necessário aqui porque .values().get() retorna um dict-like
        # mas o Django trata como objeto genérico e exige o parâmetro.
        return JsonResponse(usuario, safe=False)

    except Usuario.DoesNotExist:
        # Quando o ID não existe no banco, retornamos HTTP 404 (Not Found)
        # com uma mensagem de erro explicativa no corpo da resposta.
        return JsonResponse({'erro': 'Usuário não encontrado.'}, status=404)
