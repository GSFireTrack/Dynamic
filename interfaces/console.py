from rich.console import Console
from rich.theme import Theme
import json
from config.config_manager import ConfigManager

_console_instance = None


def carregar_tema(path="data/config.json") -> Theme:
    with open(path, "r") as f:
        styles = json.load(f)
    return styles


def get_console(force_reload=False) -> Console:
    global _console_instance
    if _console_instance is not None and not force_reload:
        return _console_instance

    config_manager = ConfigManager()
    config = config_manager.config
    tema_nome = config.theme.value
    no_color = False
    if tema_nome == "no_color":
        no_color = True

    _console_instance = Console(no_color=no_color)
    return _console_instance
