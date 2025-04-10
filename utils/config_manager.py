import os
import json
from pathlib import Path

class ConfigManager:
    def __init__(self):
        self.config_dir = self._get_config_dir()
        self.config_file = os.path.join(self.config_dir, "config.json")
        self.blocklist_ip_file = os.path.join(self.config_dir, "blocklist-ip.json")
        self.blocklist_domain_file = os.path.join(self.config_dir, "blocklist-domain.json")
        self.default_config = {
            "language": "Русский",
            "method": "Метод 1",
            "service_running": False
        }
        
        os.makedirs(self.config_dir, exist_ok=True)
        
        if not os.path.exists(self.config_file):
            self.save_config(self.default_config)
            
        if not os.path.exists(self.blocklist_ip_file):
            self.save_blocklist_ip({"ips": []})
            
        if not os.path.exists(self.blocklist_domain_file):
            self.save_blocklist_domain({"domains": []})
        
    def _get_config_dir(self):
        home = str(Path.home())
        return os.path.join(home, ".meow_bypass")
    
    def load_config(self):
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            self.save_config(self.default_config)
            return self.default_config
    
    def save_config(self, config_data):
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def get_config_dir(self):
        return self.config_dir
    
    def update_setting(self, key, value):
        config = self.load_config()
        config[key] = value
        return self.save_config(config)
    
    def get_setting(self, key, default=None):
        config = self.load_config()
        return config.get(key, default)
        
    def load_blocklist_ip(self):
        try:
            with open(self.blocklist_ip_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            default_data = {"ips": []}
            self.save_blocklist_ip(default_data)
            return default_data
            
    def save_blocklist_ip(self, data):
        try:
            with open(self.blocklist_ip_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"Error saving IP blocklist: {e}")
            return False
            
    def load_blocklist_domain(self):
        try:
            with open(self.blocklist_domain_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            default_data = {"domains": []}
            self.save_blocklist_domain(default_data)
            return default_data
            
    def save_blocklist_domain(self, data):
        try:
            with open(self.blocklist_domain_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"Error saving domain blocklist: {e}")
            return False


config_manager = ConfigManager() 