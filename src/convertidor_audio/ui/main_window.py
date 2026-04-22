from __future__ import annotations

import json
from pathlib import Path

from PySide6.QtCore import QSize, Qt, QUrl, Signal
from PySide6.QtGui import QCloseEvent, QColor, QDesktopServices, QDragEnterEvent, QDropEvent, QIcon
from PySide6.QtWidgets import (
    QAbstractItemView,
    QCheckBox,
    QColorDialog,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFormLayout,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QProgressBar,
    QSpinBox,
    QStatusBar,
    QTableWidget,
    QTableWidgetItem,
    QToolButton,
    QVBoxLayout,
    QWidget,
    QHeaderView,
)

from ..conversion import ConversionJob, ConversionSettings, FFmpegConverter
from ..formats import DEFAULT_FORMAT_KEY, SUPPORTED_AUDIO_EXTENSIONS, available_format_items, estimate_output_size_text, get_profile
from ..workers import ConversionWorker, QueuedConversion
from .style import DEFAULT_THEME_COLORS, build_stylesheet


CONFIG_PATH = Path(__file__).resolve().parents[3] / "app_settings.json"
ICONS_DIR = Path(__file__).resolve().parent / "icons"


TEXTS: dict[str, dict[str, str]] = {
    "es": {
        "window_title": "Convertidor de Audio",
        "hero_title": "Convertidor de Audio",
        "hero_subtitle": "Convierte archivos por lote de forma individual. No une pistas.",
        "controls_add_files": "Agregar archivos",
        "controls_add_folder": "Agregar carpeta",
        "controls_remove": "Quitar seleccionados",
        "controls_clear": "Limpiar cola",
        "controls_default_format": "Formato de conversión",
        "controls_apply_format": "Aplicar formato",
        "settings_tooltip": "Ajustes",
        "group_output": "Ajustes de salida",
        "label_output": "Salida",
        "btn_choose_folder": "Elegir carpeta",
        "label_bitrate": "Bitrate",
        "label_sample_rate": "Frecuencia",
        "label_channels": "Canales",
        "channels_auto": "Auto",
        "channels_mono": "Mono",
        "channels_stereo": "Estereo",
        "group_queue": "Cola de conversion",
        "rename_tip": "Tip: doble clic en Nombre de salida para renombrar.",
        "btn_start": "Iniciar conversion",
        "btn_cancel": "Cancelar",
        "check_open_on_finish": "Abrir carpeta al finalizar",
        "check_suffix": "Agregar formato al nombre",
        "table_select": "",
        "table_file": "Archivo",
        "table_format": "Formato",
        "table_duration": "Duracion",
        "table_size": "Tamano estimado",
        "table_output_name": "Nombre de salida",
        "table_status": "Estado",
        "table_progress": "Progreso",
        "status_added": "Se agregaron {count} archivo(s).",
        "status_converting": "Convirtiendo archivos...",
        "status_cancelling": "Cancelando conversion...",
        "status_cancelled": "Conversion cancelada.",
        "status_finished": "Conversion finalizada.",
        "state_waiting": "En espera",
        "state_queued": "En cola",
        "state_processing": "Procesando",
        "state_done": "Listo",
        "state_error": "Error",
        "dialog_no_files_title": "Sin archivos",
        "dialog_no_files_msg": "Agrega uno o mas archivos antes de convertir.",
        "dialog_invalid_output_title": "Salida invalida",
        "dialog_invalid_output_msg": "Selecciona una carpeta de salida valida.",
        "dialog_ffmpeg_title": "FFmpeg no disponible",
        "dialog_no_jobs_title": "Sin trabajos",
        "dialog_no_jobs_msg": "No se pudieron preparar trabajos de conversion.",
        "dialog_running_title": "Proceso en curso",
        "dialog_running_msg": "Cancela la conversion antes de limpiar la cola.",
        "dialog_folder_empty_title": "Sin archivos",
        "dialog_folder_empty_msg": "No se encontraron audios compatibles en esa carpeta.",
        "file_dialog_select_audio": "Seleccionar audios",
        "file_dialog_select_folder": "Seleccionar carpeta con audios",
        "file_dialog_select_output": "Seleccionar carpeta de salida",
        "settings_title": "Ajustes",
        "settings_language": "Idioma",
        "settings_color_window": "Fondo ventana",
        "settings_color_card": "Paneles",
        "settings_color_text": "Texto",
        "settings_color_border": "Bordes",
        "settings_color_button": "Botones",
        "settings_color_primary": "Boton principal",
        "settings_color_input": "Campos de entrada",
        "settings_color_dropdown": "Desplegables",
        "settings_color_table": "Fondo de tabla",
        "settings_color_table_alt": "Filas alternas",
        "settings_color_header": "Cabecera tabla",
        "settings_color_check": "Checks",
        "settings_color_progress": "Barra de progreso",
        "settings_accept": "Aceptar",
        "settings_cancel": "Cancelar",
        "settings_reset": "Restablecer colores",
        "language_es": "Español",
        "language_en": "English",
    },
    "en": {
        "window_title": "Audio Converter",
        "hero_title": "Audio Converter",
        "hero_subtitle": "Batch-convert files individually. No track merging.",
        "controls_add_files": "Add files",
        "controls_add_folder": "Add folder",
        "controls_remove": "Remove selected",
        "controls_clear": "Clear queue",
        "controls_default_format": "Default format",
        "controls_apply_format": "Apply format",
        "settings_tooltip": "Settings",
        "group_output": "Output settings",
        "label_output": "Output",
        "btn_choose_folder": "Choose folder",
        "label_bitrate": "Bitrate",
        "label_sample_rate": "Sample rate",
        "label_channels": "Channels",
        "channels_auto": "Auto",
        "channels_mono": "Mono",
        "channels_stereo": "Stereo",
        "group_queue": "Conversion queue",
        "rename_tip": "Tip: double click Output name to rename.",
        "btn_start": "Start conversion",
        "btn_cancel": "Cancel",
        "check_open_on_finish": "Open folder when done",
        "check_suffix": "Append format to name",
        "table_select": "",
        "table_file": "File",
        "table_format": "Format",
        "table_duration": "Duration",
        "table_size": "Estimated size",
        "table_output_name": "Output name",
        "table_status": "Status",
        "table_progress": "Progress",
        "status_added": "Added {count} file(s).",
        "status_converting": "Converting files...",
        "status_cancelling": "Cancelling conversion...",
        "status_cancelled": "Conversion canceled.",
        "status_finished": "Conversion finished.",
        "state_waiting": "Waiting",
        "state_queued": "Queued",
        "state_processing": "Processing",
        "state_done": "Done",
        "state_error": "Error",
        "dialog_no_files_title": "No files",
        "dialog_no_files_msg": "Add one or more files before converting.",
        "dialog_invalid_output_title": "Invalid output",
        "dialog_invalid_output_msg": "Select a valid output folder.",
        "dialog_ffmpeg_title": "FFmpeg unavailable",
        "dialog_no_jobs_title": "No jobs",
        "dialog_no_jobs_msg": "Could not prepare conversion jobs.",
        "dialog_running_title": "Process running",
        "dialog_running_msg": "Cancel conversion before clearing the queue.",
        "dialog_folder_empty_title": "No files",
        "dialog_folder_empty_msg": "No supported audio files found in that folder.",
        "file_dialog_select_audio": "Select audio files",
        "file_dialog_select_folder": "Select folder with audio files",
        "file_dialog_select_output": "Select output folder",
        "settings_title": "Settings",
        "settings_language": "Language",
        "settings_color_window": "Window background",
        "settings_color_card": "Panels",
        "settings_color_text": "Text",
        "settings_color_border": "Borders",
        "settings_color_button": "Buttons",
        "settings_color_primary": "Primary button",
        "settings_color_input": "Input fields",
        "settings_color_dropdown": "Dropdowns",
        "settings_color_table": "Table background",
        "settings_color_table_alt": "Alternate rows",
        "settings_color_header": "Table header",
        "settings_color_check": "Checks",
        "settings_color_progress": "Progress bar",
        "settings_accept": "OK",
        "settings_cancel": "Cancel",
        "settings_reset": "Reset colors",
        "language_es": "Spanish",
        "language_en": "English",
    },
}


