from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import json
import logging

logger = logging.getLogger(__name__)


class TerminalTheme(Enum):
    DEFAULT = "default"
    NO_COLOR = "no_color"


@dataclass
class Config:
    theme: TerminalTheme = TerminalTheme.DEFAULT
    debug: bool = False
    delay_time: float = 0.1


class ConfigManager:
    def __init__(self, config_path: str = "config/config.json"):
        self.config_path = Path(config_path)
        self._config = self._load_config()
        self._config_history = []

    def _load_config(self) -> Config:
        """Carrega a configuração do arquivo JSON."""
        try:
            if not self.config_path.exists():
                return Config()

            with open(self.config_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            return Config(
                theme=TerminalTheme(data.get("theme", TerminalTheme.NO_COLOR.value)),
                debug=data.get("debug", True),
                delay_time=data.get("delay_time", 0.1),
            )
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return Config()

    def save_config(self) -> None:
        """Salva a configuração atual no arquivo JSON."""
        try:
            data = {
                "theme": self._config.theme.value,
                "debug": self._config.debug,
                "delay_time": self._config.delay_time,
            }

            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            logger.error(f"Error saving config: {e}")
            raise

    def reset_config(self) -> None:
        """Reseta a configuração para os valores padrão e salva no arquivo."""
        self._config = Config()
        self._config_history.clear()
        self.save_config()

    @property
    def config(self) -> Config:
        """Retorna a configuração atual."""
        return self._config

    def update_config(self, **kwargs) -> None:
        """Atualiza a configuração com os parâmetros fornecidos."""
        self._save_config_state()

        for key, value in kwargs.items():
            if hasattr(self._config, key):
                if key == "theme" and isinstance(value, str):
                    value = TerminalTheme(value)
                setattr(self._config, key, value)
        self.save_config()

    def _save_config_state(self) -> None:
        """Salva o estado atual da configuração na pilha de histórico."""
        current_state = {
            "theme": self._config.theme,
            "debug": self._config.debug,
            "delay_time": self._config.delay_time,
        }
        self._config_history.append(current_state)

        if len(self._config_history) > 10:
            self._config_history.pop(0)

    def undo_last_config_change(self) -> bool:
        """Desfaz a última alteração de configuração."""
        if not self._config_history:
            return False

        previous_state = self._config_history.pop()

        self._config.theme = previous_state["theme"]
        self._config.debug = previous_state["debug"]
        self._config.delay_time = previous_state["delay_time"]

        self.save_config()
        return True

    def has_undo_history(self) -> bool:
        """Verifica se há histórico para desfazer."""
        return len(self._config_history) > 0

    def get_undo_count(self) -> int:
        """Retorna o número de ações que podem ser desfeitas."""
        return len(self._config_history)
