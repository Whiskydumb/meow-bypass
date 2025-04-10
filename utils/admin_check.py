import ctypes
import sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

def run_as_admin(executable_path, parameters=""):
    try:
        if not is_admin():
            ctypes.windll.shell32.ShellExecuteW(
                None, 
                "runas", 
                executable_path,
                parameters, 
                None, 
                1
            )
            return True
        return False
    except Exception as e:
        print(f"Failed to restart as admin: {e}")
        return False 