import random
from datetime import datetime
from time import sleep
import uuid

from config.constants import (
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
    listar_heap_ordenado,
    heap_vazio,
)
from structures.fila import (
    criar_fila,
    desenfileirar,
    fila_vazia,
    listar_fila,
    enfileirar,
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
from interfaces.menu import (
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
    tabela_fila_espera,
    tabela_historico_acoes,
    tabela_ocorrencias_andamento,
    tabela_ocorrencias_pendentes,
    selecionar_ocorrencia_atender,
    selecionar_ocorrencia_finalizar,
    painel_ocorrencia_movida_fila_espera,
    painel_atendimento_automatico_fila_espera,
)
from datetime import datetime


def criar_simulador():
    """Cria uma nova instância do simulador"""
    return {
        "fila_espera": criar_fila(),
        "fila_prioridade": criar_heap_prioridade(),
        "ocorrencias_em_andamento": {},
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


def _obter_ocorrencias_disponiveis(simulador):
    """Obtém todas as ocorrências disponíveis para atendimento, priorizando a fila de prioridade"""
    ocorrencias_disponiveis = []

    if not heap_vazio(simulador["fila_prioridade"]):
        ocorrencias_prioridade = listar_heap_ordenado(simulador["fila_prioridade"])
        for ocorrencia in ocorrencias_prioridade:
            ocorrencias_disponiveis.append(
                {
                    "ocorrencia": ocorrencia,
                    "origem": "prioridade",
                    "status_atual": "Pendente",
                }
            )
    elif not fila_vazia(simulador["fila_espera"]):

        ocorrencias_espera = listar_fila(simulador["fila_espera"])
        for ocorrencia in ocorrencias_espera:
            ocorrencias_disponiveis.append(
                {
                    "ocorrencia": ocorrencia,
                    "origem": "espera",
                    "status_atual": "Em Espera",
                }
            )

    return ocorrencias_disponiveis


def _obter_equipes_livres(simulador):
    """Obtém a lista de equipes disponíveis"""
    return [
        equipe
        for equipe in EQUIPES_DISPONIVEIS
        if equipe not in simulador["equipes_ocupadas"]
    ]


def _mover_ocorrencia_para_espera(simulador, ocorrencia):
    """Move uma ocorrência da fila de prioridade para a fila de espera"""
    ocorrencia["status"] = STATUS_OCORRENCIA["EM_ESPERA"]
    enfileirar(simulador["fila_espera"], ocorrencia)

    _remover_ocorrencia_da_prioridade(simulador, ocorrencia["id"])

    acao = f"Ocorrência {ocorrencia['id']} movida para a fila de espera"
    inserir_inicio_lista(simulador["historico"], acao, datetime.now(), ocorrencia["id"])

    print()
    painel_ocorrencia_movida_fila_espera(ocorrencia)


def _remover_ocorrencia_da_prioridade(simulador, ocorrencia_id):
    """Remove uma ocorrência específica da fila de prioridade"""
    todas_ocorrencias = listar_heap_ordenado(simulador["fila_prioridade"])
    simulador["fila_prioridade"] = criar_heap_prioridade()

    for ocorrencia in todas_ocorrencias:
        if ocorrencia["id"] != ocorrencia_id:
            inserir_heap(simulador["fila_prioridade"], ocorrencia)


def _remover_ocorrencia_da_espera(simulador, ocorrencia_id):
    """Remove uma ocorrência específica da fila de espera"""
    todas_ocorrencias = listar_fila(simulador["fila_espera"])
    simulador["fila_espera"] = criar_fila()

    for ocorrencia in todas_ocorrencias:
        if ocorrencia["id"] != ocorrencia_id:
            enfileirar(simulador["fila_espera"], ocorrencia)


def _iniciar_atendimento(simulador, ocorrencia, equipe):
    """Inicia o atendimento de uma ocorrência com uma equipe específica"""
    atribuir_equipe_ocorrencia(ocorrencia, equipe)
    atualizar_status_ocorrencia(ocorrencia, STATUS_OCORRENCIA["EM_ANDAMENTO"])
    simulador["equipes_ocupadas"].add(equipe)

    if "ocorrencias_em_andamento" not in simulador:
        simulador["ocorrencias_em_andamento"] = {}

    simulador["ocorrencias_em_andamento"][ocorrencia["id"]] = ocorrencia

    acao = f"Atendimento iniciado por {equipe}"
    inserir_inicio_lista(simulador["historico"], acao, datetime.now(), ocorrencia["id"])


def atender_proxima_ocorrencia(simulador):
    """Permite selecionar uma ocorrência específica para atender

    Priorização:
    1. Sempre prioriza ocorrências da fila de prioridade (heap)
    2. Só considera fila de espera se não houver ocorrências pendentes
    3. Move ocorrências para espera se não houver equipes disponíveis
    """

    if heap_vazio(simulador["fila_prioridade"]) and fila_vazia(
        simulador["fila_espera"]
    ):
        imprimir_erro("Não há ocorrências pendentes para atender.")
        return None

    ocorrencias_disponiveis = _obter_ocorrencias_disponiveis(simulador)

    item_selecionado = selecionar_ocorrencia_atender(ocorrencias_disponiveis)
    if not item_selecionado:
        return None

    ocorrencia = item_selecionado["ocorrencia"]
    origem = item_selecionado["origem"]

    equipes_livres = _obter_equipes_livres(simulador)

    if not equipes_livres:
        if origem == "prioridade":

            _mover_ocorrencia_para_espera(simulador, ocorrencia)
            return ocorrencia["id"]
        else:

            imprimir_erro(
                "Todas as equipes estão ocupadas. Finalize outras ocorrências primeiro."
            )
            return None

    if origem == "prioridade":
        _remover_ocorrencia_da_prioridade(simulador, ocorrencia["id"])
    else:
        _remover_ocorrencia_da_espera(simulador, ocorrencia["id"])

    equipe = random.choice(equipes_livres)
    _iniciar_atendimento(simulador, ocorrencia, equipe)

    print()
    painel_atender_proxima_ocorrencia(ocorrencia, equipe)

    return ocorrencia["id"]


def _garantir_ocorrencias_em_andamento(simulador):
    """Garante que o dicionário de ocorrências em andamento existe"""
    if "ocorrencias_em_andamento" not in simulador:
        simulador["ocorrencias_em_andamento"] = {}


def _finalizar_ocorrencia(simulador, ocorrencia):
    """Finaliza uma ocorrência específica"""

    del simulador["ocorrencias_em_andamento"][ocorrencia["id"]]

    atualizar_status_ocorrencia(ocorrencia, STATUS_OCORRENCIA["CONCLUIDA"])

    if ocorrencia["equipe_atribuida"]:
        simulador["equipes_ocupadas"].discard(ocorrencia["equipe_atribuida"])

    acao = f"Atendimento finalizado por {ocorrencia['equipe_atribuida']}"
    inserir_inicio_lista(simulador["historico"], acao, datetime.now(), ocorrencia["id"])


def finalizar_atendimento(simulador):
    """Permite selecionar uma ocorrência em andamento específica para finalizar"""
    _garantir_ocorrencias_em_andamento(simulador)

    if not simulador["ocorrencias_em_andamento"]:
        imprimir_erro("Não há ocorrências em andamento para finalizar.")
        return None

    ocorrencias_andamento = list(simulador["ocorrencias_em_andamento"].values())

    ocorrencia = selecionar_ocorrencia_finalizar(ocorrencias_andamento)
    if not ocorrencia:
        return None

    _finalizar_ocorrencia(simulador, ocorrencia)

    print()
    painel_finalizar_atendimento(ocorrencia)

    atender_fila_espera(simulador)

    return ocorrencia["id"]


def atender_fila_espera(simulador):
    """Verifica a fila de espera e tenta atender ocorrências automaticamente"""
    while not fila_vazia(simulador["fila_espera"]):
        equipes_livres = [
            eq for eq in EQUIPES_DISPONIVEIS if eq not in simulador["equipes_ocupadas"]
        ]

        if not equipes_livres:
            break

        ocorrencia = desenfileirar(simulador["fila_espera"])
        if not ocorrencia:
            break

        equipe = random.choice(equipes_livres)

        atribuir_equipe_ocorrencia(ocorrencia, equipe)
        atualizar_status_ocorrencia(ocorrencia, STATUS_OCORRENCIA["EM_ANDAMENTO"])
        simulador["equipes_ocupadas"].add(equipe)

        if "ocorrencias_em_andamento" not in simulador:
            simulador["ocorrencias_em_andamento"] = {}
        simulador["ocorrencias_em_andamento"][ocorrencia["id"]] = ocorrencia

        acao = f"Atendimento retomado (espera) por {equipe}"
        inserir_inicio_lista(
            simulador["historico"], acao, datetime.now(), ocorrencia["id"]
        )

        print()
        painel_atendimento_automatico_fila_espera(ocorrencia, equipe)


def listar_ocorrencias_pendentes(simulador):
    """Lista todas as ocorrências pendentes na fila de prioridade"""
    if heap_vazio(simulador["fila_prioridade"]):
        imprimir_alerta("Não há ocorrências pendentes.")
        return

    ocorrencias = listar_heap_ordenado(simulador["fila_prioridade"])

    tabela_ocorrencias_pendentes(ocorrencias)


def listar_ocorrencias_em_andamento(simulador):
    """Lista todas as ocorrências que estão em andamento"""
    if "ocorrencias_em_andamento" not in simulador:
        simulador["ocorrencias_em_andamento"] = {}

    if not simulador["ocorrencias_em_andamento"]:
        imprimir_alerta("Não há ocorrências em andamento.")
        return

    ocorrencias = list(simulador["ocorrencias_em_andamento"].values())
    tabela_ocorrencias_andamento(ocorrencias)


def listar_ocorrencias_fila_espera(simulador):
    """Lista todas as ocorrências na fila de espera"""
    if fila_vazia(simulador["fila_espera"]):
        imprimir_alerta("Não há ocorrências na fila de espera.")
        return

    ocorrencias = listar_fila(simulador["fila_espera"])

    tabela_fila_espera(ocorrencias)


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
    total_espera = 0
    total_concluidas = 0

    for dados in relatorio:
        status_count = {
            "Pendente": 0,
            "Em Andamento": 0,
            "Em Espera": 0,
            "Concluída": 0,
            "Cancelada": 0,
        }

        for ocorrencia_id in dados["ocorrencias_ids"]:
            if ocorrencia_id in simulador["ocorrencias"]:
                status = simulador["ocorrencias"][ocorrencia_id]["status"]
                status_count[status] += 1

        total_pendentes += status_count["Pendente"]
        total_andamento += status_count["Em Andamento"]
        total_espera += status_count["Em Espera"]
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
        f"\nPendentes: {total_pendentes}, Em Andamento: {total_andamento}, Em Espera: {total_espera}, Concluídas: {total_concluidas}"
    )


def simular_chamadas_aleatorias(simulador, quantidade=5, config_manager=None):
    """Simula a inserção de chamadas aleatórias no sistema"""
    print()
    painel_simulacao_chamadas(quantidade)

    for _ in range(quantidade):
        regiao = random.choice(REGIOES_PADRAO)
        severidade = random.randint(1, 4)
        descricao = random.choice(DESCRICOES_PADRAO)
        inserir_nova_ocorrencia(simulador, regiao, severidade, descricao)
        if config_manager:
            sleep(config_manager.config.delay_time)

    print()
    imprimir_sucesso(f"{quantidade} ocorrências simuladas com sucesso!")


def mostrar_status_sistema(simulador):
    """Mostra o status atual do sistema de combate a queimadas"""
    num_pendentes = len(simulador["fila_prioridade"])

    if "ocorrencias_em_andamento" not in simulador:
        simulador["ocorrencias_em_andamento"] = {}
    num_andamento = len(simulador["ocorrencias_em_andamento"])

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
