from pathlib import Path
import tomllib

class ConfigLoader:
    def __init__(self, config_path: str):
        self.config_path = Path(config_path)

    def load(self) -> dict:
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")

        
        with open(self.config_path, "rb") as file:
            config = tomllib.load(file)
        return config