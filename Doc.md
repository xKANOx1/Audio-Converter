# Detailed Documentation - Audio Converter

## 1. Purpose
The application batch-converts audio files individually.
It does not merge tracks.

## 2. Workflow
1. Add files or an entire folder.
2. Review each row in the queue.
3. Optionally mark rows using the checkbox in the first column.
4. Select a format per row, or use `Default format` + `Apply format`.
5. Adjust output name, bitrate, sample rate, and channels.
6. Start conversion.

## 3. UI Elements
- Gear icon in the top panel: opens Settings.
- `Output name` column: editable with double-click.
- `Append format to name` checkbox:
  - Enabled: `example` + `mp3` -> `examplemp3.mp3`
  - Disabled: `example` + `mp3` -> `example.mp3`
- `Open folder when done` checkbox: opens the output directory when conversion finishes.
- Folder icon in Output settings: opens the directory picker.

Checkbox locations:
- `Append format to name`: inside Output settings, to the right of the path field.
- `Open folder when done`: bottom controls row, next to `Start conversion` and `Cancel`.

## 4. Persistent Settings
Settings are stored automatically in `app_settings.json` at project root:
- Language (English/Spanish)
- Custom colors
- Default format
- Bitrate, sample rate, channels
- Suffix and open-folder toggles
- Output directory

By default, the initial output directory points to the user Music folder.

## 5. Custom Colors
In Settings, you can manually customize:
- Window background
- Panel/card background
- Text
- Borders
- Main button
- Progress bar

You can also use `Reset colors` to restore defaults.

## 6. Metadata
The app preserves metadata by default for all conversions.

## 7. Queue and Columns Notes
- Columns are resizable in real time.
- Horizontal scrolling appears automatically when width is not enough.
- Border and separator contrast is improved for readability.
- The checkbox column width is reduced to avoid wasted space.
- Base widths are tuned so the `Progress` column is visible at default window size.
- Clicking the checkbox-column header toggles all row checkboxes.

## 8. Control Styling Notes
- The primary button uses a cyan default color (`#0ab9cc`).
- ComboBox and SpinBox controls show visible arrows and respect rounded borders.
- Control borders and header separators use higher contrast.

## 9. Requirements
- Python 3.10+
- FFmpeg and FFprobe in PATH

## 10. Run
From the project folder:

```bash
python main.py
```

If you installed the package entry point, you can also run:

```bash
audio-converter
```

## 11. Common Issues
- Conversion does not start: verify FFmpeg/FFprobe are in PATH.
- Duplicate output names: the app avoids overwrite by appending numeric suffixes.
- Settings not persisted: close the app normally so final save can complete.
