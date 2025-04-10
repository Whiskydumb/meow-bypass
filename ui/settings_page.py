from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QComboBox, 
                            QCheckBox, QPushButton, QFrame, QHBoxLayout)
from PyQt5.QtCore import Qt, pyqtSignal
import os
import subprocess

from utils.translation import translator
from utils.config_manager import config_manager

class SettingsPage(QWidget):
    languageChanged = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("settingsPage")
        self.init_ui()
        self.load_settings_from_config()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        
        self.settings_header = QLabel(translator.get_translation("settings_title"))
        self.settings_header.setStyleSheet("color: #8dc1ef; font-size: 14px; margin-bottom: 5px;")
        layout.addWidget(self.settings_header)
        
        layout.addWidget(self.create_separator())
        
        method_row = QHBoxLayout()
        self.method_label = QLabel(translator.get_translation("method_label"))
        self.method_label.setStyleSheet("color: #475766; font-size: 12px;")
        self.method_label.setFixedWidth(70)
        self.method_combo = QComboBox()
        self.method_combo.addItems([
            translator.get_translation("method_1"), 
            translator.get_translation("method_2")
        ])
        self.method_combo.setObjectName("settingsCombo")
        self.method_combo.setFixedWidth(140)
        self.method_combo.currentTextChanged.connect(self.on_method_changed)
        method_row.addWidget(self.method_label)
        method_row.addWidget(self.method_combo)
        method_row.addStretch(1)
        layout.addLayout(method_row)

        # TODO: Добавить управение версиями и автоапдейты
        # branch_row = QHBoxLayout()
        # self.branch_label = QLabel(translator.get_translation("version_label"))
        # self.branch_label.setStyleSheet("color: #475766; font-size: 12px;")
        # self.branch_label.setFixedWidth(70)
        # self.branch_combo = QComboBox()
        # self.branch_combo.addItems([
        #     translator.get_translation("release_version"), 
        #     translator.get_translation("beta_version")
        # ])
        # self.branch_combo.setObjectName("settingsCombo")
        # self.branch_combo.setFixedWidth(140)
        # branch_row.addWidget(self.branch_label)
        # branch_row.addWidget(self.branch_combo)
        # branch_row.addStretch(1)
        # layout.addLayout(branch_row)
        
        lang_row = QHBoxLayout()
        self.lang_label = QLabel(translator.get_translation("language_label"))
        self.lang_label.setStyleSheet("color: #475766; font-size: 12px;")
        self.lang_label.setFixedWidth(70)
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(translator.get_languages())
        self.lang_combo.setObjectName("settingsCombo")
        self.lang_combo.setFixedWidth(140)
        self.lang_combo.setCurrentText(translator.current_language)
        self.lang_combo.currentTextChanged.connect(self.on_language_changed)
        lang_row.addWidget(self.lang_label)
        lang_row.addWidget(self.lang_combo)
        lang_row.addStretch(1)
        layout.addLayout(lang_row)
        
        self.open_folder_btn = QPushButton(translator.get_translation("open_folder_btn"))
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
    
    def connect_actions(self, on_open_folder=None):
        self.open_folder_btn.clicked.connect(self.open_config_folder)
    
    def load_settings_from_config(self):
        config = config_manager.load_config()
        
        language = config.get("language", translator.RUSSIAN)
        if language in translator.get_languages():
            translator.current_language = language
            self.lang_combo.setCurrentText(language)
        
        method = config.get("method", translator.get_translation("method_1"))
        available_methods = [
            translator.get_translation("method_1"),
            translator.get_translation("method_2")
        ]
        
        if method in available_methods:
            self.method_combo.setCurrentText(method)
    
    def on_language_changed(self, language):
        translator.current_language = language
        self.update_translations()
        self.languageChanged.emit(language)
        
        config_manager.update_setting("language", language)
    
    def on_method_changed(self, method):
        config_manager.update_setting("method", method)
    
    def open_config_folder(self):
        config_dir = config_manager.get_config_dir()
        
        if os.name == 'nt':
            os.startfile(config_dir)
        elif os.name == 'posix':
            subprocess.call(['open' if os.uname().sysname == 'Darwin' else 'xdg-open', config_dir])
    
    def update_translations(self):
        self.settings_header.setText(translator.get_translation("settings_title"))
        self.method_label.setText(translator.get_translation("method_label"))
        # self.branch_label.setText(translator.get_translation("version_label"))
        self.lang_label.setText(translator.get_translation("language_label"))
        self.open_folder_btn.setText(translator.get_translation("open_folder_btn"))
        
        method_index = self.method_combo.currentIndex()
        # branch_index = self.branch_combo.currentIndex()
        
        self.method_combo.clear()
        self.method_combo.addItems([
            translator.get_translation("method_1"), 
            translator.get_translation("method_2")
        ])
        
        # self.branch_combo.clear()
        # self.branch_combo.addItems([
        #     translator.get_translation("release_version"), 
        #     translator.get_translation("beta_version")
        # ])
        
        self.method_combo.setCurrentIndex(method_index)
        # self.branch_combo.setCurrentIndex(branch_index) 