from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from rich.prompt import Prompt
from rich.prompt import Confirm

from models.ocorrencia import obter_info_ocorrencia
from utils.helpers import deletar_ocorrencias_json, obter_nome_severidade
from config.config_manager import TerminalTheme
from utils.terminal import get_console

# ---------------------------------- Config ---------------------------------- #
console = get_console()

# ---------------------------------- Menu ----------------------------------- #


def atualizar_console():
    global console
    console = get_console(force_reload=True)


def exibir_menu():
    titulo = "[bold red]🔥 SIMULADOR DE RESPOSTA A QUEIMADAS 🔥[/bold red]"

    tabela = Table.grid(padding=(1, 1), expand=False)
    tabela.add_column(justify="right", no_wrap=True)
    tabela.add_column(no_wrap=True)

    tabela.add_row("1.", "[cyan]📝 Inserir nova ocorrência[/cyan]")
    tabela.add_row("2.", "[green]🚒 Atender próxima ocorrência[/green]")
    tabela.add_row("3.", "[green]✅ Finalizar atendimento[/green]")
    tabela.add_row("4.", "[yellow]📋 Listar ocorrências pendentes[/yellow]")
    tabela.add_row("5.", "[yellow]🔧 Listar ocorrências em andamento[/yellow]")
    tabela.add_row("6.", "[magenta]📝 Ver histórico de ações[/magenta]")
    tabela.add_row("7.", "[magenta]📊 Relatório por região[/magenta]")
    tabela.add_row("8.", "[blue]🎲 Simular chamadas aleatórias[/blue]")
    tabela.add_row("9.", "[blue]📈 Status do sistema[/blue]")
    tabela.add_row("10.", "[red]🔧 Configurações do simulador[/red]")
    tabela.add_row("0.", "[red]🚪 Sair[/red]")

    painel = Panel(
        tabela,
        title=titulo,
        border_style="bright_blue",
        padding=(1, 2, 0, 2),
        expand=False,
    )
    console.print(painel)


# ---------------------------------- Prints ---------------------------------- #


def imprimir_titulo(texto: str, emoji: str = "🔥", cor: str = "red"):
    """Exibe um título em destaque dentro de um painel"""
    titulo = f"[{cor}]{emoji} {texto.upper()} {emoji}[{cor}]"
    console.print(Panel(titulo, style="red", border_style="bright_blue", expand=False))


def imprimir_mensagem(texto: str, estilo: str = "white"):
    """Imprime uma mensagem comum com estilo"""
    console.print(f"[{estilo}]{texto}[/{estilo}]")


def imprimir_sucesso(texto: str):
    """Mensagem de sucesso com ícone verde"""
    console.print(f"[bold green]✅ {texto}[/bold green]")


def imprimir_erro(texto: str):
    """Mensagem de erro com ícone vermelho"""
    console.print(f"\n[bold red]❌ {texto}[/bold red]\n")


def imprimir_alerta(texto: str):
    """Mensagem de alerta com ícone amarelo"""
    console.print(f"\n[yellow]⚠️  {texto}[/yellow]\n")


def imprimir_info(texto: str):
    """Mensagem informativa com estilo azul"""
    console.print(f"[cyan]{texto}[/cyan]")


def imprimir_pergunta(
    texto: str,
    default: str = None,
    cor: str = "magenta",
    accepted_answers: list = None,
    accept_empty: bool = True,
) -> str:

    if accepted_answers:
        accepted_answers = [str(ans).lower() for ans in accepted_answers]
        if accept_empty:
            accepted_answers.append(None)
    while True:
        resposta = Prompt.ask(
            f"[{cor}]{texto}[/{cor}]", default=default, console=console
        )
        if accepted_answers and resposta not in accepted_answers:
            if None in accepted_answers:
                accepted_answers.remove(None)
            accepted_answers = [str(ans) for ans in accepted_answers]
            imprimir_erro(f"Resposta inválida. Aceitas: {', '.join(accepted_answers)}")
            continue
        if resposta:
            return resposta.strip()
        return resposta


