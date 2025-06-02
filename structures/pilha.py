def criar_pilha():
    """Cria uma nova pilha vazia"""
    return []


def empilhar(pilha, item):
    """Adiciona um item no topo da pilha"""
    pilha.append(item)
    return pilha


def desempilhar(pilha):
    """Remove e retorna o item do topo da pilha"""
    if pilha_vazia(pilha):
        return None
    return pilha.pop()


def ver_topo_pilha(pilha):
    """Retorna o item do topo da pilha sem removê-lo"""
    if pilha_vazia(pilha):
        return None
    return pilha[-1]


def pilha_vazia(pilha):
    """Verifica se a pilha está vazia"""
    return len(pilha) == 0


def listar_pilha(pilha):
    """Retorna uma lista com os itens da pilha (do topo para a base)"""
    return pilha[::-1]  # Inverte a lista para mostrar do topo para baixo


def limpar_pilha(pilha):
    """Remove todos os itens da pilha"""
    pilha.clear()
    return pilha
