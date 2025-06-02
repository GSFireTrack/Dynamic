import random
from datetime import datetime
from time import sleep
import uuid

from config.constants import (
    DELAY_TIME,
    DESCRICOES_PADRAO,
    EQUIPES_DISPONIVEIS,
    REGIOES_PADRAO,
    STATUS_OCORRENCIA,
)
from models.ocorrencia import (
    criar_ocorrencia,
    atualizar_status_ocorrencia,
    atribuir_equipe_ocorrencia,
)
from structures.heap_prioridade import (
    criar_heap_prioridade,
    inserir_heap,
    remover_heap,
    listar_heap_ordenado,
    heap_vazio,
)
from structures.pilha import (
    criar_pilha,
    empilhar,
    desempilhar,
    listar_pilha,
    pilha_vazia,
)
from structures.lista_ligada import (
    criar_lista_ligada,
    inserir_inicio_lista,
    listar_historico_lista,
)
from structures.arvore_regioes import (
    criar_arvore_regioes,
    inserir_arvore,
    gerar_relatorio_arvore,
)
from utils.helpers import (
    calcular_tempo_estimado,
    obter_nome_severidade,
)
from utils.interface_rich import (
    imprimir_erro,
    imprimir_alerta,
    imprimir_mensagem,
    imprimir_sucesso,
    painel_atender_proxima_ocorrencia,
    painel_finalizar_atendimento,
    painel_ocorrencia_criada,
    painel_relatorio_regiao,
    painel_simulacao_chamadas,
    painel_status_sistema,
    tabela_historico_acoes,
    tabela_ocorrencias_andamento,
    tabela_ocorrencias_pendentes,
)


from datetime import datetime


def criar_simulador():
    """Cria uma nova instância do simulador"""
    return {
        "fila_prioridade": criar_heap_prioridade(),
        "pilha_em_andamento": criar_pilha(),
        "historico": criar_lista_ligada(),
        "arvore_regioes": criar_arvore_regioes(),
        "ocorrencias": {},
        "equipes_ocupadas": set(),
    }


def inserir_nova_ocorrencia(simulador, regiao, severidade, descricao):
    """Insere uma nova ocorrência no simulador"""
    ocorrencia_id = str(uuid.uuid4())[:8]
    tempo_estimado = calcular_tempo_estimado(severidade)

    ocorrencia = criar_ocorrencia(
        ocorrencia_id, regiao, severidade, descricao, tempo_estimado
    )

    inserir_heap(simulador["fila_prioridade"], ocorrencia)
    simulador["ocorrencias"][ocorrencia_id] = ocorrencia
    inserir_arvore(simulador["arvore_regioes"], regiao, ocorrencia_id)

    acao = f"Nova ocorrência criada: {obter_nome_severidade(severidade)} em {regiao}"
    inserir_inicio_lista(simulador["historico"], acao, datetime.now(), ocorrencia_id)

    painel_ocorrencia_criada(
        regiao,
        severidade,
        tempo_estimado,
        descricao,
        ocorrencia_id,
    )

    return ocorrencia_id


def atender_proxima_ocorrencia(simulador):
    """Atende a próxima ocorrência na fila de prioridade"""
    if heap_vazio(simulador["fila_prioridade"]):
        imprimir_erro("Não há ocorrências pendentes para atender.")
        return None

    equipes_livres = [
        eq for eq in EQUIPES_DISPONIVEIS if eq not in simulador["equipes_ocupadas"]
    ]

    if not equipes_livres:
        imprimir_alerta(
            "Todas as equipes estão ocupadas. Aguarde uma equipe ficar disponível."
        )
        return None

    ocorrencia = remover_heap(simulador["fila_prioridade"])

    equipe = random.choice(equipes_livres)
    atribuir_equipe_ocorrencia(ocorrencia, equipe)
    atualizar_status_ocorrencia(ocorrencia, STATUS_OCORRENCIA["EM_ANDAMENTO"])
    simulador["equipes_ocupadas"].add(equipe)

    empilhar(simulador["pilha_em_andamento"], ocorrencia)

    acao = f"Atendimento iniciado por {equipe}"
    inserir_inicio_lista(simulador["historico"], acao, datetime.now(), ocorrencia["id"])

    painel_atender_proxima_ocorrencia(ocorrencia, equipe)

    return ocorrencia["id"]


