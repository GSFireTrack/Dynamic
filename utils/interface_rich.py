from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from rich.prompt import Prompt

from models.ocorrencia import obter_info_ocorrencia
from utils.helpers import obter_nome_severidade

console = Console()

# ---------------------------------- Menu ----------------------------------- #


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
    titulo = f"[bold {cor}]{emoji} {texto.upper()} {emoji}[/bold {cor}]"
    console.print(
        Panel(titulo, style="bold red", border_style="bright_blue", expand=False)
    )


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


def imprimir_pergunta(texto: str, default: str = None) -> str:
    """Exibe uma pergunta e retorna a resposta do usuário"""
    resposta = Prompt.ask(f"[magenta]{texto}[/magenta]", default=default)
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
        title=f"[bold red]🚒 Atendendo ocorrência {ocorrencia['id']}[/bold red]",
        border_style="red",
        padding=(1, 1, 1, 1),
        expand=False,
    )

    console.print(painel)


def painel_finalizar_atendimento(ocorrencia):
    """Exibe um painel de sucesso ao finalizar o atendimento de uma ocorrência"""
    painel = Panel.fit(
        f"[bold green]✅ Atendimento finalizado para ocorrência {ocorrencia['id']}[/bold green]\n\n"
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
