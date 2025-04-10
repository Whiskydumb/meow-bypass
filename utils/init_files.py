import os
import logging
from pathlib import Path

from utils.config_manager import config_manager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('init_files')

class BinFilesInitializer:
    def __init__(self):
        self.config_dir = config_manager.get_config_dir()
        self.bin_dir = os.path.join(self.config_dir, "bin")
        
        os.makedirs(self.bin_dir, exist_ok=True)
        
    def check_bin_files(self):
        required_files = [
            "winws.exe",
            "WinDivert.dll",
            "WinDivert64.sys",
            "quic_initial_www_google_com.bin",
            "tls_clienthello_www_google_com.bin"
        ]
        
        files_present = []
        files_missing = []
        
        for filename in required_files:
            file_path = os.path.join(self.bin_dir, filename)
            
            if os.path.exists(file_path):
                files_present.append(filename)
                logger.info(f"Found {filename} in bin directory")
            else:
                files_missing.append(filename)
                logger.warning(f"Required file {filename} not found in bin directory")
                
        return files_present, files_missing
    
    def check_json_files(self):
        json_files = [
            "blocklist-domain.json",
            "blocklist-ip.json"
        ]
        
        files_present = []
        files_missing = []
        
        for filename in json_files:
            file_path = os.path.join(self.config_dir, filename)
            
            if os.path.exists(file_path):
                files_present.append(filename)
                logger.info(f"Found {filename} in config directory")
            else:
                files_missing.append(filename)
                logger.warning(f"JSON file {filename} not found in config directory")
                
        return files_present, files_missing
    
    def initialize(self):
        bin_present, bin_missing = self.check_bin_files()
        json_present, json_missing = self.check_json_files()
        
        status = {
            "success": len(bin_missing) == 0 and len(json_missing) == 0,
            "bin_files": {
                "present": bin_present,
                "missing": bin_missing
            },
            "json_files": {
                "present": json_present,
                "missing": json_missing
            }
        }
        
        return status

bin_initializer = BinFilesInitializer() 