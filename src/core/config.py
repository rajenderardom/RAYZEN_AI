"""
RAYZEN AI
Configuration Manager

Version : 0.1.0 Genesis
"""

from dataclasses import dataclass


@dataclass
class AppConfig:
    """Stores application configuration."""

    app_name: str = "RAYZEN AI"
    version: str = "0.1.0 Genesis"
    author: str = "Rajender Kumar"
    debug: bool = True
