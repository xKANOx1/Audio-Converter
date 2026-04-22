@echo off
setlocal

where ffmpeg >nul 2>&1
if errorlevel 1 (
	echo [ERROR] ffmpeg was not found in PATH.
	echo Install FFmpeg and reopen the terminal.
	echo Quick install with winget: winget install --id Gyan.FFmpeg --source winget
	exit /b 1
)

where ffprobe >nul 2>&1
if errorlevel 1 (
	echo [ERROR] ffprobe was not found in PATH.
	echo Install FFmpeg and reopen the terminal.
	echo Quick install with winget: winget install --id Gyan.FFmpeg --source winget
	exit /b 1
)

if exist ".venv\Scripts\python.exe" (
	".venv\Scripts\python.exe" main.py
) else (
	python main.py
)

endlocal