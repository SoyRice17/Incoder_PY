import json
from util import JsonIOManager

class ConfigManager:
    _instance = None
    _config = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_config()
        return cls._instance
    
    def _init_config(self):
        if self._config is None:
            json_manager = JsonIOManager()
            self._config = json_manager.read_json(json_manager.config_path)
            self.json_manager = json_manager
    
    @property
    def config(self):
        return self._config
    
    def save_config(self):
        self.json_manager.write_json(self.json_manager.config_path, self._config)
    
    
