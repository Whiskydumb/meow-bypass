import base64
from PyQt5.QtGui import QIcon, QPixmap, QPainter
from PyQt5.QtCore import QByteArray, Qt
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtGui import QFontDatabase

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