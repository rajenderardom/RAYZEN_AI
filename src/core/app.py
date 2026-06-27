"""
RAYZEN AI
Core Application

Version : 0.1.0 Genesis
"""

class RayzenApp:
    """Main application class for RAYZEN AI."""

    def __init__(self):
        self.name = "RAYZEN AI"
        self.version = "0.1.0 Genesis"
        self.status = "Ready"

    def start(self):
        print("=" * 50)
        print(f"{self.name}")
        print(f"Version : {self.version}")
        print(f"Status  : {self.status}")
        print("=" * 50)
        print("Core Engine Started Successfully.")
        print("=" * 50)