class SettingsDialog(QDialog):
    def __init__(self, language_key: str, custom_colors: dict[str, str], parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._language_key = language_key
        self._custom_colors = custom_colors.copy()
        self.language_combo = QComboBox(self)
        self.color_buttons: dict[str, QPushButton] = {}
        self._build_ui()

    def _t(self, key: str) -> str:
        return TEXTS.get(self._language_key, TEXTS["en"]).get(key, key)

    def _build_ui(self) -> None:
        self.setModal(True)
        self.setMinimumWidth(420)
        form = QFormLayout(self)

        self.language_combo.addItem(self._t("language_es"), "es")
        self.language_combo.addItem(self._t("language_en"), "en")
        self.language_combo.setCurrentIndex(self.language_combo.findData(self._language_key))
        form.addRow(self._t("settings_language"), self.language_combo)

        color_map = [
            ("window", self._t("settings_color_window")),
            ("card", self._t("settings_color_card")),
            ("text", self._t("settings_color_text")),
            ("border", self._t("settings_color_border")),
            ("button", self._t("settings_color_button")),
            ("primary", self._t("settings_color_primary")),
            ("input", self._t("settings_color_input")),
            ("dropdown", self._t("settings_color_dropdown")),
            ("table", self._t("settings_color_table")),
            ("table_alt", self._t("settings_color_table_alt")),
            ("header", self._t("settings_color_header")),
            ("check", self._t("settings_color_check")),
            ("progress", self._t("settings_color_progress")),
        ]

        for key, label in color_map:
            btn = QPushButton(self._custom_colors.get(key, DEFAULT_THEME_COLORS[key]))
            btn.clicked.connect(lambda _=False, color_key=key: self._pick_color(color_key))
            self.color_buttons[key] = btn
            self._apply_button_color(key)
            form.addRow(label, btn)

        reset_btn = QPushButton(self._t("settings_reset"))
        reset_btn.clicked.connect(self._reset_colors)
        form.addRow("", reset_btn)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, parent=self)
        ok_button = buttons.button(QDialogButtonBox.Ok)
        cancel_button = buttons.button(QDialogButtonBox.Cancel)
        if ok_button is not None:
            ok_button.setText(self._t("settings_accept"))
        if cancel_button is not None:
            cancel_button.setText(self._t("settings_cancel"))
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        form.addWidget(buttons)

    def _pick_color(self, key: str) -> None:
        current = QColor(self._custom_colors.get(key, DEFAULT_THEME_COLORS[key]))
        chosen = QColorDialog.getColor(current, self)
        if not chosen.isValid():
            return
        self._custom_colors[key] = chosen.name()
        self._apply_button_color(key)

    def _apply_button_color(self, key: str) -> None:
        color = self._custom_colors.get(key, DEFAULT_THEME_COLORS[key])
        btn = self.color_buttons[key]
        btn.setText(color)
        btn.setStyleSheet(f"background:{color}; color:#ffffff; border:1px solid #000000;")

    def _reset_colors(self) -> None:
        self._custom_colors = {}
        for key in self.color_buttons:
            self._apply_button_color(key)

    def selections(self) -> tuple[str, dict[str, str]]:
        language = str(self.language_combo.currentData())
        return language, self._custom_colors


