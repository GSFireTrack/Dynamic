from datetime import datetime


def criar_no_lista(acao, timestamp, ocorrencia_id):
    """Cria um novo nó para a lista ligada"""
    return {
        "acao": acao,
        "timestamp": timestamp,
        "ocorrencia_id": ocorrencia_id,
        "proximo": None,
    }


def criar_lista_ligada():
    """Cria uma nova lista ligada vazia"""
    return {"cabeca": None, "tamanho": 0}


def inserir_inicio_lista(lista, acao, timestamp, ocorrencia_id):
    """Insere uma nova ação no início da lista"""
    novo_no = criar_no_lista(acao, timestamp, ocorrencia_id)
    novo_no["proximo"] = lista["cabeca"]
    lista["cabeca"] = novo_no
    lista["tamanho"] += 1
    return lista


def listar_historico_lista(lista, limite=10):
    """Lista o histórico de ações (últimas 'limite' ações)"""
    historico = []
    atual = lista["cabeca"]
    contador = 0

    while atual and contador < limite:
        historico.append(
            {
                "acao": atual["acao"],
                "timestamp": atual["timestamp"].strftime("%d/%m/%Y %H:%M:%S"),
                "ocorrencia_id": atual["ocorrencia_id"],
            }
        )
        atual = atual["proximo"]
        contador += 1

    return historico


def tamanho_lista(lista):
    """Retorna o tamanho da lista"""
    return lista["tamanho"]


def lista_vazia(lista):
    """Verifica se a lista está vazia"""
    return lista["cabeca"] is None


def limpar_lista(lista):
    """Remove todos os elementos da lista"""
    lista["cabeca"] = None
    lista["tamanho"] = 0
    return lista


def buscar_por_ocorrencia(lista, ocorrencia_id):
    """Busca todas as ações relacionadas a uma ocorrência específica"""
    acoes_encontradas = []
    atual = lista["cabeca"]

    while atual:
        if atual["ocorrencia_id"] == ocorrencia_id:
            acoes_encontradas.append(
                {
                    "acao": atual["acao"],
                    "timestamp": atual["timestamp"].strftime("%d/%m/%Y %H:%M:%S"),
                    "ocorrencia_id": atual["ocorrencia_id"],
                }
            )
        atual = atual["proximo"]

    return acoes_encontradas
