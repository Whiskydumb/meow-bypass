from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QToolButton, QMessageBox
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor

from resources.icons import PLAY_ICON_SVG, PAUSE_ICON_SVG
from utils.resource_utils import svg_to_icon
from utils.translation import translator
from utils.windivert_manager import windivert_manager
from utils.admin_check import is_admin, run_as_admin
from utils.config_manager import config_manager

import sys

class CustomMessageBox(QMessageBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        
    def showEvent(self, event):
        super().showEvent(event)
        if self.parent():
            self.setStyleSheet(self.parent().styleSheet())
        else:
            self.setStyleSheet("""
                QMessageBox {
                    background-color: #121418;
                    color: #dbe0e9;
                }
                QLabel {
                    color: #dbe0e9;
                }
                QPushButton {
                    background-color: #181c23;
                    color: #dbe0e9;
                    border: 1px solid #252a35;
                    border-radius: 4px;
                    padding: 5px 15px;
                    min-width: 60px;
                }
                QPushButton:hover {
                    background-color: #252a35;
                }
            """)

class MainPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.update_button_state()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        self.play_icon = svg_to_icon(PLAY_ICON_SVG, "#121418")
        self.pause_icon = svg_to_icon(PAUSE_ICON_SVG, "#121418")
        
        self.play_btn = QToolButton()
        self.play_btn.setIcon(self.play_icon)
        self.play_btn.setIconSize(QSize(32, 32))
        self.play_btn.setFixedSize(80, 80)
        self.play_btn.setStyleSheet("""
            QToolButton {
                border-radius: 40px;
                background: #8dc1ef;
                color: #121418;
                font-size: 24px;
                font-weight: bold;
            }
            QToolButton:hover {
                background: #78a5cc;
            }
        """)
        
        self.play_label = QLabel(translator.get_translation("play_button"))
        self.play_label.setAlignment(Qt.AlignCenter)
        self.play_label.setStyleSheet("color: #dbe0e9; margin-top: 10px; font-size: 14px;")
        
        layout.addStretch()
        layout.addWidget(self.play_btn, alignment=Qt.AlignCenter)
        layout.addWidget(self.play_label)
        layout.addStretch()
        
    def connect_actions(self, on_play):
        self.play_btn.clicked.connect(self.on_play_btn_clicked)
        self.on_play_callback = on_play
        
    def on_play_btn_clicked(self):
        is_running = config_manager.get_setting("service_running", False)
        
        if is_running:
            success, message = windivert_manager.stop_bypass()
            self.update_button_state()
            self.on_play_callback(success, message, False)
        else:
            if not is_admin():
                msg_box = CustomMessageBox(self)
                msg_box.setWindowTitle(translator.get_translation("admin_required_title"))
                msg_box.setText(translator.get_translation("admin_required_message"))
                msg_box.setIcon(QMessageBox.Question)
                
                yes_button = QPushButton(translator.get_translation("yes_button"))
                no_button = QPushButton(translator.get_translation("no_button"))
                
                yes_button.setStyleSheet("""
                    background-color: #181c23;
                    color: #dbe0e9;
                    border: 1px solid #252a35;
                    border-radius: 4px;
                    padding: 5px 15px;
                    min-width: 60px;
                """)
                no_button.setStyleSheet("""
                    background-color: #181c23;
                    color: #dbe0e9;
                    border: 1px solid #252a35;
                    border-radius: 4px;
                    padding: 5px 15px;
                    min-width: 60px;
                """)
                
                msg_box.addButton(yes_button, QMessageBox.YesRole)
                msg_box.addButton(no_button, QMessageBox.NoRole)
                
                reply = msg_box.exec_()
                
                if reply == 0:
                    run_as_admin(sys.executable, ' '.join(sys.argv))
                    sys.exit(0)
                else:
                    return
            
            method = config_manager.get_setting("method", "Метод 1")
            method_number = method.split()[-1]
            
            success, message = windivert_manager.start_bypass(method_number)
            self.update_button_state()
            self.on_play_callback(success, message, True)
        
    def update_button_state(self):
        is_running = config_manager.get_setting("service_running", False)
        
        if is_running:
            self.play_btn.setIcon(self.pause_icon)
            self.play_label.setText(translator.get_translation("stop_button"))
        else:
            self.play_btn.setIcon(self.play_icon)
            self.play_label.setText(translator.get_translation("play_button"))
        
    def update_translations(self):
        is_running = config_manager.get_setting("service_running", False)
        
        if is_running:
            self.play_label.setText(translator.get_translation("stop_button"))
        else:
            self.play_label.setText(translator.get_translation("play_button")) 