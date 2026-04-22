from pathlib import Path


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
    "dropdown": "#19304d",
    "table": "#0b1627",
    "table_alt": "#0d1a2d",
    "header": "#12213a",
    "progress": "#4cc9f0",
    "check": "#2ea8ff",
    "header_separator": "#5f86ba",
}


def _hex_to_rgb(color: str) -> tuple[int, int, int]:
    value = color.lstrip("#")
    if len(value) == 3:
        value = "".join(ch * 2 for ch in value)
    return int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16)


def _clamp(value: int) -> int:
    return max(0, min(255, value))


def _shift(color: str, delta: int) -> str:
    red, green, blue = _hex_to_rgb(color)
    return f"#{_clamp(red + delta):02x}{_clamp(green + delta):02x}{_clamp(blue + delta):02x}"


def build_theme(custom_colors: dict[str, str] | None = None) -> dict[str, str]:
    theme = DEFAULT_THEME_COLORS.copy()
    if custom_colors:
        for key, value in custom_colors.items():
            if key in theme and isinstance(value, str) and value.startswith("#") and len(value) in {4, 7}:
                theme[key] = value

    if not (isinstance(custom_colors, dict) and "button_hover" in custom_colors):
        theme["button_hover"] = _shift(theme["button"], 14)
    if not (isinstance(custom_colors, dict) and "button_press" in custom_colors):
        theme["button_press"] = _shift(theme["button"], -18)

    return theme


def build_stylesheet(custom_colors: dict[str, str] | None = None) -> str:
    c = build_theme(custom_colors)
    icons_dir = (Path(__file__).resolve().parent / "icons").as_posix()
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
QPlainTextEdit {{
    background: {c['input']};
    border: 1px solid {c['header_separator']};
    border-radius: 10px;
    padding: 6px 10px;
    selection-background-color: {c['primary']};
    selection-color: {c['primary_text']};
}}

QSpinBox,
QComboBox {{
    padding-right: 28px;
}}

QSpinBox::up-button,
QSpinBox::down-button,
QComboBox::drop-down {{
    subcontrol-origin: padding;
    border-left: 1px solid {c['header_separator']};
    width: 22px;
    margin: 1px;
    background: {c['dropdown']};
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
    image: url({icons_dir}/triangle_down.svg);
    width: 10px;
    height: 10px;
}}

QSpinBox::up-arrow {{
    image: url({icons_dir}/triangle_up.svg);
    width: 10px;
    height: 10px;
}}

QSpinBox::down-arrow {{
    image: url({icons_dir}/triangle_down.svg);
    width: 10px;
    height: 10px;
}}

QComboBox QAbstractItemView {{
    background: {c['dropdown']};
    color: {c['text']};
    border: 1px solid {c['header_separator']};
    selection-background-color: {c['primary']};
    selection-color: {c['primary_text']};
    outline: none;
}}

QComboBox QAbstractItemView::item:selected {{
    background: {c['primary']};
    color: {c['primary_text']};
}}

QCheckBox::indicator,
QTableWidget::indicator {{
    width: 14px;
    height: 14px;
    border-radius: 2px;
    border: 1px solid {c['header_separator']};
    background: transparent;
}}

QCheckBox::indicator:checked,
QTableWidget::indicator:checked {{
    background: {c['check']};
    border: 1px solid {c['check']};
}}

QTableWidget {{
    background: {c['table']};
    gridline-color: {c['header_separator']};
    alternate-background-color: {c['table_alt']};
    border: 1px solid {c['header_separator']};
    border-radius: 10px;
}}

QTableWidget::viewport {{
    background: {c['table']};
    border-radius: 10px;
}}

QTableCornerButton::section {{
    background: {c['header']};
    border: 1px solid {c['header_separator']};
    border-top-left-radius: 10px;
}}

QTableWidget::item:selected,
QTableWidget::item:selected:active,
QTableWidget::item:selected:!active {{
    background: {c['primary']};
    color: {c['primary_text']};
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
    background: transparent;
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