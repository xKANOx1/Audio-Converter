from __future__ import annotations

import threading
from dataclasses import dataclass

from PySide6.QtCore import QThread, Signal

from .conversion import ConversionJob, ConversionSettings, FFmpegConverter


@dataclass(frozen=True)
class QueuedConversion:
    row: int
    job: ConversionJob


class ConversionWorker(QThread):
    row_started = Signal(int, str)
    row_progress = Signal(int, int)
    row_finished = Signal(int, bool, str)
    batch_finished = Signal(bool)
    log_message = Signal(str)

    def __init__(self, jobs: list[QueuedConversion], settings: ConversionSettings, converter: FFmpegConverter) -> None:
        super().__init__()
        self._jobs = jobs
        self._settings = settings
        self._converter = converter
        self._cancel_event = threading.Event()

    def cancel(self) -> None:
        self._cancel_event.set()
        self._converter.cancel_current()

    def run(self) -> None:
        cancelled = False

        for queued in self._jobs:
            if self._cancel_event.is_set():
                cancelled = True
                break

            self.row_started.emit(queued.row, str(queued.job.output_path))

            def progress_callback(progress: float | None) -> None:
                if progress is None:
                    return
                self.row_progress.emit(queued.row, int(progress * 100))

            result = self._converter.convert(
                queued.job,
                self._settings,
                progress_callback=progress_callback,
                cancel_event=self._cancel_event,
            )

            self.row_finished.emit(queued.row, result.success, result.message)

            if self._cancel_event.is_set() and not result.success:
                cancelled = True
                break

        self.batch_finished.emit(cancelled)