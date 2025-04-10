import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFrame, QStackedWidget, QSystemTrayIcon, QMenu, QAction, QApplication
from PyQt5.QtCore import Qt, QPoint, QEvent
from PyQt5.QtGui import QFont

from ui.title_bar import CustomTitleBar
from ui.main_page import MainPage
from ui.settings_page import SettingsPage
from resources.icons import APP_ICON_SVG
from utils.resource_utils import svg_to_icon
from utils.translation import translator

class MainWindow(QWidget):
    def __init__(self, app_font_family):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setFixedSize(250, 250)
        self.setWindowTitle(translator.get_translation("app_title"))
        
        self.app_font = QFont(app_font_family)
        self.app_font.setPointSize(9)
        self.setFont(self.app_font)
        
        app_icon = svg_to_icon(APP_ICON_SVG, "#8dc1ef")
        self.setWindowIcon(app_icon)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(0)
        
        self.content_container = QFrame(self)
        self.content_container.setFrameShape(QFrame.NoFrame)
        self.content_container.setObjectName("contentContainer")
        content_layout = QVBoxLayout(self.content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        self.title_bar = CustomTitleBar(self)
        content_layout.addWidget(self.title_bar)
        
        self.stacked_widget = QStackedWidget()
        content_layout.addWidget(self.stacked_widget)
        
        main_layout.addWidget(self.content_container)
        
        self.main_page = MainPage()
        self.settings_page = SettingsPage()
        
        self.settings_page.languageChanged.connect(self.on_language_changed)
        
        self.stacked_widget.addWidget(self.main_page)
        self.stacked_widget.addWidget(self.settings_page)

        self.title_bar.home_btn.clicked.connect(self.switch_to_home)
        self.title_bar.settings_btn.clicked.connect(self.switch_to_settings)
        
        self.main_page.connect_actions(self.on_play)
        self.settings_page.connect_actions(self.on_open_folder)
        
        self.create_tray()
        
        self.apply_styles()
        
    def switch_to_home(self):
        self.stacked_widget.setCurrentIndex(0)
        self.title_bar.home_btn.setChecked(True)
        self.title_bar.settings_btn.setChecked(False)
        self.title_bar.home_btn.setIcon(self.title_bar.home_icon_active)
        self.title_bar.settings_btn.setIcon(self.title_bar.settings_icon_normal)

    def switch_to_settings(self):
        self.stacked_widget.setCurrentIndex(1)
        self.title_bar.home_btn.setChecked(False)
        self.title_bar.settings_btn.setChecked(True)
        self.title_bar.home_btn.setIcon(self.title_bar.home_icon_normal)
        self.title_bar.settings_btn.setIcon(self.title_bar.settings_icon_active)
        
    def create_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.windowIcon())
        
        self.tray_menu = QMenu()
        self.tray_menu.setStyleSheet("""
            QMenu {
                background-color: #121418;
                color: #dbe0e9;
                border: 1px solid #181c23;
            }
            QMenu::item {
                padding: 5px 20px 5px 20px;
            }
            QMenu::item:selected {
                background-color: #181c23;
            }
        """)
        
        self.open_action = QAction(translator.get_translation("open_action"), self)
        self.open_action.triggered.connect(self.show_from_tray)
        
        self.settings_action = QAction(translator.get_translation("settings_action"), self)
        self.settings_action.triggered.connect(self.show_settings_from_tray)
        
        self.exit_action = QAction(translator.get_translation("exit_action"), self)
        self.exit_action.triggered.connect(self.close_application)
        
        self.tray_menu.addAction(self.open_action)
        self.tray_menu.addAction(self.settings_action)
        self.tray_menu.addSeparator()
        self.tray_menu.addAction(self.exit_action)
        
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.activated.connect(self.tray_icon_activated)
        self.tray_icon.show()
        
    def tray_icon_activated(self, reason):
        # DoubleClick - двойной клик
        # Trigger - одинарный клик
        # MiddleClick - клик средней кнопкой мыши
        if reason == QSystemTrayIcon.DoubleClick or reason == QSystemTrayIcon.Trigger:
            self.show_from_tray()
    
    def show_from_tray(self):
        self.showNormal()
        self.activateWindow()

    def close_application(self):
        self.tray_icon.hide()
        QApplication.quit()

    def hide_to_tray(self):
        self.hide()
    
    def closeEvent(self, event):
        event.ignore()
        self.hide_to_tray()
        
    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            if self.isMinimized():
                event.ignore()
                self.hide_to_tray()
                return
        super().changeEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            delta = QPoint(event.globalPos() - self.old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()
            
    def apply_styles(self):
        self.setStyleSheet(f"""
            QWidget {{
                color: #dbe0e9;
                font-family: {self.app_font.family()};
            }}
            #contentContainer {{
                background-color: #121418;
                border-radius: 15px;
                border: 1px solid #181c23;
            }}
            #titleBar {{
                background-color: #121418;
                border-top-left-radius: 15px;
                border-top-right-radius: 15px;
            }}
            #settingsPage {{
                background-color: #121418;
                border-bottom-left-radius: 15px;
                border-bottom-right-radius: 15px;
            }}
            QPushButton {{
                border: none;
                background: transparent;
            }}
            QPushButton:hover {{
                background: #181c23;
                border-radius: 4px;
            }}
            #settingsBtn {{
                background: #121418;
                color: #dbe0e9;
                padding: 4px;
                border-radius: 4px;
                border: 1px solid #181c23;
                font-size: 12px;
            }}
            #settingsBtn:hover {{
                background: #181c23;
            }}
            QCheckBox {{ 
                margin: 2px; 
                color: #dbe0e9;
                font-size: 12px;
            }}
            QComboBox {{ 
                margin: 2px; 
                background: #181c23;
                color: #dbe0e9;
                padding: 3px;
                border-radius: 4px;
                min-height: 18px;
                font-size: 12px;
            }}
            #settingsCombo {{
                max-height: 22px;
                font-size: 12px;
            }}
            QComboBox::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 15px;
                border: none;
            }}
            QComboBox QAbstractItemView {{
                background: #181c23;
                color: #dbe0e9;
                selection-background-color: #8dc1ef;
                selection-color: #121418;
            }}
            QLabel {{
                color: #dbe0e9;
            }}
            QStackedWidget {{
                background: #121418;
                border-bottom-left-radius: 15px;
                border-bottom-right-radius: 15px;
            }}
        """)
    
    def on_language_changed(self, language):
        self.setWindowTitle(translator.get_translation("app_title"))

        self.open_action.setText(translator.get_translation("open_action"))
        self.settings_action.setText(translator.get_translation("settings_action"))
        self.exit_action.setText(translator.get_translation("exit_action"))
        
        self.main_page.update_translations()
        
    def on_play(self):
        print("Play button clicked - functionality to be implemented")
        
    def on_open_folder(self):
        print("Open folder button clicked - functionality to be implemented")

    def toggle_window_visibility(self):
        if self.isVisible():
            self.hide_to_tray()
        else:
            self.show_from_tray()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.hide_to_tray()
        else:
            super().keyPressEvent(event)

    def show_settings_from_tray(self):
        self.show_from_tray()
        self.switch_to_settings() 