def finalizar_atendimento(simulador):
    """Finaliza o atendimento da ocorrência em andamento"""
    if pilha_vazia(simulador["pilha_em_andamento"]):
        imprimir_erro("Não há ocorrências em andamento para finalizar.")
        return None

    ocorrencia = desempilhar(simulador["pilha_em_andamento"])
    atualizar_status_ocorrencia(ocorrencia, STATUS_OCORRENCIA["CONCLUIDA"])

    if ocorrencia["equipe_atribuida"]:
        simulador["equipes_ocupadas"].discard(ocorrencia["equipe_atribuida"])

    acao = f"Atendimento finalizado por {ocorrencia['equipe_atribuida']}"
    inserir_inicio_lista(simulador["historico"], acao, datetime.now(), ocorrencia["id"])

    painel_finalizar_atendimento(ocorrencia)

    return ocorrencia["id"]


def listar_ocorrencias_pendentes(simulador):
    """Lista todas as ocorrências pendentes na fila de prioridade"""
    if heap_vazio(simulador["fila_prioridade"]):
        imprimir_alerta("Não há ocorrências pendentes.")
        return

    ocorrencias = listar_heap_ordenado(simulador["fila_prioridade"])

    tabela_ocorrencias_pendentes(ocorrencias)


def listar_ocorrencias_em_andamento(simulador):
    """Lista todas as ocorrências que estão em andamento na pilha"""
    if pilha_vazia(simulador["pilha_em_andamento"]):
        imprimir_alerta("Não há ocorrências em andamento.")
        return

    ocorrencias = listar_pilha(simulador["pilha_em_andamento"])

    tabela_ocorrencias_andamento(ocorrencias)


def listar_historico_acoes(simulador, limite=10):
    """Lista o histórico de ações do simulador"""
    historico = listar_historico_lista(simulador["historico"], limite)

    if not historico:
        imprimir_alerta("Não há histórico de ações.")
        return

    tabela_historico_acoes(historico, limite)


def gerar_relatorio_por_regiao(simulador):
    """Gera um relatório de ocorrências por região"""
    relatorio = gerar_relatorio_arvore(simulador["arvore_regioes"])

    if not relatorio:
        imprimir_alerta("Não há dados para relatório por região.")
        return

    total_geral = 0
    total_pendentes = 0
    total_andamento = 0
    total_concluidas = 0

    for dados in relatorio:
        status_count = {
            "Pendente": 0,
            "Em Andamento": 0,
            "Concluída": 0,
            "Cancelada": 0,
        }

        for ocorrencia_id in dados["ocorrencias_ids"]:
            if ocorrencia_id in simulador["ocorrencias"]:
                status = simulador["ocorrencias"][ocorrencia_id]["status"]
                status_count[status] += 1

        total_pendentes += status_count["Pendente"]
        total_andamento += status_count["Em Andamento"]
        total_concluidas += status_count["Concluída"]

        total_geral += dados["total_ocorrencias"]

        painel_relatorio_regiao(
            dados["regiao"],
            dados["total_ocorrencias"],
            status_count,
        )

    print()
    imprimir_mensagem("" + "=" * 50)
    imprimir_mensagem(
        f"Total de ocorrências registradas: {total_geral} em {len(relatorio)} regiões."
        f"\nPendentes: {total_pendentes}, Em Andamento: {total_andamento}, Concluídas: {total_concluidas}"
    )


def simular_chamadas_aleatorias(simulador, quantidade=5):
    """Simula a inserção de chamadas aleatórias no sistema"""
    print()
    painel_simulacao_chamadas(quantidade)

    for _ in range(quantidade):
        regiao = random.choice(REGIOES_PADRAO)
        severidade = random.randint(1, 4)
        descricao = random.choice(DESCRICOES_PADRAO)
        inserir_nova_ocorrencia(simulador, regiao, severidade, descricao)
        sleep(DELAY_TIME)

    print()
    imprimir_sucesso(f"{quantidade} ocorrências simuladas com sucesso!")


def mostrar_status_sistema(simulador):
    """Mostra o status atual do sistema de combate a queimadas"""
    num_pendentes = len(simulador["fila_prioridade"])
    num_andamento = len(simulador["pilha_em_andamento"])
    num_equipes_disponiveis = len(EQUIPES_DISPONIVEIS) - len(
        simulador["equipes_ocupadas"]
    )

    painel_status_sistema(
        simulador,
        num_pendentes,
        num_andamento,
        num_equipes_disponiveis,
        len(EQUIPES_DISPONIVEIS),
    )


def simulador_clear(simulador):
    """Limpa o simulador, removendo todas as ocorrências e estruturas internas."""
    simulador["fila_prioridade"] = criar_heap_prioridade()
    simulador["pilha_em_andamento"] = criar_pilha()
    simulador["historico"] = criar_lista_ligada()
    simulador["arvore_regioes"] = criar_arvore_regioes()
    simulador["ocorrencias"] = {}
