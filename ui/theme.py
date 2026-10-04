PNG_COLORS = {
    "primary_red": "#CE1126",
    "gold": "#FCD116",
    "black": "#000000",
    "white": "#FFFFFF",
    "dark_bg": "#0f1115",
    "dark_panel": "#171b22",
    "dark_card": "#202733",
    "surface": "#2b3340",
    "soft_border": "#313b49",
    "light_bg": "#f5f5f5",
    "light_panel": "#ffffff",
    "light_text": "#f4f4f4",
    "dark_text": "#171717",
    "muted": "#d7d7d7",
    "success": "#22c55e",
}

DARK_STYLESHEET = f"""
QMainWindow {{
    background-color: {PNG_COLORS['dark_bg']};
    color: {PNG_COLORS['light_text']};
}}

QWidget {{
    background-color: {PNG_COLORS['dark_bg']};
    color: {PNG_COLORS['light_text']};
}}

QLabel {{
    color: {PNG_COLORS['light_text']};
}}

QPushButton {{
    background-color: {PNG_COLORS['primary_red']};
    color: {PNG_COLORS['white']};
    border: none;
    border-radius: 9px;
    padding: 10px 16px;
    font-weight: 700;
}}

QPushButton:hover {{
    background-color: {PNG_COLORS['gold']};
    color: {PNG_COLORS['black']};
}}

QLineEdit, QComboBox, QTextEdit {{
    background-color: {PNG_COLORS['dark_panel']};
    color: {PNG_COLORS['light_text']};
    border: 1px solid {PNG_COLORS['primary_red']};
    border-radius: 7px;
    padding: 8px 10px;
}}

QGroupBox {{
    border: 1px solid {PNG_COLORS['primary_red']};
    border-radius: 10px;
    margin-top: 12px;
    padding-top: 12px;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    left: 14px;
    color: {PNG_COLORS['gold']};
    font-weight: 700;
}}

QTabWidget::pane {{
    border: 1px solid {PNG_COLORS['primary_red']};
    border-radius: 10px;
    background-color: {PNG_COLORS['dark_bg']};
}}

QTabBar::tab {{
    background-color: {PNG_COLORS['dark_panel']};
    color: {PNG_COLORS['light_text']};
    border: 1px solid {PNG_COLORS['soft_border']};
    padding: 10px 18px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
}}

QTabBar::tab:selected {{
    background-color: {PNG_COLORS['primary_red']};
    color: {PNG_COLORS['white']};
}}

QStatusBar {{
    background-color: {PNG_COLORS['dark_panel']};
    color: {PNG_COLORS['light_text']};
    border-top: 1px solid {PNG_COLORS['primary_red']};
}}

QTableWidget {{
    background-color: {PNG_COLORS['dark_panel']};
    color: {PNG_COLORS['light_text']};
    gridline-color: {PNG_COLORS['soft_border']};
    border: 1px solid {PNG_COLORS['primary_red']};
}}

QHeaderView::section {{
    background-color: {PNG_COLORS['primary_red']};
    color: {PNG_COLORS['white']};
    padding: 8px;
    border: none;
}}

QProgressBar {{
    border: 1px solid {PNG_COLORS['gold']};
    border-radius: 8px;
    background: {PNG_COLORS['dark_panel']};
    color: {PNG_COLORS['light_text']};
}}

QProgressBar::chunk {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                               stop:0 {PNG_COLORS['gold']},
                               stop:1 {PNG_COLORS['primary_red']});
    border-radius: 7px;
}}
"""

LIGHT_STYLESHEET = f"""
QMainWindow {{
    background-color: {PNG_COLORS['light_bg']};
    color: {PNG_COLORS['dark_text']};
}}

QWidget {{
    background-color: {PNG_COLORS['light_bg']};
    color: {PNG_COLORS['dark_text']};
}}

QLabel {{
    color: {PNG_COLORS['dark_text']};
}}

QPushButton {{
    background-color: {PNG_COLORS['primary_red']};
    color: {PNG_COLORS['white']};
    border: none;
    border-radius: 9px;
    padding: 10px 16px;
    font-weight: 700;
}}

QPushButton:hover {{
    background-color: {PNG_COLORS['gold']};
    color: {PNG_COLORS['black']};
}}

QLineEdit, QComboBox, QTextEdit {{
    background-color: {PNG_COLORS['light_panel']};
    color: {PNG_COLORS['dark_text']};
    border: 1px solid {PNG_COLORS['primary_red']};
    border-radius: 7px;
    padding: 8px 10px;
}}

QGroupBox {{
    border: 1px solid {PNG_COLORS['primary_red']};
    border-radius: 10px;
    margin-top: 12px;
    padding-top: 12px;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    left: 14px;
    color: {PNG_COLORS['primary_red']};
    font-weight: 700;
}}

QTabWidget::pane {{
    border: 1px solid {PNG_COLORS['primary_red']};
    border-radius: 10px;
    background-color: {PNG_COLORS['light_bg']};
}}

QTabBar::tab {{
    background-color: {PNG_COLORS['light_panel']};
    color: {PNG_COLORS['dark_text']};
    border: 1px solid {PNG_COLORS['soft_border']};
    padding: 10px 18px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
}}

QTabBar::tab:selected {{
    background-color: {PNG_COLORS['primary_red']};
    color: {PNG_COLORS['white']};
}}

QStatusBar {{
    background-color: {PNG_COLORS['light_panel']};
    color: {PNG_COLORS['dark_text']};
    border-top: 1px solid {PNG_COLORS['primary_red']};
}}

QTableWidget {{
    background-color: {PNG_COLORS['light_panel']};
    color: {PNG_COLORS['dark_text']};
    gridline-color: #d9d9d9;
    border: 1px solid {PNG_COLORS['primary_red']};
}}

QHeaderView::section {{
    background-color: {PNG_COLORS['primary_red']};
    color: {PNG_COLORS['white']};
    padding: 8px;
    border: none;
}}

QProgressBar {{
    border: 1px solid {PNG_COLORS['primary_red']};
    border-radius: 8px;
    background: {PNG_COLORS['light_panel']};
    color: {PNG_COLORS['dark_text']};
}}

QProgressBar::chunk {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                               stop:0 {PNG_COLORS['gold']},
                               stop:1 {PNG_COLORS['primary_red']});
    border-radius: 7px;
}}
"""