def imprimir_divisor(simbolo: str = "─", cor: str = "grey50"):
    """Linha divisória estética"""
    console.rule(character=simbolo, style=cor)


# ------------------------------ Painel & Tabela ----------------------------- #


def painel_ocorrencia_criada(
    regiao, severidade, tempo_estimado, descricao, ocorrencia_id
):
    """Exibe um painel de sucesso ao criar uma nova ocorrência"""
    painel = Panel.fit(
        f"[bold]Região:[/bold] {regiao} | [bold]Severidade:[/bold] {obter_nome_severidade(severidade)} | [bold]Tempo estimado:[/bold] {tempo_estimado}min\n"
        f"[bold]Descrição:[/bold] {descricao if descricao else 'Nenhuma descrição fornecida'}",
        title=f"[bold green]✅ Ocorrência {ocorrencia_id} criada com sucesso![/bold green]\n",
        border_style="green",
        padding=(1, 1, 0, 1),
    )
    print()
    console.print(painel)


def painel_atender_proxima_ocorrencia(ocorrencia, equipe):
    """Exibe um painel para atender a próxima ocorrência"""
    tabela = Table(padding=(0, 1), expand="false", show_header=False, box=None)
    tabela.add_row(
        "[bold]Equipe: [/bold]" + equipe,
        "[bold]Severidade: [/bold]" + obter_nome_severidade(ocorrencia["severidade"]),
    )
    tabela.add_row()
    tabela.add_row(
        "[bold]Região: [/bold]" + ocorrencia["regiao"],
        "[bold]Tempo estimado: [/bold]" + f"{ocorrencia['tempo_estimado']}min",
    )

    painel = Panel(
        tabela,
        title=f"[bold green]Ocorrência {ocorrencia['id']}[/bold green]",
        border_style="green",
        padding=(1, 1, 1, 1),
        expand=False,
    )

    console.print(painel)


def painel_finalizar_atendimento(ocorrencia):
    """Exibe um painel de sucesso ao finalizar o atendimento de uma ocorrência"""
    painel = Panel.fit(
        f"[bold green]✅ Ocorrência {ocorrencia['id']}[/bold green]\n\n"
        f"Equipe [bold]{ocorrencia['equipe_atribuida']}[/bold] agora está disponível",
        border_style="green",
    )
    console.print(painel)


