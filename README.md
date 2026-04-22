# Audio Converter

Desktop application built with Python and PySide6 to batch-convert audio files with per-file format selection.

This tool converts each input file independently. It does not merge tracks.

## Features

- Clean desktop UI with drag-and-drop support.
- Per-row output format in the same queue.
- Selective format apply using row checkboxes.
- Editable output name per file.
- Supported formats: MP3, M4A, AAC, WAV, FLAC, OGG, OPUS, ALAC, WMA, AIFF.
- FFmpeg-based conversion suitable for large/long files.
- Per-file progress and cancellation support.
- Metadata preservation enabled by default.
- User-selected output folder.
- Optional auto-open output folder after conversion.
- Optional format suffix in output file names (for example, `songmp3.mp3` vs `song.mp3`).
- Resizable table columns with horizontal scrolling when needed.
- Built-in settings dialog with English/Spanish language and color customization.
- Persistent preferences across sessions.

## Requirements

- Python 3.10+
- FFmpeg and FFprobe available in PATH

To verify FFmpeg availability:

```bash
ffmpeg -version
ffprobe -version
```

If commands are not found, install FFmpeg and add its `bin` directory to your system PATH.

### Install FFmpeg

Use one of the following options depending on your OS.

#### Windows

Option 1 (recommended, with winget):

```powershell
winget install --id Gyan.FFmpeg --source winget
```

Option 2 (with Chocolatey):

```powershell
choco install ffmpeg
```

Option 3 (manual):

1. Download a build from https://www.gyan.dev/ffmpeg/builds/ (Essentials build is enough).
2. Extract it, for example to `C:\ffmpeg`.
3. Add `C:\ffmpeg\bin` (or your extracted `bin` folder) to system PATH.
4. Close and reopen your terminal.

#### macOS

With Homebrew:

```bash
brew install ffmpeg
```

#### Linux

Ubuntu / Debian:

```bash
sudo apt update
sudo apt install ffmpeg
```

Tested on Ubuntu 24.04, the command above is the expected/default path.
If `apt` cannot find `ffmpeg`, enable the `universe` repository and retry:

```bash
sudo add-apt-repository universe
sudo apt update
sudo apt install ffmpeg
```

Fedora:

```bash
sudo dnf install ffmpeg
```

Arch Linux:

```bash
sudo pacman -S ffmpeg
```

After installation, verify again:

```bash
ffmpeg -version
ffprobe -version
```

## Setup

1. Clone or download this repository.
2. Create and activate a virtual environment.
3. Install dependencies.

### Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Ubuntu 24.04, you may need to install the matching `venv` package first before creating the environment:

```bash
sudo apt install python3.12-venv
```

If your system is using another version instead, install the matching package for that version:

```bash
sudo apt install python3.11-venv
```

## Run

```bash
python main.py
```

On Windows you can also use:

```bat
run.bat
```

## Optional package install

If you want to install the app as a local package and use the command entry point:

```bash
pip install .
audio-converter
```

## Usage

1. Add one or more files (or a full folder).
2. Optionally check specific rows in the first column.
3. Set a format per row, or use `Default format` + `Apply format`.
4. Edit output names if needed.
5. Configure bitrate, sample rate, and channels.
6. Choose the output folder.
7. Optionally enable format suffix and auto-open folder.
8. Start conversion.

## Configuration and persistence

- Preferences are automatically stored in `app_settings.json` at project root.
- Saved settings include language, color theme overrides, default format, bitrate, sample rate, channels, suffix toggle, open-on-finish toggle, and output folder.

## Troubleshooting

- Conversion does not start:
	- Verify `ffmpeg` and `ffprobe` are installed and accessible from terminal.
- Output names collide:
	- The app automatically appends numeric suffixes to avoid overwriting files.
- Preferences seem outdated:
	- Close the app normally so settings are written on exit.

## Documentation

See `Doc.md` for the full UI and workflow reference.