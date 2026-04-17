DEFAULT_THEME_COLORS: dict[str, str] = {
    "window": "#08111f",
    "text": "#e8eef7",
    "card": "#0f1a2f",
    "border": "#33527a",
    "muted": "#99a8bf",
    "ok": "#64d2a6",
    "warn": "#ffb454",
    "error": "#ff6b6b",
    "button": "#19304d",
    "button_hover": "#234064",
    "button_press": "#10253d",
    "primary": "#0ab9cc",
    "primary_hover": "#12cade",
    "primary_text": "#041217",
    "input": "#0b1627",
    "alt": "#0d1a2d",
    "header": "#12213a",
    "progress": "#4cc9f0",
    "header_separator": "#5f86ba",
}


def build_theme(custom_colors: dict[str, str] | None = None) -> dict[str, str]:
    theme = DEFAULT_THEME_COLORS.copy()
    if custom_colors:
        for key, value in custom_colors.items():
            if key in theme and isinstance(value, str) and value.startswith("#") and len(value) in {4, 7}:
                theme[key] = value
    return theme


def build_stylesheet(custom_colors: dict[str, str] | None = None) -> str:
    c = build_theme(custom_colors)
    return f"""
QMainWindow {{
    background: {c['window']};
    color: {c['text']};
}}

QWidget {{
    font-family: Segoe UI;
    font-size: 10pt;
    color: {c['text']};
}}

QFrame#HeroCard,
QFrame#PanelCard {{
    background: {c['card']};
    border: 1px solid {c['border']};
    border-radius: 18px;
}}

QLabel#TitleLabel {{
    font-size: 24px;
    font-weight: 700;
    color: {c['text']};
}}

QLabel#SubtitleLabel {{
    color: {c['muted']};
}}

QLabel#EngineStatusLabel[status="ok"] {{
    color: {c['ok']};
    font-weight: 600;
}}

QLabel#EngineStatusLabel[status="warn"] {{
    color: {c['warn']};
    font-weight: 600;
}}

QLabel#EngineStatusLabel[status="error"] {{
    color: {c['error']};
    font-weight: 600;
}}

QPushButton,
QToolButton {{
    background: {c['button']};
    border: 1px solid {c['header_separator']};
    border-radius: 10px;
    padding: 7px 12px;
    font-weight: 600;
}}

QToolButton#SettingsGearButton {{
    font-size: 16px;
    min-width: 34px;
    min-height: 34px;
    border-radius: 17px;
    padding: 0;
}}

QToolButton#MetadataHelpButton {{
    min-width: 20px;
    max-width: 20px;
    min-height: 20px;
    max-height: 20px;
    border-radius: 10px;
    padding: 0;
    font-size: 10px;
}}

QLabel#MetadataHelpLabel {{
    min-width: 20px;
    max-width: 20px;
    min-height: 20px;
    max-height: 20px;
    border-radius: 10px;
    border: 1px solid {c['header_separator']};
    background: {c['button']};
    color: {c['text']};
    qproperty-alignment: AlignCenter;
    font-weight: 700;
}}

QPushButton:hover,
QToolButton:hover {{
    background: {c['button_hover']};
}}

QPushButton:pressed,
QToolButton:pressed {{
    background: {c['button_press']};
}}

QPushButton#PrimaryButton {{
    background: {c['primary']};
    color: {c['primary_text']};
    border: 1px solid {c['primary']};
}}

QPushButton#PrimaryButton:hover {{
    background: {c['primary_hover']};
}}

QPushButton:disabled,
QToolButton:disabled {{
    background: {c['card']};
    color: {c['muted']};
    border-color: {c['border']};
}}

QLineEdit,
QSpinBox,
QComboBox,
QTableWidget,
QPlainTextEdit {{
    background: {c['input']};
    border: 1px solid {c['header_separator']};
    border-radius: 10px;
    padding: 6px 10px;
    selection-background-color: {c['primary']};
}}

QSpinBox,
QComboBox {{
    padding-right: 28px;
}}

QSpinBox::up-button,
QSpinBox::down-button,
QComboBox::drop-down {{
    subcontrol-origin: padding;
    subcontrol-position: top right;
    border-left: 1px solid {c['header_separator']};
    width: 22px;
    margin: 1px;
    background: {c['button']};
}}

QComboBox::drop-down {{
    subcontrol-position: center right;
    border-top-right-radius: 8px;
    border-bottom-right-radius: 8px;
}}

QSpinBox::up-button {{
    subcontrol-position: top right;
    border-top-right-radius: 8px;
}}

QSpinBox::down-button {{
    subcontrol-position: bottom right;
    border-bottom-right-radius: 8px;
    border-top: 1px solid {c['header_separator']};
}}

QSpinBox::up-button:hover,
QSpinBox::down-button:hover,
QComboBox::drop-down:hover {{
    background: {c['button_hover']};
}}

QComboBox::down-arrow {{
    image: none;
    width: 0px;
    height: 0px;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid {c['text']};
}}

QSpinBox::up-arrow {{
    image: none;
    width: 0px;
    height: 0px;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-bottom: 6px solid {c['text']};
}}

QSpinBox::down-arrow {{
    image: none;
    width: 0px;
    height: 0px;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 6px solid {c['text']};
}}

QTableWidget {{
    gridline-color: {c['header_separator']};
    alternate-background-color: {c['alt']};
}}

QHeaderView::section {{
    background: {c['header']};
    color: {c['text']};
    border-top: 1px solid {c['header_separator']};
    border-bottom: 1px solid {c['header_separator']};
    border-right: 1px solid {c['header_separator']};
    padding: 8px;
    font-weight: 600;
}}

QProgressBar {{
    background: {c['window']};
    border: 1px solid {c['border']};
    border-radius: 8px;
    text-align: center;
    color: {c['text']};
}}

QProgressBar::chunk {{
    background: {c['progress']};
    border-radius: 8px;
}}

QGroupBox {{
    border: 1px solid {c['border']};
    border-radius: 14px;
    margin-top: 12px;
    padding-top: 12px;
    font-weight: 600;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
}}
"""