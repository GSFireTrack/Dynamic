def criar_no_arvore(regiao):
    """Cria um novo nó da árvore"""
    return {
        "regiao": regiao,
        "ocorrencias": [],
        "total_ocorrencias": 0,
        "esquerda": None,
        "direita": None,
    }


def criar_arvore_regioes():
    """Cria uma nova árvore de regiões vazia"""
    return {"raiz": None}


def inserir_arvore(arvore, regiao, ocorrencia_id):
    """Insere uma ocorrência em uma região"""
    arvore["raiz"] = _inserir_recursivo(arvore["raiz"], regiao, ocorrencia_id)
    return arvore


def _inserir_recursivo(no, regiao, ocorrencia_id):
    """Inserção recursiva na árvore"""
    if no is None:
        novo_no = criar_no_arvore(regiao)
        novo_no["ocorrencias"].append(ocorrencia_id)
        novo_no["total_ocorrencias"] = 1
        return novo_no

    if regiao == no["regiao"]:
        no["ocorrencias"].append(ocorrencia_id)
        no["total_ocorrencias"] += 1
    elif regiao < no["regiao"]:
        no["esquerda"] = _inserir_recursivo(no["esquerda"], regiao, ocorrencia_id)
    else:
        no["direita"] = _inserir_recursivo(no["direita"], regiao, ocorrencia_id)

    return no


def gerar_relatorio_arvore(arvore):
    """Gera relatório de todas as regiões em ordem"""
    relatorio = []
    _percorrer_em_ordem(arvore["raiz"], relatorio)
    return relatorio


def _percorrer_em_ordem(no, relatorio):
    """Percorre a árvore em ordem para gerar relatório"""
    if no:
        _percorrer_em_ordem(no["esquerda"], relatorio)
        relatorio.append(
            {
                "regiao": no["regiao"],
                "total_ocorrencias": no["total_ocorrencias"],
                "ocorrencias_ids": no["ocorrencias"].copy(),
            }
        )
        _percorrer_em_ordem(no["direita"], relatorio)


def arvore_vazia(arvore):
    """Verifica se a árvore está vazia"""
    return arvore["raiz"] is None


def contar_regioes(arvore):
    """Conta o número total de regiões na árvore"""
    return _contar_nos(arvore["raiz"])


def _contar_nos(no):
    """Conta recursivamente o número de nós"""
    if no is None:
        return 0
    return 1 + _contar_nos(no["esquerda"]) + _contar_nos(no["direita"])


def listar_todas_regioes(arvore):
    """Lista todas as regiões cadastradas em ordem alfabética"""
    regioes = []
    _coletar_regioes(arvore["raiz"], regioes)
    return regioes


def _coletar_regioes(no, regioes):
    """Coleta recursivamente todas as regiões"""
    if no:
        _coletar_regioes(no["esquerda"], regioes)
        regioes.append(no["regiao"])
        _coletar_regioes(no["direita"], regioes)
