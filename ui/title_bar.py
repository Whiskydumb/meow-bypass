from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QToolButton
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor

from resources.icons import HOME_ICON_SVG, SETTINGS_ICON_SVG, APP_ICON_SVG, MINIMIZE_ICON_SVG
from utils.resource_utils import svg_to_icon

class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setFixedHeight(30)
        
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor("#121418"))
        self.setPalette(p)
        self.setObjectName("titleBar")
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)
        
        self.app_icon = svg_to_icon(APP_ICON_SVG, "#8dc1ef")
        self.logo = QLabel()
        self.logo.setPixmap(self.app_icon.pixmap(16, 16))
        layout.addWidget(self.logo)
        
        self.tab_buttons = QWidget()
        self.tab_buttons.setAutoFillBackground(True)
        p = self.tab_buttons.palette()
        p.setColor(self.tab_buttons.backgroundRole(), QColor("#121418"))
        self.tab_buttons.setPalette(p)
        
        tab_layout = QHBoxLayout(self.tab_buttons)
        tab_layout.setContentsMargins(0, 0, 0, 0)

        self.home_icon_normal = svg_to_icon(HOME_ICON_SVG, "#6b7986")
        self.home_icon_active = svg_to_icon(HOME_ICON_SVG, "#8dc1ef")
        self.settings_icon_normal = svg_to_icon(SETTINGS_ICON_SVG, "#6b7986")
        self.settings_icon_active = svg_to_icon(SETTINGS_ICON_SVG, "#8dc1ef")
        self.minimize_icon = svg_to_icon(MINIMIZE_ICON_SVG, "#6b7986")
        
        self.home_btn = QToolButton()
        self.home_btn.setIcon(self.home_icon_active)
        self.home_btn.setIconSize(QSize(20, 20))
        self.home_btn.setCheckable(True)
        self.home_btn.setChecked(True)
        
        self.settings_btn = QToolButton()
        self.settings_btn.setIcon(self.settings_icon_normal)
        self.settings_btn.setIconSize(QSize(20, 20))
        self.settings_btn.setCheckable(True)
        
        tab_layout.addWidget(self.home_btn)
        tab_layout.addWidget(self.settings_btn)
        layout.addWidget(self.tab_buttons, alignment=Qt.AlignCenter)
        
        self.minimize_btn = QToolButton()
        self.minimize_btn.setIcon(self.minimize_icon)
        self.minimize_btn.setIconSize(QSize(16, 16))
        self.minimize_btn.clicked.connect(self.parent.showMinimized)
        layout.addWidget(self.minimize_btn)
        
        self.apply_styles()
        
    def apply_styles(self):
        self.home_btn.setStyleSheet("""
            QToolButton {
                background-color: transparent;
                border: none;
                padding: 3px;
            }
            QToolButton:hover {
                background-color: #181c23;
                border-radius: 4px;
            }
            QToolButton:checked {
                background-color: transparent;
            }
        """)
        self.settings_btn.setStyleSheet("""
            QToolButton {
                background-color: transparent;
                border: none;
                padding: 3px;
            }
            QToolButton:hover {
                background-color: #181c23;
                border-radius: 4px;
            }
            QToolButton:checked {
                background-color: transparent;
            }
        """)
        self.minimize_btn.setStyleSheet("""
            QToolButton {
                background-color: transparent;
                color: #dbe0e9;
                border: none;
                padding: 3px;
            }
            QToolButton:hover {
                background-color: #181c23;
                border-radius: 4px;
            }
        """) 