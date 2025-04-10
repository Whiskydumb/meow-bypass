from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QToolButton
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor

from resources.icons import PLAY_ICON_SVG
from utils.resource_utils import svg_to_icon

class MainPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        self.play_icon = svg_to_icon(PLAY_ICON_SVG, "#121418")
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
        
        self.play_label = QLabel("Запустить")
        self.play_label.setAlignment(Qt.AlignCenter)
        self.play_label.setStyleSheet("color: #dbe0e9; margin-top: 10px; font-size: 14px;")
        
        layout.addStretch()
        layout.addWidget(self.play_btn, alignment=Qt.AlignCenter)
        layout.addWidget(self.play_label)
        layout.addStretch()
        
    def connect_actions(self, on_play):
        self.play_btn.clicked.connect(on_play) 