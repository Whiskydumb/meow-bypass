import sys
import os
from PyQt5.QtWidgets import QApplication, QMessageBox

from resources.fonts import JETBRAINS_MONO_BASE64
from utils.resource_utils import load_font_from_base64
from ui.main_window import MainWindow
from utils.init_files import bin_initializer
from utils.admin_check import is_admin, run_as_admin

def check_and_initialize_files(app):
    if not is_admin():
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Требуются права администратора")
        msg_box.setText("Для работы WinDivert требуются права администратора.\nПерезапустить приложение с правами администратора?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.Yes)
        
        if msg_box.exec_() == QMessageBox.Yes:
            run_as_admin(sys.executable, ' '.join(sys.argv))
            sys.exit(0)
        else:
            sys.exit(1)
            
    status = bin_initializer.initialize()
    
    if not status["success"]:
        msg = "Не удалось найти следующие файлы:\n\n"
        
        if status["bin_files"]["missing"]:
            msg += "Бинарные файлы:\n- " + "\n- ".join(status["bin_files"]["missing"]) + "\n\n"
            
        if status["json_files"]["missing"]:
            msg += "JSON файлы:\n- " + "\n- ".join(status["json_files"]["missing"]) + "\n\n"
            
        msg += "Убедитесь, что все файлы находятся в правильных директориях и запустите приложение снова."
        
        error_box = QMessageBox()
        error_box.setWindowTitle("Ошибка инициализации")
        error_box.setText(msg)
        error_box.setIcon(QMessageBox.Warning)
        error_box.exec_()
        
    return status["success"]

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    if not check_and_initialize_files(app):
        sys.exit(1)
    
    app_font_family = load_font_from_base64(JETBRAINS_MONO_BASE64, "JetBrains Mono")
    
    window = MainWindow(app_font_family)
    window.show()
    sys.exit(app.exec_()) 