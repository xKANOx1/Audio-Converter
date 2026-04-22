# Audio Converter

Desktop Python app for batch audio conversion with a visual interface, support for large files, and per-file settings.

This tool converts audio files individually; it does not merge tracks together.

## Features

- Graphical interface with a file list.
- Different output format per file in the same queue.
- Per-row selection column to apply format only to checked files.
- Editable output name per file from the Output name column.
- Support for multiple formats: MP3, M4A, AAC, WAV, FLAC, OGG, OPUS, ALAC, WMA, and AIFF.
- FFmpeg-based conversion, ideal for long or heavy files.
- Per-file progress and process cancellation.
- Metadata preservation enabled by default for all conversions.
- Output folder selection.
- Option to automatically open the output folder when finished.
- Option to add or remove the format in the output name (for example `filemp3.mp3` or `file.mp3`).
- Queue columns can be resized in real time, with horizontal scroll when needed.
- Gear button in the top panel to change language (es/en) and adjust colors manually.
- Preferences persist between sessions (language, colors, default format, and more).
- Default output path points to the user Music folder (for example `C:\Users\<user>\Music`).
- Main button uses a cyan style by default (`#0ab9cc`), while keeping customization through settings.

## Requirements

- Python 3.10 or newer.
- FFmpeg and FFprobe installed and available in PATH.

## Quick Start

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies.
4. Ensure FFmpeg is available.
5. Run the app.

## Create A Virtual Environment

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Ubuntu 24.04 note:

```bash
sudo apt install python3.12-venv
```

If your system uses a different Python minor version, install the matching `python3.x-venv` package.

## Installation

```bash
pip install -r requirements.txt
```

On Windows, if FFmpeg is not in PATH, install it with one of these options:

```powershell
winget install --id Gyan.FFmpeg --source winget
```

or

```powershell
choco install ffmpeg
```

Quick check:

```bash
ffmpeg -version
ffprobe -version
```

## Run

```bash
python main.py
```

You can also use the command installed by the project if you install the package:

```bash
audio-converter
```

On Windows, you can also use:

```bat
run.bat
```

## Usage

1. Add one or more files.
2. Check rows in the first column if you want to apply format only to specific files.
3. If you click the header of that checkbox column, you can check or uncheck all rows.
4. Choose a different format in each row if you want mixed outputs in a single run.
5. You can also use Default format + Apply format to change multiple files at once.
6. Select the output folder with the folder icon, between the Output label and the path.
7. If needed, change the output name in the Output name column.
8. Adjust bitrate, sample rate, and channels if required.
9. Choose whether to add the format to the output name.
10. Optional: enable Open folder when done.
11. Start conversion.
12. Use the top gear for language and manual color settings.

Note: the Add format to name checkbox is in Output settings, to the right of the path block.

## Technical Notes

- Large files are not fully loaded into memory; FFmpeg processes them in streaming mode.
- Output is concentrated in a user-selected folder, and each file name can be customized from the table.
- Preferences are saved in `app_settings.json` at the project root.

## Repository Hygiene

- Local runtime artifacts (virtual environments, logs, output files, and generated metadata) are ignored through `.gitignore`.
- Avoid committing user-specific settings and runtime outputs.

## Development And Contribution

- Contribution guide: `CONTRIBUTING.md`
- Changelog: `CHANGELOG.md`
- CI workflow: `.github/workflows/ci.yml`

The CI workflow validates imports and runs a syntax compilation check.

## License

This project is licensed under the MIT License. See `LICENSE`.