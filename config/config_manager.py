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
        self.save_config()

    @property
    def config(self) -> Config:
        """Retorna a configuração atual."""
        return self._config

    def update_config(self, **kwargs) -> None:
        """Atualiza a configuração com os parâmetros fornecidos."""
        for key, value in kwargs.items():
            if hasattr(self._config, key):
                if key == "theme" and isinstance(value, str):
                    value = TerminalTheme(value)
                setattr(self._config, key, value)
        self.save_config()
