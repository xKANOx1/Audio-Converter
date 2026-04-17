from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class FormatProfile:
    key: str
    label: str
    extension: str
    codec: str
    description: str
    supports_bitrate: bool = True
    extra_args: tuple[str, ...] = ()


FORMAT_PROFILES: dict[str, FormatProfile] = {
    "mp3": FormatProfile(
        key="mp3",
        label="MP3",
        extension="mp3",
        codec="libmp3lame",
        description="Highly compatible and lightweight.",
    ),
    "m4a": FormatProfile(
        key="m4a",
        label="M4A (AAC)",
        extension="m4a",
        codec="aac",
        description="Compatible with Apple and modern devices.",
        extra_args=("-movflags", "+faststart"),
    ),
    "aac": FormatProfile(
        key="aac",
        label="AAC",
        extension="aac",
        codec="aac",
        description="Compressed audio in a pure AAC container.",
    ),
    "wav": FormatProfile(
        key="wav",
        label="WAV",
        extension="wav",
        codec="pcm_s16le",
        description="Uncompressed, ideal for editing.",
        supports_bitrate=False,
    ),
    "flac": FormatProfile(
        key="flac",
        label="FLAC",
        extension="flac",
        codec="flac",
        description="Lossless with a good size/quality balance.",
        supports_bitrate=False,
    ),
    "ogg": FormatProfile(
        key="ogg",
        label="OGG Vorbis",
        extension="ogg",
        codec="libvorbis",
        description="Good compression for general use.",
    ),
    "opus": FormatProfile(
        key="opus",
        label="OPUS",
        extension="opus",
        codec="libopus",
        description="Excellent quality at low bitrates.",
    ),
    "alac": FormatProfile(
        key="alac",
        label="ALAC (M4A)",
        extension="m4a",
        codec="alac",
        description="Lossless audio inside an M4A container.",
        supports_bitrate=False,
    ),
    "wma": FormatProfile(
        key="wma",
        label="WMA",
        extension="wma",
        codec="wmav2",
        description="Classic compatibility format on Windows.",
    ),
    "aiff": FormatProfile(
        key="aiff",
        label="AIFF",
        extension="aiff",
        codec="pcm_s16be",
        description="Uncompressed, suitable for professional editing.",
        supports_bitrate=False,
    ),
}


DEFAULT_FORMAT_KEY = "mp3"


def available_format_items() -> list[tuple[str, str]]:
    return [(profile.label, profile.key) for profile in FORMAT_PROFILES.values()]


def get_profile(format_key: str) -> FormatProfile:
    if format_key not in FORMAT_PROFILES:
        return FORMAT_PROFILES[DEFAULT_FORMAT_KEY]
    return FORMAT_PROFILES[format_key]


def format_suffix(format_key: str) -> str:
    return get_profile(format_key).extension


def build_output_path(source_path: str | Path, output_directory: str | Path, format_key: str) -> Path:
    source = Path(source_path)
    output_dir = Path(output_directory)
    profile = get_profile(format_key)
    output_dir.mkdir(parents=True, exist_ok=True)
    base_name = f"{source.stem}_{profile.key}.{profile.extension}"
    candidate = output_dir / base_name
    counter = 1
    while candidate.exists():
        candidate = output_dir / f"{source.stem}_{profile.key}_{counter}.{profile.extension}"
        counter += 1
    return candidate


def estimate_output_size_text(
    duration_seconds: float | None,
    format_key: str,
    bitrate_kbps: int,
    sample_rate: int | None,
    channels: int | None,
) -> str:
    if duration_seconds is None or duration_seconds <= 0:
        return "Unknown"

    profile = get_profile(format_key)

    if profile.supports_bitrate:
        estimated_bytes = duration_seconds * (bitrate_kbps * 1000 / 8)
    else:
        resolved_sample_rate = sample_rate or 44100
        resolved_channels = channels or 2

        if profile.codec in {"pcm_s16le", "pcm_s16be"}:
            estimated_bytes = duration_seconds * resolved_sample_rate * resolved_channels * (16 / 8)
        elif profile.codec == "flac":
            pcm_bytes = duration_seconds * resolved_sample_rate * resolved_channels * (16 / 8)
            estimated_bytes = pcm_bytes * 0.65
        elif profile.codec == "alac":
            pcm_bytes = duration_seconds * resolved_sample_rate * resolved_channels * (16 / 8)
            estimated_bytes = pcm_bytes * 0.7
        else:
            estimated_bytes = duration_seconds * resolved_sample_rate * resolved_channels * (16 / 8) * 0.8

    estimated_megabytes = estimated_bytes / (1024 * 1024)
    return f"Approx. {estimated_megabytes:.2f} MB"


SUPPORTED_AUDIO_EXTENSIONS = {
    ".wav",
    ".mp3",
    ".m4a",
    ".aac",
    ".flac",
    ".ogg",
    ".opus",
    ".wma",
    ".aiff",
    ".aif",
    ".caf",
    ".webm",
    ".mkv",
    ".mp4",
}