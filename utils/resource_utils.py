import base64
from PyQt5.QtGui import QIcon, QPixmap, QPainter
from PyQt5.QtCore import QByteArray, Qt
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtGui import QFontDatabase
import os

def load_font_from_base64(base64_data, font_family_name):
    try:
        font_data = base64.b64decode(base64_data)
        font_id = QFontDatabase.addApplicationFontFromData(font_data)
        if font_id != -1:
            font_families = QFontDatabase.applicationFontFamilies(font_id)
            if font_families:
                return font_families[0]
        return font_family_name
    except Exception as e:
        print(f"Error loading font: {e}")
        return font_family_name

def svg_to_icon(svg_content, color="#dbe0e9"):
    colored_svg = svg_content.replace('stroke="currentColor"', f'stroke="{color}"')
    
    pixmap = QPixmap(24, 24)
    pixmap.fill(Qt.transparent)
    
    renderer = QSvgRenderer(QByteArray(colored_svg.encode()))
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    
    return QIcon(pixmap)

def save_binary_from_base64(base64_data, file_path):
    try:
        if not base64_data:
            return False
            
        binary_data = base64.b64decode(base64_data)
        
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'wb') as f:
            f.write(binary_data)
        return True
    except Exception as e:
        print(f"Error saving binary file: {e}")
        return False
        
def encode_binary_to_base64(file_path):
    try:
        if not os.path.exists(file_path):
            return ""
            
        with open(file_path, 'rb') as f:
            binary_data = f.read()
        
        return base64.b64encode(binary_data).decode('utf-8')
    except Exception as e:
        print(f"Error encoding binary file: {e}")
        return "" 