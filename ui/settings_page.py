from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QComboBox, 
                            QCheckBox, QPushButton, QFrame, QHBoxLayout)
from PyQt5.QtCore import Qt

class SettingsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("settingsPage")
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        
        settings_header = QLabel("Настройки приложения")
        settings_header.setStyleSheet("color: #8dc1ef; font-size: 14px; font-weight: bold; margin-bottom: 5px;")
        layout.addWidget(settings_header)
        
        layout.addWidget(self.create_separator())
        
        method_row = QHBoxLayout()
        method_label = QLabel("Метод:")
        method_label.setStyleSheet("color: #475766; font-weight: bold; font-size: 12px;")
        method_label.setFixedWidth(70)
        self.method_combo = QComboBox()
        self.method_combo.addItems(["Метод 1", "Метод 2"])
        self.method_combo.setObjectName("settingsCombo")
        self.method_combo.setFixedWidth(140)
        method_row.addWidget(method_label)
        method_row.addWidget(self.method_combo)
        method_row.addStretch(1)
        layout.addLayout(method_row)

        branch_row = QHBoxLayout()
        branch_label = QLabel("Версия:")
        branch_label.setStyleSheet("color: #475766; font-weight: bold; font-size: 12px;")
        branch_label.setFixedWidth(70)
        self.branch_combo = QComboBox()
        self.branch_combo.addItems(["Релиз", "Бета"])
        self.branch_combo.setObjectName("settingsCombo")
        self.branch_combo.setFixedWidth(140)
        branch_row.addWidget(branch_label)
        branch_row.addWidget(self.branch_combo)
        branch_row.addStretch(1)
        layout.addLayout(branch_row)
        
        lang_row = QHBoxLayout()
        lang_label = QLabel("Язык:")
        lang_label.setStyleSheet("color: #475766; font-weight: bold; font-size: 12px;")
        lang_label.setFixedWidth(70)
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["Русский", "English"])
        self.lang_combo.setObjectName("settingsCombo")
        self.lang_combo.setFixedWidth(140)
        lang_row.addWidget(lang_label)
        lang_row.addWidget(self.lang_combo)
        lang_row.addStretch(1)
        layout.addLayout(lang_row)
        
        self.open_folder_btn = QPushButton("Открыть папку")
        self.open_folder_btn.setObjectName("settingsBtn")
        self.open_folder_btn.setFixedHeight(25)
        layout.addWidget(self.open_folder_btn)
        
        layout.addStretch()
    
    def create_separator(self):
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: #181c23; margin: 3px 0; max-height: 1px;")
        return separator
    
    def connect_actions(self, on_open_folder):
        self.open_folder_btn.clicked.connect(on_open_folder) 