"""
RAYZEN AI
Settings Manager

Version : 0.1.0 Genesis
"""


class SettingsManager:
    """Manages application settings."""

    def __init__(self):
        self.settings = {
            "theme": "dark",
            "language": "en",
            "debug": True,
        }

    def get(self, key):
        return self.settings.get(key)

    def set(self, key, value):
        self.settings[key] = value
