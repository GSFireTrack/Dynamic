import heapq
from models.ocorrencia import comparar_prioridade_ocorrencias


def criar_heap_prioridade():
    """Cria um novo heap de prioridade vazio"""
    return []


def inserir_heap(heap, ocorrencia):
    """Insere uma ocorrência no heap de prioridade"""
    prioridade = calcular_chave_prioridade(ocorrencia)
    item = (prioridade, ocorrencia["timestamp"], ocorrencia)
    heapq.heappush(heap, item)


def remover_heap(heap):
    """Remove e retorna a ocorrência de maior prioridade"""
    if not heap:
        return None
    prioridade, timestamp, ocorrencia = heapq.heappop(heap)
    return ocorrencia


def ver_topo_heap(heap):
    """Retorna a ocorrência de maior prioridade sem removê-la"""
    if not heap:
        return None
    prioridade, timestamp, ocorrencia = heap[0]
    return ocorrencia


def heap_vazio(heap):
    """Verifica se o heap está vazio"""
    return len(heap) == 0


def listar_heap_ordenado(heap):
    """Retorna uma lista ordenada das ocorrências no heap (sem modificar o heap)"""
    if not heap:
        return []

    heap_temp = heap.copy()
    ocorrencias = []

    while heap_temp:
        _, _, ocorrencia = heapq.heappop(heap_temp)
        ocorrencias.append(ocorrencia)

    return ocorrencias


def calcular_chave_prioridade(ocorrencia):
    """Calcula a chave de prioridade para uma ocorrência"""
    severidade = ocorrencia["severidade"]
    timestamp = ocorrencia["timestamp"].timestamp()
    return (-severidade, timestamp)  # Negando a severidade para criar um heap máximo