def tabela_ocorrencias_pendentes(ocorrencias):
    """Exibe uma tabela com as ocorrências pendentes"""
    tabela = Table(box=box.SIMPLE_HEAVY)
    tabela.add_column("Nº", style="cyan", justify="right")
    tabela.add_column("ID", style="magenta")
    tabela.add_column("Região", style="green")
    tabela.add_column("Severidade", style="red")
    tabela.add_column("Descrição", style="yellow")
    tabela.add_column("Tempo Estimado", justify="center")
    tabela.add_column("Criada em", style="dim")

    for i, ocorrencia in enumerate(ocorrencias, 1):
        info = obter_info_ocorrencia(ocorrencia)
        tabela.add_row(
            str(i),
            info["id"],
            info["regiao"],
            obter_nome_severidade(info["severidade"]),
            info["descricao"] or "-",
            f"{info['tempo_estimado']} min",
            (
                info["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
                if isinstance(info["timestamp"], datetime)
                else str(info["timestamp"])
            ),
        )
    console.print(tabela)


def tabela_ocorrencias_andamento(ocorrencias):
    """Exibe uma tabela com as ocorrências em andamento"""
    tabela = Table(box=box.SIMPLE_HEAVY)
    tabela.add_column("Nº", style="cyan", justify="right")
    tabela.add_column("ID", style="magenta")
    tabela.add_column("Região", style="green")
    tabela.add_column("Severidade", style="red")
    tabela.add_column("Equipe", style="blue")
    tabela.add_column("Tempo Estimado Restante", justify="center")

    for i, ocorrencia in enumerate(ocorrencias, 1):
        info = obter_info_ocorrencia(ocorrencia)
        tabela.add_row(
            str(i),
            info["id"],
            info["regiao"],
            obter_nome_severidade(info["severidade"]),
            info["equipe_atribuida"] or "-",
            f"{info['tempo_estimado']} min",
        )
    console.print(tabela)


def tabela_historico_acoes(historico, limite=10):
    """Exibe uma tabela com o histórico de ações realizadas"""
    print()
    tabela = Table(
        title=f"📝 Histórico das Últimas {min(limite, len(historico))} Ações",
        box=box.SIMPLE_HEAVY,
    )
    tabela.add_column("Nº", style="cyan", justify="right")
    tabela.add_column("Ação", style="magenta")
    tabela.add_column("Ocorrência", style="green")
    tabela.add_column("Timestamp", style="dim")

    for i, acao in enumerate(historico, 1):
        tabela.add_row(
            str(i),
            acao["acao"],
            acao["ocorrencia_id"],
            (
                acao["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
                if isinstance(acao["timestamp"], datetime)
                else str(acao["timestamp"])
            ),
        )
    console.print(tabela)


def painel_relatorio_regiao(regiao, total_ocorrencias, status_count):
    """Exibe um painel com o relatório de ocorrências por região"""
    print()
    linhas_status = "\n".join(
        f"[bold]{status}:[/bold] {count}"
        for status, count in status_count.items()
        if count > 0
    )

    conteudo = (
        f"{linhas_status}\n\n[bold]Total de ocorrências:[/bold] {total_ocorrencias}"
        if linhas_status
        else f"[bold]Total de ocorrências:[/bold] {total_ocorrencias}"
    )

    painel = Panel.fit(
        conteudo,
        title=f"[bold cyan] Região: {regiao} [/bold cyan]",
        border_style="cyan",
        padding=(1, 1, 0, 1),
    )
    console.print(painel)


def painel_simulacao_chamadas(quantidade):
    """Exibe um painel informativo sobre a simulação de chamadas aleatórias"""
    painel = Panel.fit(
        f"🎲 Simulando {quantidade} chamadas aleatórias",
        title="Simulação de Chamadas Aleatórias",
        border_style="magenta",
        padding=(1, 1, 0, 1),
    )
    console.print(painel)


def painel_status_sistema(
    simulador,
    num_pendentes,
    num_andamento,
    num_equipes_disponiveis,
    equipes_disponiveis,
):
    """Exibe um painel com o status atual do sistema de ocorrências"""
    painel = Panel(
        f"📊 Ocorrências pendentes: {num_pendentes}\n\n"
        f"🚒 Ocorrências em andamento: {num_andamento}\n\n"
        f"👥 Equipes disponíveis: {num_equipes_disponiveis}/{equipes_disponiveis}\n\n"
        + (
            f"🔧 Equipes ocupadas: {', '.join(simulador['equipes_ocupadas'])}\n\n"
            if simulador["equipes_ocupadas"]
            else ""
        )
        + f"📝 Total de ações no histórico: {simulador['historico']['tamanho']}\n\n"
        f"🌍 Total de ocorrências registradas: {len(simulador['ocorrencias'])}",
        border_style="bright_yellow",
        expand=False,
        padding=(1, 2, 1, 2),
    )
    console.print(painel)


def painel_configuracoes_simulador(
    simulador,
    tempo_maximo_resposta,
    tempo_minimo_resposta,
    equipes_disponiveis,
):
    """Exibe um painel com as configurações atuais do simulador"""
    painel = Panel(
        f"⏱️ Tempo máximo de resposta: {tempo_maximo_resposta} min\n\n"
        f"⏱️ Tempo mínimo de resposta: {tempo_minimo_resposta} min\n\n"
        f"👥 Equipes disponíveis: {equipes_disponiveis}\n\n"
        f"📝 Histórico de ações: {simulador['historico']['tamanho']} ações registradas",
        border_style="bright_blue",
        expand=False,
        padding=(1, 2, 1, 2),
    )
    console.print(painel)


def painel_configuracoes_interativas(simulador, config_manager):
    """Exibe as configurações como uma tabela interativa e permite edição"""
    imprimir_titulo("Configurações do Simulador", emoji="⚙️", cor="bright_blue")

    tema_atual = config_manager.config.theme

    tabela = Table(title="🔧 Configurações Atuais", box=box.SIMPLE_HEAVY)
    tabela.add_column("Opção", style="cyan", justify="right")
    tabela.add_column("Parâmetro", style="magenta")
    tabela.add_column("Valor Atual", style="green")

    tabela.add_row(
        "1",
        "Tema do terminal",
        "Sem cor (no_color)" if tema_atual == "no_color" else "Padrão (colorido)",
    )
    tabela.add_row(
        "2",
        "Tempo de delay entre ações",
        str(config_manager.config.delay_time) + " segundos",
    )
    tabela.add_row(
        "3",
        "Modo de depuração",
        "Ativado" if config_manager.config.debug else "Desativado",
    )
    tabela.add_row(
        "4",
        "[yellow]Redefinir configurações para padrão[/yellow]",
        "",
    )
    tabela.add_row(
        "5",
        "[red]Deletar todas as ocorrências[/red]",
        "Todas as ocorrências serão removidas",
    )
    tabela.add_row(
        "0",
        "[red]Voltar ao menu principal[/red]",
        "",
    )

    print()
    console.print(tabela)

    while True:
        escolha = Prompt.ask(
            "[magenta]Digite o número da configuração que deseja alterar[/magenta]",
            default="0",
            show_default=False,
            console=console,
        ).strip()
        if escolha == "0":
            imprimir_info("Retornando ao menu...")
            return
        elif escolha == "1":
            novo_tema = (
                TerminalTheme.NO_COLOR
                if config_manager.config.theme == TerminalTheme.DEFAULT
                else TerminalTheme.DEFAULT
            )
            config_manager.update_config(theme=novo_tema)
            atualizar_console()
            imprimir_info(f"Tema atualizado para: {novo_tema.value}")
            break

        elif escolha == "2":
            novo_delay = Prompt.ask(
                "[magenta]Digite o novo tempo de delay entre ações (em segundos)[/magenta]",
                default=str(config_manager.config.delay_time),
                show_default=True,
            )
            try:
                if float(novo_delay) < 0:
                    raise ValueError
                config_manager.update_config(delay_time=float(novo_delay))
                imprimir_info(
                    f"Tempo de delay atualizado para: {config_manager.config.delay_time} segundos"
                )
            except ValueError:
                imprimir_erro("Valor inválido. Deve ser um número positivo.")
            break
        elif escolha == "3":
            novo_debug = not config_manager.config.debug
            config_manager.update_config(debug=novo_debug)
            imprimir_info(
                f"Modo de depuração {'ativado' if novo_debug else 'desativado'}."
            )
            break
        elif escolha == "4":
            confirmar = Confirm.ask(
                "[red]Tem certeza que deseja redefinir as configurações para o padrão?[/red]",
                default=False,
            )
            if confirmar:
                config_manager.reset_config()
                imprimir_sucesso("Configurações redefinidas para o padrão.")
                atualizar_console()
                break
        elif escolha == "5":
            confirmar = Confirm.ask(
                "[red]Tem certeza que deseja deletar todas as ocorrências? Esta ação não pode ser desfeita![/red]",
                default=False,
            )
            if confirmar:
                deletar_ocorrencias_json()
                from services.simulador_service import simulador_clear

                simulador_clear(simulador)
                imprimir_sucesso("Todas as ocorrências foram deletadas.")
                break
        else:
            imprimir_erro("Opção inválida.")
