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
    "light_bg": "#f4f6f8",
    "light_panel": "#ffffff",
    "light_card": "#ffffff",
    "light_surface": "#eef3f8",
    "light_border": "#dfe6ee",
    "light_text": "#f4f4f4",
    "dark_text": "#1f2937",
    "muted_text": "#5b6472",
    "soft_muted": "#6b7280",
    "muted": "#d7d7d7",
    "success": "#22c55e",
}

DARK_STYLESHEET = f"""
QMainWindow {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                stop:0 {PNG_COLORS['dark_bg']},
                                stop:0.7 {PNG_COLORS['dark_panel']},
                                stop:1 {PNG_COLORS['dark_bg']});
    color: {PNG_COLORS['light_text']};
}}

QWidget {{
    background-color: transparent;
    color: {PNG_COLORS['light_text']};
}}

QLabel {{
    color: {PNG_COLORS['light_text']};
}}

QPushButton {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 {PNG_COLORS['primary_red']},
                                stop:1 #ff5b52);
    color: {PNG_COLORS['white']};
    border: none;
    border-radius: 12px;
    padding: 11px 18px;
    font-weight: 700;
}}

QPushButton:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 {PNG_COLORS['gold']},
                                stop:1 {PNG_COLORS['primary_red']});
    color: {PNG_COLORS['black']};
}}

QLineEdit, QComboBox, QTextEdit {{
    background-color: rgba(23, 27, 34, 0.85);
    color: {PNG_COLORS['light_text']};
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 12px;
    padding: 10px 14px;
    selection-background-color: {PNG_COLORS['primary_red']};
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
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 18px;
    background-color: rgba(15,17,21,0.86);
}}

QTabBar::tab {{
    background-color: rgba(23, 27, 34, 0.8);
    color: {PNG_COLORS['light_text']};
    border: 1px solid rgba(255,255,255,0.06);
    padding: 12px 22px;
    border-top-left-radius: 12px;
    border-top-right-radius: 12px;
    margin-right: 4px;
    min-width: 120px;
}}

QTabBar::tab:selected {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 {PNG_COLORS['primary_red']},
                                stop:1 #ff5b52);
    color: {PNG_COLORS['white']};
    border-color: rgba(255,255,255,0.12);
}}

QFrame#heroCard {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                stop:0 rgba(206,17,38,0.35),
                                stop:0.5 rgba(17,19,25,0.96),
                                stop:1 rgba(17,19,25,0.98));
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px;
}}

QFrame#featureCard {{
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
}}

QFrame#featureCard QLabel {{
    color: {PNG_COLORS['light_text']};
}}

QStatusBar {{
    background-color: {PNG_COLORS['dark_panel']};
    color: {PNG_COLORS['light_text']};
    border-top: 1px solid {PNG_COLORS['primary_red']};
}}

QTableWidget {{
    background-color: rgba(23, 27, 34, 0.9);
    color: {PNG_COLORS['light_text']};
    gridline-color: {PNG_COLORS['soft_border']};
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
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
