import sys
from PyQt5.QtWidgets import QApplication

from resources.fonts import JETBRAINS_MONO_BASE64
from utils.resource_utils import load_font_from_base64
from ui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    app_font_family = load_font_from_base64(JETBRAINS_MONO_BASE64, "JetBrains Mono")
    
    window = MainWindow(app_font_family)
    window.show()
    sys.exit(app.exec_()) 