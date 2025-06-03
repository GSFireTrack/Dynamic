from collections import deque


def criar_fila():
    """Cria uma nova fila vazia usando deque"""
    return deque()


def enfileirar(fila, item):
    """Adiciona um item ao final da fila"""
    fila.append(item)
    return fila


def desenfileirar(fila):
    """Remove e retorna o item do início da fila"""
    if fila_vazia(fila):
        return None
    return fila.popleft()


def ver_inicio_fila(fila):
    """Retorna o item do início da fila sem removê-lo"""
    if fila_vazia(fila):
        return None
    return fila[0]


def fila_vazia(fila):
    """Verifica se a fila está vazia"""
    return len(fila) == 0


def listar_fila(fila):
    """Retorna uma lista com os itens da fila (do início ao fim)"""
    return list(fila)


def limpar_fila(fila):
    """Remove todos os itens da fila"""
    fila.clear()
    return fila