class AudioTableWidget(QTableWidget):
    files_dropped = Signal(list)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(0, 8, parent)
        self.setAcceptDrops(True)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.setSelectionMode(QTableWidget.ExtendedSelection)
        self.setAlternatingRowColors(True)
        self.setHorizontalHeaderLabels(["", "File", "Format", "Duration", "Estimated size", "Output name", "Status", "Progress"])
        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Interactive)
        header.setStretchLastSection(True)
        header.setMinimumSectionSize(24)
        self.setColumnWidth(0, 24)
        self.setColumnWidth(1, 195)
        self.setColumnWidth(2, 100)
        self.setColumnWidth(3, 84)
        self.setColumnWidth(4, 125)
        self.setColumnWidth(5, 270)
        self.setColumnWidth(6, 88)
        self.setColumnWidth(7, 108)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.verticalHeader().setVisible(False)
        self.setShowGrid(True)

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)

    def dropEvent(self, event: QDropEvent) -> None:
        paths: list[str] = []
        for url in event.mimeData().urls():
            local_path = url.toLocalFile()
            if local_path:
                paths.append(local_path)
        if paths:
            self.files_dropped.emit(paths)
            event.acceptProposedAction()
        else:
            super().dropEvent(event)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.current_language = "en"
        self.custom_colors: dict[str, str] = {}
        self._updating_table = False

        self.converter = FFmpegConverter()
        self.worker: ConversionWorker | None = None
        preferred_music_dir = Path.home() / "Music"
        self.output_directory = preferred_music_dir if preferred_music_dir.exists() else Path.home()
        self.output_directory.mkdir(parents=True, exist_ok=True)

        self._build_ui()
        self._load_preferences()
        self._connect_signals()
        self._apply_theme()
        self._apply_ui_texts()
        self._refresh_engine_status()
        self._refresh_output_previews()

    def _t(self, key: str) -> str:
        return TEXTS.get(self.current_language, TEXTS["en"]).get(key, key)

    def _apply_theme(self) -> None:
        self.setStyleSheet(build_stylesheet(self.custom_colors))

    def _table_headers(self) -> list[str]:
        return [
            self._t("table_select"),
            self._t("table_file"),
            self._t("table_format"),
            self._t("table_duration"),
            self._t("table_size"),
            self._t("table_output_name"),
            self._t("table_status"),
            self._t("table_progress"),
        ]

    def _apply_ui_texts(self) -> None:
        self.setWindowTitle(self._t("window_title"))
        self.title_label.setText(self._t("hero_title"))
        self.subtitle_label.setText(self._t("hero_subtitle"))
        self.settings_gear_button.setToolTip(self._t("settings_tooltip"))

        self.add_files_button.setText(self._t("controls_add_files"))
        self.add_folder_button.setText(self._t("controls_add_folder"))
        self.remove_button.setText(self._t("controls_remove"))
        self.clear_button.setText(self._t("controls_clear"))
        self.default_format_label.setText(self._t("controls_default_format"))
        self.apply_format_button.setText(self._t("controls_apply_format"))

        self.settings_group.setTitle(self._t("group_output"))
        self.output_label.setText(self._t("label_output"))
        self.browse_output_button.setToolTip(self._t("btn_choose_folder"))
        self.bitrate_label.setText(self._t("label_bitrate"))
        self.sample_rate_label.setText(self._t("label_sample_rate"))
        self.channels_label.setText(self._t("label_channels"))

        self.queue_group.setTitle(self._t("group_queue"))
        self.rename_hint_label.setText(self._t("rename_tip"))

        self.start_button.setText(self._t("btn_start"))
        self.cancel_button.setText(self._t("btn_cancel"))
        self.open_explorer_on_finish_check.setText(self._t("check_open_on_finish"))
        self.include_format_suffix_check.setText(self._t("check_suffix"))

        self.table.setHorizontalHeaderLabels(self._table_headers())
        self._refresh_status_texts()
        self._refresh_channel_labels()
        self._refresh_output_previews()

    def _load_preferences(self) -> None:
        defaults = {
            "language": "en",
            "custom_colors": {},
            "default_format": DEFAULT_FORMAT_KEY,
            "open_on_finish": False,
            "include_format_suffix": True,
            "bitrate": 192,
            "sample_rate": 44100,
            "channels": 2,
            "output_directory": str(self.output_directory),
        }

        data = defaults.copy()
        loaded_data: dict[str, object] = {}
        if CONFIG_PATH.exists():
            try:
                loaded = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
                if isinstance(loaded, dict):
                    loaded_data = loaded
                    data.update(loaded)
            except (json.JSONDecodeError, OSError):
                pass

        self.current_language = data.get("language", "en") if data.get("language") in TEXTS else "en"
        self.custom_colors = data.get("custom_colors", {}) if isinstance(data.get("custom_colors"), dict) else {}

        self.default_format_combo.setCurrentIndex(self.default_format_combo.findData(data.get("default_format", DEFAULT_FORMAT_KEY)))
        self.open_explorer_on_finish_check.setChecked(bool(data.get("open_on_finish", False)))
        self.include_format_suffix_check.setChecked(bool(data.get("include_format_suffix", True)))

        bitrate = int(data.get("bitrate", 192))
        self.bitrate_spin.setValue(max(32, min(512, bitrate)))

        sample = data.get("sample_rate", 44100)
        sample_idx = self.sample_rate_combo.findData(sample)
        if sample_idx >= 0:
            self.sample_rate_combo.setCurrentIndex(sample_idx)

        channels = data.get("channels", 2)
        channels_idx = self.channels_combo.findData(channels)
        if channels_idx >= 0:
            self.channels_combo.setCurrentIndex(channels_idx)

        saved_output = loaded_data.get("output_directory")
        if isinstance(saved_output, str) and saved_output.strip():
            output_dir = Path(saved_output)
        else:
            output_dir = Path(str(defaults["output_directory"]))

        legacy_output_dir = Path.cwd() / "output"
        if output_dir == legacy_output_dir or not output_dir.exists() or not output_dir.is_dir():
            output_dir = Path(str(defaults["output_directory"]))

        self.output_directory = output_dir
        self.output_path_edit.setText(str(self.output_directory))

    def _save_preferences(self) -> None:
        payload = {
            "language": self.current_language,
            "custom_colors": self.custom_colors,
            "default_format": self.default_format_combo.currentData(),
            "open_on_finish": self.open_explorer_on_finish_check.isChecked(),
            "include_format_suffix": self.include_format_suffix_check.isChecked(),
            "bitrate": int(self.bitrate_spin.value()),
            "sample_rate": self.sample_rate_combo.currentData(),
            "channels": self.channels_combo.currentData(),
            "output_directory": str(self.output_directory),
        }
        try:
            CONFIG_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=True), encoding="utf-8")
        except OSError:
            pass

    def closeEvent(self, event: QCloseEvent) -> None:
        self._save_preferences()
        super().closeEvent(event)

    def _build_ui(self) -> None:
        self.resize(1120, 720)
        self.setMinimumSize(QSize(1080, 720))
        self.setAcceptDrops(True)

        root = QWidget(self)
        self.setCentralWidget(root)
        main_layout = QVBoxLayout(root)
        main_layout.setContentsMargins(18, 18, 18, 18)
        main_layout.setSpacing(14)

        hero = QFrame()
        hero.setObjectName("HeroCard")
        hero_layout = QVBoxLayout(hero)
        hero_layout.setContentsMargins(18, 16, 18, 16)
        hero_layout.setSpacing(8)

        hero_top = QHBoxLayout()
        self.title_label = QLabel()
        self.title_label.setObjectName("TitleLabel")
        self.settings_gear_button = QToolButton()
        self.settings_gear_button.setObjectName("SettingsGearButton")
        self.settings_gear_button.setText("⚙")
        hero_top.addWidget(self.title_label)
        hero_top.addStretch(1)
        hero_top.addWidget(self.settings_gear_button)

        self.subtitle_label = QLabel()
        self.subtitle_label.setObjectName("SubtitleLabel")
        self.subtitle_label.setWordWrap(True)

        hero_layout.addLayout(hero_top)
        hero_layout.addWidget(self.subtitle_label)
        main_layout.addWidget(hero)

        top_panel = QFrame()
        top_panel.setObjectName("PanelCard")
        top_layout = QVBoxLayout(top_panel)
        top_layout.setContentsMargins(16, 16, 16, 16)
        top_layout.setSpacing(12)

        controls_row = QHBoxLayout()
        controls_row.setSpacing(10)

        self.add_files_button = QPushButton()
        self.add_folder_button = QPushButton()
        self.remove_button = QPushButton()
        self.clear_button = QPushButton()

        self.default_format_label = QLabel()
        self.default_format_combo = QComboBox()
        for label, key in available_format_items():
            self.default_format_combo.addItem(label, key)

        self.apply_format_button = QPushButton()

        controls_row.addWidget(self.add_files_button)
        controls_row.addWidget(self.add_folder_button)
        controls_row.addWidget(self.remove_button)
        controls_row.addWidget(self.clear_button)
        controls_row.addStretch(1)
        controls_row.addWidget(self.default_format_label)
        controls_row.addWidget(self.default_format_combo)
        controls_row.addWidget(self.apply_format_button)
        top_layout.addLayout(controls_row)

        self.settings_group = QGroupBox()
        settings_layout = QGridLayout(self.settings_group)
        settings_layout.setContentsMargins(20, 18, 20, 18)
        settings_layout.setHorizontalSpacing(14)
        settings_layout.setVerticalSpacing(10)

        self.output_label = QLabel()
        self.output_path_edit = QLineEdit(str(self.output_directory))
        self.output_path_edit.setReadOnly(True)
        self.browse_output_button = QPushButton()
        self.browse_output_button.setText("")
        self.browse_output_button.setIcon(QIcon(str(ICONS_DIR / "folder_alt.svg")))
        self.browse_output_button.setIconSize(QSize(24, 24))
        self.browse_output_button.setFixedWidth(40)

        self.bitrate_label = QLabel()
        self.bitrate_spin = QSpinBox()
        self.bitrate_spin.setRange(32, 512)
        self.bitrate_spin.setValue(192)
        self.bitrate_spin.setSuffix(" kbps")

        self.sample_rate_label = QLabel()
        self.sample_rate_combo = QComboBox()
        self.sample_rate_combo.addItem("Auto", None)
        for rate in (22050, 44100, 48000, 96000):
            self.sample_rate_combo.addItem(f"{rate} Hz", rate)
        self.sample_rate_combo.setCurrentIndex(2)

        self.channels_label = QLabel()
        self.channels_combo = QComboBox()
        self.channels_combo.addItem(self._t("channels_auto"), None)
        self.channels_combo.addItem(self._t("channels_mono"), 1)
        self.channels_combo.addItem(self._t("channels_stereo"), 2)
        self.channels_combo.setCurrentIndex(2)

        bitrate_wrapper = QWidget(self.settings_group)
        bitrate_layout = QHBoxLayout(bitrate_wrapper)
        bitrate_layout.setContentsMargins(0, 0, 0, 0)
        bitrate_layout.setSpacing(10)
        bitrate_layout.addWidget(self.bitrate_label)
        bitrate_layout.addWidget(self.bitrate_spin)

        sample_rate_wrapper = QWidget(self.settings_group)
        sample_rate_layout = QHBoxLayout(sample_rate_wrapper)
        sample_rate_layout.setContentsMargins(0, 0, 0, 0)
        sample_rate_layout.setSpacing(10)
        sample_rate_layout.addWidget(self.sample_rate_label)
        sample_rate_layout.addWidget(self.sample_rate_combo)

        channels_wrapper = QWidget(self.settings_group)
        channels_layout = QHBoxLayout(channels_wrapper)
        channels_layout.setContentsMargins(0, 0, 0, 0)
        channels_layout.setSpacing(10)
        channels_layout.addWidget(self.channels_label)
        channels_layout.addWidget(self.channels_combo)

        metrics_row = QWidget(self.settings_group)
        metrics_layout = QHBoxLayout(metrics_row)
        metrics_layout.setContentsMargins(10, 0, 10, 0)
        metrics_layout.setSpacing(0)
        metrics_layout.addStretch(1)
        metrics_layout.addWidget(bitrate_wrapper)
        metrics_layout.addStretch(1)
        metrics_layout.addWidget(sample_rate_wrapper)
        metrics_layout.addStretch(1)
        metrics_layout.addWidget(channels_wrapper)
        metrics_layout.addStretch(1)

        self.include_format_suffix_check = QCheckBox()

        settings_layout.addWidget(self.output_label, 0, 0)
        settings_layout.addWidget(self.browse_output_button, 0, 1)
        settings_layout.addWidget(self.output_path_edit, 0, 2, 1, 3)
        settings_layout.addWidget(self.include_format_suffix_check, 0, 5)
        settings_layout.addWidget(metrics_row, 1, 0, 1, 6)

        settings_layout.setColumnStretch(2, 1)
        settings_layout.setColumnStretch(3, 1)
        settings_layout.setColumnStretch(5, 0)

        top_layout.addWidget(self.settings_group)
        main_layout.addWidget(top_panel)

        self.queue_group = QGroupBox()
        queue_layout = QVBoxLayout(self.queue_group)
        queue_layout.setContentsMargins(14, 18, 14, 14)
        queue_layout.setSpacing(10)

        self.rename_hint_label = QLabel()
        self.rename_hint_label.setObjectName("SubtitleLabel")
        self.rename_hint_label.setWordWrap(True)
        queue_layout.addWidget(self.rename_hint_label)

        self.table = AudioTableWidget()
        queue_layout.addWidget(self.table)

        bottom_controls = QHBoxLayout()
        bottom_controls.setSpacing(10)

        self.start_button = QPushButton()
        self.start_button.setObjectName("PrimaryButton")
        self.cancel_button = QPushButton()
        self.cancel_button.setEnabled(False)
        self.open_explorer_on_finish_check = QCheckBox()

        bottom_controls.addStretch(1)
        bottom_controls.addWidget(self.open_explorer_on_finish_check)
        bottom_controls.addWidget(self.cancel_button)
        bottom_controls.addWidget(self.start_button)

        queue_layout.addLayout(bottom_controls)
        main_layout.addWidget(self.queue_group, 1)

        self.status_bar = QStatusBar()
        self.status_bar.setSizeGripEnabled(False)
        self.setStatusBar(self.status_bar)
        self.status_bar.clearMessage()

    def _connect_signals(self) -> None:
        self.add_files_button.clicked.connect(self.add_files)
        self.add_folder_button.clicked.connect(self.add_folder)
        self.remove_button.clicked.connect(self.remove_selected_rows)
        self.clear_button.clicked.connect(self.clear_rows)
        self.browse_output_button.clicked.connect(self.choose_output_directory)
        self.start_button.clicked.connect(self.start_conversion)
        self.cancel_button.clicked.connect(self.cancel_conversion)
        self.apply_format_button.clicked.connect(self.apply_default_format_to_selected)
        self.settings_gear_button.clicked.connect(self._open_settings_dialog)

        self.default_format_combo.currentIndexChanged.connect(self._on_preference_changed)
        self.default_format_combo.currentIndexChanged.connect(self._refresh_output_previews)
        self.table.files_dropped.connect(self.add_files_from_paths)
        self.table.itemChanged.connect(self._on_table_item_changed)
        self.table.horizontalHeader().sectionClicked.connect(self._on_header_section_clicked)

        self.sample_rate_combo.currentIndexChanged.connect(self._on_preference_changed)
        self.sample_rate_combo.currentIndexChanged.connect(self._refresh_output_previews)
        self.channels_combo.currentIndexChanged.connect(self._on_preference_changed)
        self.channels_combo.currentIndexChanged.connect(self._refresh_output_previews)
        self.include_format_suffix_check.stateChanged.connect(self._on_suffix_toggle)
        self.open_explorer_on_finish_check.stateChanged.connect(self._on_preference_changed)
        self.bitrate_spin.valueChanged.connect(self._on_preference_changed)
        self.bitrate_spin.valueChanged.connect(self._refresh_output_previews)

    def _on_header_section_clicked(self, section: int) -> None:
        if section != 0:
            return
        if self.table.rowCount() == 0:
            return
        all_checked = True
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item is None or item.checkState() != Qt.Checked:
                all_checked = False
                break

        target_state = Qt.Unchecked if all_checked else Qt.Checked
        self._updating_table = True
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item is not None:
                item.setCheckState(target_state)
        self._updating_table = False

    def _on_preference_changed(self) -> None:
        self._save_preferences()

    def _open_settings_dialog(self) -> None:
        dialog = SettingsDialog(self.current_language, self.custom_colors, self)
        dialog.setWindowTitle(self._t("settings_title"))
        if dialog.exec() != QDialog.Accepted:
            return
        self.current_language, self.custom_colors = dialog.selections()
        self._apply_theme()
        self._apply_ui_texts()
        self._refresh_output_previews()
        self._save_preferences()

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)

    def dropEvent(self, event: QDropEvent) -> None:
        dropped_paths = [url.toLocalFile() for url in event.mimeData().urls() if url.toLocalFile()]
        if dropped_paths:
            self.add_files_from_paths(dropped_paths)
            event.acceptProposedAction()
        else:
            super().dropEvent(event)

    def _refresh_engine_status(self) -> None:
        available, _ = self.converter.check_available()
        self.start_button.setEnabled(available)

    def add_files(self) -> None:
        files, _ = QFileDialog.getOpenFileNames(
            self,
            self._t("file_dialog_select_audio"),
            str(Path.home()),
            "Audio files (*.wav *.mp3 *.m4a *.aac *.flac *.ogg *.opus *.wma *.aiff *.aif *.caf *.webm *.mp4);;All files (*.*)",
        )
        if files:
            self.add_files_from_paths(files)

    def add_folder(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, self._t("file_dialog_select_folder"), str(Path.home()))
        if not folder:
            return

        folder_path = Path(folder)
        collected: list[str] = []
        for path in folder_path.rglob("*"):
            if path.is_file() and path.suffix.lower() in SUPPORTED_AUDIO_EXTENSIONS:
                collected.append(str(path))

        if collected:
            self.add_files_from_paths(collected)
        else:
            QMessageBox.information(self, self._t("dialog_folder_empty_title"), self._t("dialog_folder_empty_msg"))

    def add_files_from_paths(self, paths: list[str]) -> None:
        existing_paths = {
            self.table.item(row, 1).data(Qt.UserRole)
            for row in range(self.table.rowCount())
            if self.table.item(row, 1)
        }
        added = 0
        default_format = self.default_format_combo.currentData() or DEFAULT_FORMAT_KEY

        for path_text in paths:
            source_path = Path(path_text)
            if not source_path.exists() or not source_path.is_file():
                continue
            if source_path.suffix.lower() not in SUPPORTED_AUDIO_EXTENSIONS:
                continue
            if str(source_path) in existing_paths:
                continue
            self._insert_row(source_path, str(default_format))
            added += 1

        if added:
            self._refresh_output_previews()
            self.status_bar.showMessage(self._t("status_added").format(count=added), 4000)

    def _insert_row(self, source_path: Path, format_key: str) -> None:
        self._updating_table = True
        row = self.table.rowCount()
        self.table.insertRow(row)

        select_item = QTableWidgetItem()
        select_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable | Qt.ItemIsSelectable)
        select_item.setCheckState(Qt.Unchecked)
        self.table.setItem(row, 0, select_item)

        source_item = QTableWidgetItem(source_path.name)
        source_item.setData(Qt.UserRole, str(source_path))
        source_item.setToolTip(str(source_path))
        self.table.setItem(row, 1, source_item)

        format_combo = QComboBox()
        for label, key in available_format_items():
            format_combo.addItem(label, key)
        format_combo.setCurrentIndex(format_combo.findData(format_key))
        format_combo.currentIndexChanged.connect(self._refresh_output_previews)
        self.table.setCellWidget(row, 2, format_combo)

        duration_item = QTableWidgetItem("Calculando...")
        duration_item.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(row, 3, duration_item)

        size_item = QTableWidgetItem("Calculando...")
        size_item.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(row, 4, size_item)

        output_item = QTableWidgetItem(self._default_output_filename(source_path, format_key))
        output_item.setToolTip("Edit this name to customize output" if self.current_language == "en" else "Edita este nombre para personalizar salida")
        output_item.setData(Qt.UserRole, False)
        self.table.setItem(row, 5, output_item)

        status_item = QTableWidgetItem(self._t("state_waiting"))
        status_item.setTextAlignment(Qt.AlignCenter)
        status_item.setData(Qt.UserRole + 1, "state_waiting")
        self.table.setItem(row, 6, status_item)

        progress_bar = QProgressBar()
        progress_bar.setRange(0, 100)
        progress_bar.setValue(0)
        progress_bar.setFormat("%p%")
        self.table.setCellWidget(row, 7, progress_bar)

        duration_seconds = self.converter.probe_duration(source_path)
        duration_item.setText(self._format_duration(duration_seconds))
        duration_item.setData(Qt.UserRole, duration_seconds)
        size_item.setText(self._format_estimated_size(format_key, duration_seconds))
        self._updating_table = False

    def _format_duration(self, duration_seconds: float | None) -> str:
        if duration_seconds is None:
            return "Unknown" if self.current_language == "en" else "Desconocida"
        total_seconds = int(duration_seconds)
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        return f"{minutes:02d}:{seconds:02d}"

    def _format_estimated_size(self, format_key: str, duration_seconds: float | None) -> str:
        sample_rate = self.sample_rate_combo.currentData()
        channels = self.channels_combo.currentData()
        return estimate_output_size_text(
            duration_seconds,
            format_key,
            int(self.bitrate_spin.value()),
            sample_rate if isinstance(sample_rate, int) else None,
            channels if isinstance(channels, int) else None,
            self.current_language,
        )

    def _default_output_filename(self, source_path: Path, format_key: str) -> str:
        profile = get_profile(format_key)
        if self.include_format_suffix_check.isChecked():
            return f"{source_path.stem}{profile.key}.{profile.extension}"
        return f"{source_path.stem}.{profile.extension}"

    def _normalize_output_filename(self, source_path: Path, output_name: str, format_key: str) -> str:
        profile = get_profile(format_key)
        cleaned = Path(output_name.strip()).name
        if not cleaned:
            return self._default_output_filename(source_path, format_key)
        candidate = Path(cleaned)
        if candidate.suffix.lower() != f".{profile.extension}":
            stem = candidate.stem if candidate.stem else source_path.stem
            return f"{stem}.{profile.extension}"
        return cleaned

    def _row_output_full_path(self, row: int, ensure_unique: bool, used_paths: set[Path] | None = None) -> Path | None:
        source_item = self.table.item(row, 1)
        output_item = self.table.item(row, 5)
        format_combo = self.table.cellWidget(row, 2)
        if source_item is None or output_item is None or not isinstance(format_combo, QComboBox):
            return None

        source_path = Path(str(source_item.data(Qt.UserRole)))
        format_key = str(format_combo.currentData())
        output_name = self._normalize_output_filename(source_path, output_item.text(), format_key)
        candidate = self.output_directory / output_name

        if not ensure_unique:
            return candidate

        occupied = used_paths if used_paths is not None else set()
        counter = 1
        unique = candidate
        while unique in occupied or unique.exists():
            unique = candidate.with_name(f"{candidate.stem}_{counter}{candidate.suffix}")
            counter += 1
        return unique

    def _on_table_item_changed(self, item: QTableWidgetItem) -> None:
        if self._updating_table:
            return
        if item.column() != 5:
            return

        row = item.row()
        source_item = self.table.item(row, 1)
        format_combo = self.table.cellWidget(row, 2)
        if source_item is None or not isinstance(format_combo, QComboBox):
            return

        source_path = Path(str(source_item.data(Qt.UserRole)))
        format_key = str(format_combo.currentData())
        normalized = self._normalize_output_filename(source_path, item.text(), format_key)

        self._updating_table = True
        item.setText(normalized)
        item.setData(Qt.UserRole, True)
        self._updating_table = False
        self._refresh_output_previews()

    def _on_suffix_toggle(self) -> None:
        self._save_preferences()
        self._refresh_output_previews()

    def _refresh_output_previews(self) -> None:
        self._updating_table = True
        for row in range(self.table.rowCount()):
            source_item = self.table.item(row, 1)
            format_combo = self.table.cellWidget(row, 2)
            duration_item = self.table.item(row, 3)
            size_item = self.table.item(row, 4)
            output_item = self.table.item(row, 5)
            if source_item is None or output_item is None or duration_item is None or size_item is None or not isinstance(format_combo, QComboBox):
                continue

            source_path = Path(str(source_item.data(Qt.UserRole)))
            format_key = str(format_combo.currentData())

            if not bool(output_item.data(Qt.UserRole)):
                output_item.setText(self._default_output_filename(source_path, format_key))

            output_item.setText(self._normalize_output_filename(source_path, output_item.text(), format_key))
            output_item.setToolTip(str(self.output_directory / output_item.text()))

            duration_seconds = duration_item.data(Qt.UserRole)
            if not isinstance(duration_seconds, (int, float)):
                duration_seconds = self.converter.probe_duration(source_path)
                duration_item.setData(Qt.UserRole, duration_seconds)
            duration_item.setText(self._format_duration(duration_seconds))
            size_item.setText(self._format_estimated_size(format_key, duration_seconds))
        self._updating_table = False

    def _set_status_for_row(self, row: int, status_key: str, tooltip: str | None = None) -> None:
        status_item = self.table.item(row, 6)
        if status_item is None:
            return
        status_item.setData(Qt.UserRole + 1, status_key)
        status_item.setText(self._t(status_key))
        if tooltip is not None:
            status_item.setToolTip(tooltip)

    def _refresh_status_texts(self) -> None:
        for row in range(self.table.rowCount()):
            status_item = self.table.item(row, 6)
            if status_item is None:
                continue
            status_key = status_item.data(Qt.UserRole + 1)
            if isinstance(status_key, str):
                status_item.setText(self._t(status_key))

    def _refresh_channel_labels(self) -> None:
        sample_rate_value = self.sample_rate_combo.currentData()
        channels_value = self.channels_combo.currentData()

        self.sample_rate_combo.blockSignals(True)
        self.sample_rate_combo.setItemText(0, self._t("channels_auto"))
        self.sample_rate_combo.blockSignals(False)

        self.channels_combo.blockSignals(True)
        self.channels_combo.setItemText(0, self._t("channels_auto"))
        self.channels_combo.setItemText(1, self._t("channels_mono"))
        self.channels_combo.setItemText(2, self._t("channels_stereo"))
        self.channels_combo.blockSignals(False)

        sample_idx = self.sample_rate_combo.findData(sample_rate_value)
        if sample_idx >= 0:
            self.sample_rate_combo.setCurrentIndex(sample_idx)

        channels_idx = self.channels_combo.findData(channels_value)
        if channels_idx >= 0:
            self.channels_combo.setCurrentIndex(channels_idx)

    def choose_output_directory(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, self._t("file_dialog_select_output"), str(self.output_directory))
        if not folder:
            return
        self.output_directory = Path(folder)
        self.output_directory.mkdir(parents=True, exist_ok=True)
        self.output_path_edit.setText(str(self.output_directory))
        self._refresh_output_previews()
        self._save_preferences()

    def open_output_folder(self) -> None:
        if self.output_directory.exists():
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(self.output_directory)))

    def remove_selected_rows(self) -> None:
        rows = sorted({index.row() for index in self.table.selectionModel().selectedRows()}, reverse=True)
        for row in rows:
            self.table.removeRow(row)
        self._refresh_output_previews()

    def clear_rows(self) -> None:
        if self.worker and self.worker.isRunning():
            QMessageBox.warning(self, self._t("dialog_running_title"), self._t("dialog_running_msg"))
            return
        self.table.setRowCount(0)

    def apply_default_format_to_selected(self) -> None:
        format_key = str(self.default_format_combo.currentData())
        checked_rows: list[int] = []
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item and item.checkState() == Qt.Checked:
                checked_rows.append(row)

        target_rows = checked_rows
        if not target_rows:
            target_rows = sorted({index.row() for index in self.table.selectionModel().selectedRows()})

        for row in target_rows:
            combo = self.table.cellWidget(row, 2)
            if isinstance(combo, QComboBox):
                combo.setCurrentIndex(combo.findData(format_key))

        self._refresh_output_previews()
        self._save_preferences()

    def _collect_settings(self) -> ConversionSettings:
        sample_rate = self.sample_rate_combo.currentData()
        channels = self.channels_combo.currentData()
        return ConversionSettings(
            bitrate_kbps=int(self.bitrate_spin.value()),
            sample_rate=sample_rate if isinstance(sample_rate, int) else None,
            channels=channels if isinstance(channels, int) else None,
            preserve_metadata=True,
        )

    def _collect_jobs(self) -> list[QueuedConversion]:
        jobs: list[QueuedConversion] = []
        used_paths: set[Path] = set()
        self._updating_table = True
        for row in range(self.table.rowCount()):
            source_item = self.table.item(row, 1)
            format_combo = self.table.cellWidget(row, 2)
            if source_item is None or not isinstance(format_combo, QComboBox):
                continue
            source_path = Path(str(source_item.data(Qt.UserRole)))
            format_key = str(format_combo.currentData())
            output_path = self._row_output_full_path(row, ensure_unique=True, used_paths=used_paths)
            if output_path is None:
                continue
            used_paths.add(output_path)
            output_item = self.table.item(row, 5)
            if output_item:
                output_item.setText(output_path.name)
                output_item.setToolTip(str(output_path))
            jobs.append(QueuedConversion(row=row, job=ConversionJob(source_path=source_path, format_key=format_key, output_path=output_path)))
        self._updating_table = False
        return jobs

    def start_conversion(self) -> None:
        if self.worker and self.worker.isRunning():
            return
        if self.table.rowCount() == 0:
            QMessageBox.information(self, self._t("dialog_no_files_title"), self._t("dialog_no_files_msg"))
            return
        if not self.output_directory.exists():
            QMessageBox.warning(self, self._t("dialog_invalid_output_title"), self._t("dialog_invalid_output_msg"))
            return

        available, message = self.converter.check_available()
        if not available:
            QMessageBox.critical(self, self._t("dialog_ffmpeg_title"), message)
            return

        settings = self._collect_settings()
        jobs = self._collect_jobs()
        if not jobs:
            QMessageBox.information(self, self._t("dialog_no_jobs_title"), self._t("dialog_no_jobs_msg"))
            return

        for row in range(self.table.rowCount()):
            progress_bar = self.table.cellWidget(row, 7)
            self._set_status_for_row(row, "state_queued")
            if isinstance(progress_bar, QProgressBar):
                progress_bar.setValue(0)

        self.worker = ConversionWorker(jobs, settings, self.converter)
        self.worker.row_started.connect(self._on_row_started)
        self.worker.row_progress.connect(self._on_row_progress)
        self.worker.row_finished.connect(self._on_row_finished)
        self.worker.batch_finished.connect(self._on_batch_finished)

        self.add_files_button.setEnabled(False)
        self.add_folder_button.setEnabled(False)
        self.remove_button.setEnabled(False)
        self.clear_button.setEnabled(False)
        self.apply_format_button.setEnabled(False)
        self.default_format_combo.setEnabled(False)
        self.browse_output_button.setEnabled(False)
        self.start_button.setEnabled(False)
        self.cancel_button.setEnabled(True)

        self.status_bar.showMessage(self._t("status_converting"))
        self.worker.start()

    def cancel_conversion(self) -> None:
        if self.worker and self.worker.isRunning():
            self.worker.cancel()
            self.status_bar.showMessage(self._t("status_cancelling"))

    def _on_row_started(self, row: int, output_path: str) -> None:
        self._set_status_for_row(row, "state_processing")
        output_item = self.table.item(row, 5)
        if output_item:
            output_item.setText(Path(output_path).name)
            output_item.setToolTip(output_path)

    def _on_row_progress(self, row: int, progress: int) -> None:
        progress_bar = self.table.cellWidget(row, 7)
        if isinstance(progress_bar, QProgressBar):
            progress_bar.setValue(progress)

    def _on_row_finished(self, row: int, success: bool, message: str) -> None:
        progress_bar = self.table.cellWidget(row, 7)
        self._set_status_for_row(row, "state_done" if success else "state_error", message)
        if isinstance(progress_bar, QProgressBar):
            progress_bar.setValue(100 if success else progress_bar.value())

    def _on_batch_finished(self, cancelled: bool) -> None:
        self.add_files_button.setEnabled(True)
        self.add_folder_button.setEnabled(True)
        self.remove_button.setEnabled(True)
        self.clear_button.setEnabled(True)
        self.apply_format_button.setEnabled(True)
        self.default_format_combo.setEnabled(True)
        self.browse_output_button.setEnabled(True)
        self.start_button.setEnabled(True)
        self.cancel_button.setEnabled(False)
        self._refresh_output_previews()

        if cancelled:
            self.status_bar.showMessage(self._t("status_cancelled"), 5000)
        else:
            self.status_bar.showMessage(self._t("status_finished"), 5000)
            if self.open_explorer_on_finish_check.isChecked():
                self.open_output_folder()

        self._save_preferences()
        self.worker = None
