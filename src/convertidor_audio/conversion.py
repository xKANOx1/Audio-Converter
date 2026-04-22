from __future__ import annotations

import json
import queue
import subprocess
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional

from .formats import FormatProfile, get_profile


ProgressCallback = Callable[[Optional[float]], None]


@dataclass(frozen=True)
class ConversionSettings:
    bitrate_kbps: int
    sample_rate: int | None
    channels: int | None
    preserve_metadata: bool = True


@dataclass(frozen=True)
class ConversionJob:
    source_path: Path
    format_key: str
    output_path: Path


@dataclass(frozen=True)
class ConversionResult:
    success: bool
    message: str
    output_path: Path | None = None


class FFmpegUnavailableError(RuntimeError):
    pass


class FFmpegConverter:
    def __init__(self, ffmpeg_binary: str = "ffmpeg", ffprobe_binary: str = "ffprobe") -> None:
        self.ffmpeg_binary = ffmpeg_binary
        self.ffprobe_binary = ffprobe_binary
        self._current_process: subprocess.Popen[str] | None = None

    def check_available(self) -> tuple[bool, str]:
        for binary in (self.ffmpeg_binary, self.ffprobe_binary):
            try:
                completed = subprocess.run(
                    [binary, "-version"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    check=False,
                )
            except FileNotFoundError:
                return False, f"{binary} was not found in PATH."
            if completed.returncode != 0:
                return False, f"{binary} is not responding correctly."
        return True, "FFmpeg is ready to convert."

    def probe_duration(self, source_path: str | Path) -> float | None:
        try:
            completed = subprocess.run(
                [
                    self.ffprobe_binary,
                    "-v",
                    "error",
                    "-show_entries",
                    "format=duration",
                    "-of",
                    "json",
                    str(source_path),
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
            )
        except FileNotFoundError:
            return None

        if completed.returncode != 0 or not completed.stdout:
            return None

        try:
            payload = json.loads(completed.stdout)
            duration_value = payload.get("format", {}).get("duration")
            if duration_value is None:
                return None
            return float(duration_value)
        except (ValueError, TypeError, json.JSONDecodeError):
            return None

    def build_command(
        self,
        source_path: str | Path,
        output_path: str | Path,
        profile: FormatProfile,
        settings: ConversionSettings,
    ) -> list[str]:
        command = [
            self.ffmpeg_binary,
            "-hide_banner",
            "-nostdin",
            "-y",
            "-i",
            str(source_path),
            "-vn",
        ]

        if settings.preserve_metadata:
            command.extend(["-map_metadata", "0"])
        else:
            command.extend(["-map_metadata", "-1"])

        command.extend(["-c:a", profile.codec])

        if profile.supports_bitrate:
            command.extend(["-b:a", f"{settings.bitrate_kbps}k"])

        if settings.sample_rate is not None:
            command.extend(["-ar", str(settings.sample_rate)])

        if settings.channels is not None:
            command.extend(["-ac", str(settings.channels)])

        if profile.extra_args:
            command.extend(profile.extra_args)

        command.extend([
            "-progress",
            "pipe:1",
            "-nostats",
            "-loglevel",
            "error",
            str(output_path),
        ])
        return command

    def cancel_current(self) -> None:
        if self._current_process and self._current_process.poll() is None:
            self._current_process.kill()

    def convert(
        self,
        job: ConversionJob,
        settings: ConversionSettings,
        progress_callback: ProgressCallback | None = None,
        cancel_event: threading.Event | None = None,
    ) -> ConversionResult:
        profile = get_profile(job.format_key)
        command = self.build_command(job.source_path, job.output_path, profile, settings)

        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
            )
        except FileNotFoundError as exc:
            return ConversionResult(False, f"Could not run FFmpeg: {exc}", None)

        self._current_process = process
        duration = self.probe_duration(job.source_path)
        output_queue: queue.Queue[str | None] = queue.Queue()

        def read_stdout() -> None:
            if process.stdout is None:
                output_queue.put(None)
                return
            for line in process.stdout:
                output_queue.put(line)
            output_queue.put(None)

        reader = threading.Thread(target=read_stdout, daemon=True)
        reader.start()

        finished_reading = False
        last_progress = 0.0

        while True:
            if cancel_event is not None and cancel_event.is_set():
                self.cancel_current()
                return ConversionResult(False, "Conversion canceled by the user.", None)

            try:
                line = output_queue.get(timeout=0.2)
            except queue.Empty:
                if process.poll() is not None and finished_reading:
                    break
                continue

            if line is None:
                finished_reading = True
                if process.poll() is not None:
                    break
                continue

            key, _, value = line.strip().partition("=")
            if key in {"out_time_ms", "out_time_us"} and duration:
                try:
                    current_ms = int(value) / (1000 if key == "out_time_ms" else 1000000)
                    progress = max(0.0, min(1.0, current_ms / duration))
                    if progress_callback and progress - last_progress >= 0.001:
                        progress_callback(progress)
                        last_progress = progress
                except ValueError:
                    continue
            elif key == "progress" and value == "end":
                if progress_callback:
                    progress_callback(1.0)

        process.wait()
        stderr_output = ""
        if process.stderr is not None:
            stderr_output = process.stderr.read().strip()

        self._current_process = None

        if process.returncode == 0:
            if progress_callback:
                progress_callback(1.0)
            return ConversionResult(True, "Conversion completed.", job.output_path)

        message = stderr_output or f"FFmpeg exited with code {process.returncode}."
        return ConversionResult(False, message, None)