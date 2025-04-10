import os
import subprocess
import sys
import ctypes
import json
import time
import threading
from pathlib import Path

from utils.config_manager import config_manager
from utils.admin_check import is_admin

class WinDivertManager:
    def __init__(self):
        self.process = None
        self.running = False
        self.config_dir = config_manager.get_config_dir()
        self.bin_path = os.path.join(self.config_dir, "bin")
        self.ensure_bin_path_exists()
        self.bin_files = {
            "winws": os.path.join(self.bin_path, "winws.exe"),
            "quic_initial": os.path.join(self.bin_path, "quic_initial_www_google_com.bin"),
            "tls_clienthello": os.path.join(self.bin_path, "tls_clienthello_www_google_com.bin")
        }
        
    def ensure_bin_path_exists(self):
        if not os.path.exists(self.bin_path):
            os.makedirs(self.bin_path)
            
    def get_domains_by_type(self, type_filter="all"):
        domain_data = config_manager.load_blocklist_domain()
        domains = domain_data.get("domains", [])
        
        if type_filter == "discord":
            return [domain for domain in domains if "discord" in domain.lower()]
        elif type_filter == "general":
            return [domain for domain in domains if "discord" not in domain.lower()]
        else:
            return domains
            
    def get_ips_by_type(self, type_filter="all"):
        ip_data = config_manager.load_blocklist_ip()
        ips = ip_data.get("ips", [])
        
        if type_filter == "discord":
            return [ip for ip in ips if "discord" in ip.lower()]
        elif type_filter == "cloudflare":
            return [ip for ip in ips if "cloudflare" in ip.lower()]
        else:
            return ips
    
    def get_windivert_binary_path(self):
        return self.bin_files["winws"]
    
    def start_bypass(self, method="1"):
        if not is_admin():
            return False, "Administrator privileges required"
            
        if self.running:
            return False, "Service is already running"
            
        try:
            winws_path = self.get_windivert_binary_path()
            
            if not os.path.exists(winws_path):
                return False, "Missing winws.exe in bin directory"
            
            if method == "1":
                return self.start_method_1()
            elif method == "2":
                return self.start_method_2()
            else:
                return False, f"Unknown method: {method}"
                
        except Exception as e:
            return False, f"Error starting bypass: {str(e)}"
    
    def start_method_1(self):
        try:
            winws_path = self.bin_files["winws"]
            quic_initial_path = self.bin_files["quic_initial"]
            
            missing_files = []
            for file_path in [winws_path, quic_initial_path]:
                if not os.path.exists(file_path):
                    missing_files.append(os.path.basename(file_path))
            
            if missing_files:
                return False, f"Missing required files: {', '.join(missing_files)}"
            
            general_domains = self.get_domains_by_type("general")
            discord_ips = self.get_ips_by_type("discord")
            cloudflare_ips = self.get_ips_by_type("cloudflare")
            
            temp_general_domains = os.path.join(self.config_dir, "temp_general_domains.txt")
            temp_discord_ips = os.path.join(self.config_dir, "temp_discord_ips.txt")
            temp_cloudflare_ips = os.path.join(self.config_dir, "temp_cloudflare_ips.txt")
            
            with open(temp_general_domains, 'w', encoding='utf-8') as f:
                f.write("\n".join(general_domains))
            
            with open(temp_discord_ips, 'w', encoding='utf-8') as f:
                f.write("\n".join(discord_ips))
                
            with open(temp_cloudflare_ips, 'w', encoding='utf-8') as f:
                f.write("\n".join(cloudflare_ips))
            
            cmd = [
                winws_path,
                "--wf-tcp=80,443",
                "--wf-udp=443,50000-50100",
                "--filter-udp=443",
                f"--hostlist={temp_general_domains}",
                "--dpi-desync=fake",
                "--dpi-desync-repeats=6",
                f"--dpi-desync-fake-quic={quic_initial_path}",
                "--new",
                "--filter-udp=50000-50100",
                f"--ipset={temp_discord_ips}",
                "--dpi-desync=fake",
                "--dpi-desync-any-protocol",
                "--dpi-desync-cutoff=d3",
                "--dpi-desync-repeats=6",
                "--new",
                "--filter-tcp=80",
                f"--hostlist={temp_general_domains}",
                "--dpi-desync=fake,split2",
                "--dpi-desync-autottl=2",
                "--dpi-desync-fooling=md5sig",
                "--new",
                "--filter-l3=ipv4",
                "--filter-tcp=443",
                "--dpi-desync=syndata",
                "--new",
                "--filter-tcp=80",
                f"--ipset={temp_cloudflare_ips}",
                "--dpi-desync=fake,split2",
                "--dpi-desync-autottl=2",
                "--dpi-desync-fooling=md5sig",
                "--new",
                "--filter-udp=443",
                f"--ipset={temp_cloudflare_ips}",
                "--dpi-desync=fake",
                "--dpi-desync-repeats=6",
                f"--dpi-desync-fake-quic={quic_initial_path}",
                "--new"
            ]
            
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            time.sleep(1)
            if self.process.poll() is not None:
                stderr = self.process.stderr.read().decode('utf-8', errors='ignore')
                return False, f"Failed to start bypass: {stderr}"
            
            self.running = True
            config_manager.update_setting("service_running", True)
            
            monitor_thread = threading.Thread(target=self._monitor_process, daemon=True)
            monitor_thread.start()
            
            return True, "Method 1 (general ALT5) bypass started successfully"
            
        except Exception as e:
            return False, f"Error starting method 1: {str(e)}"
    
    def start_method_2(self):
        try:
            winws_path = self.bin_files["winws"]
            quic_initial_path = self.bin_files["quic_initial"]
            tls_clienthello_path = self.bin_files["tls_clienthello"]
            
            missing_files = []
            for file_path in [winws_path, quic_initial_path, tls_clienthello_path]:
                if not os.path.exists(file_path):
                    missing_files.append(os.path.basename(file_path))
            
            if missing_files:
                return False, f"Missing required files: {', '.join(missing_files)}"
            
            general_domains = self.get_domains_by_type("general")
            discord_ips = self.get_ips_by_type("discord")
            cloudflare_ips = self.get_ips_by_type("cloudflare")
            
            temp_general_domains = os.path.join(self.config_dir, "temp_general_domains.txt")
            temp_discord_ips = os.path.join(self.config_dir, "temp_discord_ips.txt")
            temp_cloudflare_ips = os.path.join(self.config_dir, "temp_cloudflare_ips.txt")
            
            with open(temp_general_domains, 'w', encoding='utf-8') as f:
                f.write("\n".join(general_domains))
            
            with open(temp_discord_ips, 'w', encoding='utf-8') as f:
                f.write("\n".join(discord_ips))
                
            with open(temp_cloudflare_ips, 'w', encoding='utf-8') as f:
                f.write("\n".join(cloudflare_ips))
            
            cmd = [
                winws_path,
                "--wf-tcp=80,443",
                "--wf-udp=443,50000-50100",
                "--filter-udp=443",
                f"--hostlist={temp_general_domains}",
                "--dpi-desync=fake",
                "--dpi-desync-repeats=6",
                f"--dpi-desync-fake-quic={quic_initial_path}",
                "--new",
                "--filter-udp=50000-50100",
                f"--ipset={temp_discord_ips}",
                "--dpi-desync=fake",
                "--dpi-desync-any-protocol",
                "--dpi-desync-cutoff=d3",
                "--dpi-desync-repeats=6",
                "--new",
                "--filter-tcp=80",
                f"--hostlist={temp_general_domains}",
                "--dpi-desync=fake,split2",
                "--dpi-desync-autottl=2",
                "--dpi-desync-fooling=md5sig",
                "--new",
                "--filter-tcp=443",
                f"--hostlist={temp_general_domains}",
                "--dpi-desync=fake",
                "--dpi-desync-repeats=6",
                "--dpi-desync-fooling=md5sig",
                f"--dpi-desync-fake-tls={tls_clienthello_path}",
                "--new",
                "--filter-udp=443",
                f"--ipset={temp_cloudflare_ips}",
                "--dpi-desync=fake",
                "--dpi-desync-repeats=6",
                f"--dpi-desync-fake-quic={quic_initial_path}",
                "--new",
                "--filter-tcp=80",
                f"--ipset={temp_cloudflare_ips}",
                "--dpi-desync=fake,split2",
                "--dpi-desync-autottl=2",
                "--dpi-desync-fooling=md5sig",
                "--new",
                "--filter-tcp=443",
                f"--ipset={temp_cloudflare_ips}",
                "--dpi-desync=fake",
                "--dpi-desync-repeats=6",
                "--dpi-desync-fooling=md5sig",
                f"--dpi-desync-fake-tls={tls_clienthello_path}"
            ]
            
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            time.sleep(1)
            if self.process.poll() is not None:
                stderr = self.process.stderr.read().decode('utf-8', errors='ignore')
                return False, f"Failed to start bypass: {stderr}"
            
            self.running = True
            config_manager.update_setting("service_running", True)
            
            monitor_thread = threading.Thread(target=self._monitor_process, daemon=True)
            monitor_thread.start()
            
            return True, "Method 2 (general МГТС2) bypass started successfully"
            
        except Exception as e:
            return False, f"Error starting method 2: {str(e)}"
    
    def stop_bypass(self):
        if not self.running or self.process is None:
            return False, "Service is not running"
            
        try:
            self.process.terminate()
            timeout = 5
            while self.process.poll() is None and timeout > 0:
                time.sleep(0.5)
                timeout -= 0.5
                
            if self.process.poll() is None:
                self.process.kill()
            
            self.running = False
            self.process = None
            config_manager.update_setting("service_running", False)
            
            temp_files = [
                os.path.join(self.config_dir, "temp_general_domains.txt"),
                os.path.join(self.config_dir, "temp_discord_ips.txt"),
                os.path.join(self.config_dir, "temp_cloudflare_ips.txt")
            ]
            
            for file_path in temp_files:
                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                    except:
                        pass
            
            return True, "Bypass stopped successfully"
            
        except Exception as e:
            return False, f"Error stopping bypass: {str(e)}"
    
    def check_status(self):
        if self.running and self.process and self.process.poll() is None:
            return True, "Service is running"
        else:
            self.running = False
            config_manager.update_setting("service_running", False)
            return False, "Service is not running"
    
    def _monitor_process(self):
        if self.process:
            self.process.wait()
            self.running = False
            config_manager.update_setting("service_running", False)


windivert_manager = WinDivertManager() 