from django.urls import path
from .views import (
    listar_tarefas,
    listar_tarefas_por_status,
    listar_tarefas_por_prioridade,
    buscar_tarefa_por_id,
    listar_tarefas_por_status_e_prioridade,
    listar_tarefas_atrasadas,
    buscar_tarefas_por_titulo,
    criar_tarefa,
    atualizar_tarefa,
    remover_tarefa,
)

urlpatterns = [
    # ── Leitura (GET) ──────────────────────────────────────────────────────────
    path('tarefas/', listar_tarefas),
    path('tarefas/status/<str:status>/', listar_tarefas_por_status),
    path('tarefas/prioridade/<str:prioridade>/', listar_tarefas_por_prioridade),
    path('tarefas/filtro/<str:status>/<str:prioridade>/', listar_tarefas_por_status_e_prioridade),
    path('tarefas/atrasadas/', listar_tarefas_atrasadas),
    path('tarefas/busca/<str:termo>/', buscar_tarefas_por_titulo),
    path('tarefas/<int:tarefa_id>/', buscar_tarefa_por_id),

    # ── Escrita (POST / PUT / DELETE) ──────────────────────────────────────────
    path('tarefas/criar/', criar_tarefa),                            # POST
    path('tarefas/<int:tarefa_id>/atualizar/', atualizar_tarefa),    # PUT
    path('tarefas/<int:tarefa_id>/remover/', remover_tarefa),        # DELETE
]
