import random
import traceback

from config.constants import DEBUG, REGIOES_PADRAO, SEVERIDADES
from services.simulador_service import (
    criar_simulador,
    inserir_nova_ocorrencia,
    atender_proxima_ocorrencia,
    finalizar_atendimento,
    listar_ocorrencias_pendentes,
    listar_ocorrencias_em_andamento,
    listar_historico_acoes,
    gerar_relatorio_por_regiao,
    simular_chamadas_aleatorias,
    mostrar_status_sistema,
)
from utils.helpers import (
    validar_entrada_numerica,
    limpar_tela,
)
from utils.interface_rich import (
    exibir_menu,
    imprimir_pergunta,
    imprimir_titulo,
    imprimir_erro,
    imprimir_sucesso,
    imprimir_alerta,
    imprimir_info,
)

from rich.console import Console

console = Console()


def processar_opcao_1(simulador):
    imprimir_titulo("Inserir nova ocorrência", emoji="📝", cor="cyan")

    regiao = imprimir_pergunta("Região")
    if not regiao:
        regiao = random.choice(REGIOES_PADRAO)
        imprimir_info(f"Região aleatória selecionada: {regiao}")

    imprimir_info(
        "[bold]Níveis de severidade:[/bold] 1-BAIXA | 2-MEDIA | 3-ALTA | 4-CRITICA"
    )
    entrada_sev = imprimir_pergunta("Severidade (1-4)")

    if validar_entrada_numerica(entrada_sev, 1, 4):
        severidade = int(entrada_sev)
    else:
        severidade = random.choice(list(SEVERIDADES.keys()))
        imprimir_info(f"Severidade aleatória selecionada: {SEVERIDADES[severidade]}")

    descricao = imprimir_pergunta("Descrição da ocorrência")
    if not descricao:
        descricao = "Ocorrência de queimada reportada"

    inserir_nova_ocorrencia(simulador, regiao, severidade, descricao)


def processar_opcao_6(simulador):
    imprimir_titulo("Histórico de ações", emoji="📜", cor="magenta")

    try:
        limite_str = imprimir_pergunta("\nQuantas ações mostrar?", default="10")
        limite = int(limite_str)
    except ValueError:
        limite = 10

    listar_historico_acoes(simulador, limite)


def processar_opcao_8(simulador):
    imprimir_titulo("Simular chamadas aleatórias", emoji="🎲", cor="blue")

    try:
        qtd_str = imprimir_pergunta("Quantas ocorrências simular?", default="5")
        qtd = int(qtd_str)
    except ValueError:
        qtd = 5

    simular_chamadas_aleatorias(simulador, qtd)


def executar_simulador():
    simulador = criar_simulador()

    while True:
        try:
            exibir_menu()
            opcao = console.input("Escolha uma opção: ").strip()
            limpar_tela()

            if opcao == "1":
                processar_opcao_1(simulador)
            elif opcao == "2":
                imprimir_titulo("Atender ocorrência", emoji="🚒", cor="green")
                atender_proxima_ocorrencia(simulador)
            elif opcao == "3":
                imprimir_titulo("Finalizar atendimento", emoji="✅", cor="green")
                finalizar_atendimento(simulador)
            elif opcao == "4":
                imprimir_titulo("Ocorrências pendentes", emoji="📋", cor="yellow")
                listar_ocorrencias_pendentes(simulador)
            elif opcao == "5":
                imprimir_titulo("Ocorrências em andamento", emoji="🔧", cor="yellow")
                listar_ocorrencias_em_andamento(simulador)
            elif opcao == "6":
                processar_opcao_6(simulador)
            elif opcao == "7":
                imprimir_titulo("Relatório por região", emoji="📊", cor="magenta")
                gerar_relatorio_por_regiao(simulador)
            elif opcao == "8":
                processar_opcao_8(simulador)
            elif opcao == "9":
                imprimir_titulo("Status do sistema", emoji="📈", cor="blue")
                mostrar_status_sistema(simulador)
            elif opcao == "0":
                limpar_tela()
                imprimir_sucesso("👋 Encerrando simulador. Até logo!")
                break
            else:
                imprimir_erro("Opção inválida. Tente novamente.")

            input(f"\nPressione Enter para voltar ao menu...")
            limpar_tela()

        except KeyboardInterrupt:
            limpar_tela()
            imprimir_alerta("👋 Encerrando simulador. Até logo!")
            break
        except Exception as e:
            if DEBUG:
                imprimir_erro(f"Erro: {e}")
                traceback.print_exc()
            else:
                imprimir_erro("Ocorreu um erro inesperado. Tente novamente.")
            print("")


if __name__ == "__main__":
    limpar_tela()
    try:
        executar_simulador()
    except Exception as e:
        imprimir_erro(f"Erro ao iniciar o simulador: {e}")
