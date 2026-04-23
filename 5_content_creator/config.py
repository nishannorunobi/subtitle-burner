"""
Configuration loader for 5_content_creator.

Reads values from `config.properties` and exposes them as module-level constants.
"""

from pathlib import Path
from typing import Dict


CONFIG_FILE = Path(__file__).with_name("config.properties")


def _parse_properties(path: Path) -> Dict[str, str]:
    """Parse a Java-style .properties file into a dictionary."""
    data: Dict[str, str] = {}

    if not path.exists():
        return data

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()

        # Skip empty lines and comments
        if not line or line.startswith("#") or line.startswith("!"):
            continue

        # Support key=value and key:value formats
        if "=" in line:
            key, value = line.split("=", 1)
        elif ":" in line:
            key, value = line.split(":", 1)
        else:
            # Ignore malformed lines
            continue

        data[key.strip()] = value.strip()

    return data


_CONFIG = _parse_properties(CONFIG_FILE)

# Expose all properties as uppercase constants.
# Example: api_key -> API_KEY
for _k, _v in _CONFIG.items():
    globals()[_k.upper()] = _v

# Build constants from:
# - mount.path
# - filelocation.original
# - filename.original
# - extention.original
MOUNT_PATH = _CONFIG.get("mount.path", "")
FILELOCATION_ORIGINAL = _CONFIG.get("filelocation.original", "")
FILENAME_ORIGINAL = _CONFIG.get("filename.original", "")
EXTENTION_ORIGINAL = "."+_CONFIG.get("extention.original", "")

ORIGINAL_FILE_PATH = MOUNT_PATH + FILELOCATION_ORIGINAL + FILENAME_ORIGINAL + EXTENTION_ORIGINAL

FILELOCATION_PROCESSING = _CONFIG.get("filelocation.processing", "")
FILENAME_PROCESSING = _CONFIG.get("filename.processing", "")
EXTENTION_PROCESSING = "."+_CONFIG.get("extention.processing", "")
PROCESSING_FILE_PATH = (
    MOUNT_PATH + FILELOCATION_PROCESSING + FILENAME_PROCESSING + EXTENTION_PROCESSING
)

FILELOCATION_VOCALS = _CONFIG.get("filelocation.vocals", "")
PREFIX_VOCALS = _CONFIG.get("prefix.vocals", "")
EXTENTION_VOCALS = "."+_CONFIG.get("extention.vocals", "")
VOCALS_FILE_PATH = MOUNT_PATH + FILELOCATION_VOCALS + PREFIX_VOCALS + EXTENTION_VOCALS

FILELOCATION_VOCALS_VAD = _CONFIG.get("filelocation.vocals.vad", "")
PREFIX_VOCALS_VAD = _CONFIG.get("prefix.vocals.vad", "")
EXTENTION_VOCALS_VAD = "."+_CONFIG.get("extention.vocals.vad", "")
VOCALS_VAD_FILE_PATH = (
    MOUNT_PATH + FILELOCATION_VOCALS_VAD + PREFIX_VOCALS_VAD + EXTENTION_VOCALS_VAD
)

FILELOCATION_BEFORE_SUB = _CONFIG.get("filelocation.before_sub", "")
PREFIX_BEFORE_SUB = _CONFIG.get("prefix.before_sub", "")
EXTENTION_BEFORE_SUB = "."+_CONFIG.get("extention.before_sub", "")
BEFORE_SUB_FILE_PATH = (
    MOUNT_PATH + FILELOCATION_BEFORE_SUB + PREFIX_BEFORE_SUB + EXTENTION_BEFORE_SUB
)

FILELOCATION_READY4SUB = _CONFIG.get("filelocation.ready4sub", "")
PREFIX_READY4SUB = _CONFIG.get("prefix.ready4sub", "")
EXTENTION_READY4SUB = "."+_CONFIG.get("extention.ready4sub", "")
READY4SUB_FILE_PATH = (
    MOUNT_PATH + FILELOCATION_READY4SUB + PREFIX_READY4SUB + EXTENTION_READY4SUB
)

FILELOCATION_ELEVENLAB = _CONFIG.get("filelocation.elevenlab", "")
PREFIX_ELEVENLAB = _CONFIG.get("prefix.elevenlab", "")
EXTENTION_ELEVENLAB = "."+_CONFIG.get("extention.elevenlab", "")
ELEVENLAB_FILE_PATH = (
    MOUNT_PATH + FILELOCATION_ELEVENLAB + PREFIX_ELEVENLAB + EXTENTION_ELEVENLAB
)

FILELOCATION_ELEVENLAB2SUB = _CONFIG.get("filelocation.elevenlab2sub", "")
PREFIX_ELEVENLAB2SUB = _CONFIG.get("prefix.elevenlab2sub", "")
EXTENTION_ELEVENLAB2SUB = "."+_CONFIG.get("extention.elevenlab2sub", "")
ELEVENLAB2SUB_FILE_PATH = (
    MOUNT_PATH + FILELOCATION_ELEVENLAB2SUB + PREFIX_ELEVENLAB2SUB + EXTENTION_ELEVENLAB2SUB
)

FILELOCATION_LYRICS = _CONFIG.get("filelocation.lyrics", "")
PREFIX_LYRICS = _CONFIG.get("prefix.lyrics", "")
EXTENTION_LYRICS = "."+_CONFIG.get("extention.lyrics", "")
LYRICS_FILE_PATH = MOUNT_PATH + FILELOCATION_LYRICS + PREFIX_LYRICS + EXTENTION_LYRICS

FILELOCATION_READY2UP = _CONFIG.get("filelocation.ready2up", "")
PREFIX_READY2UP = _CONFIG.get("prefix.ready2up", "")
EXTENTION_READY2UP = "."+_CONFIG.get("extention.ready2up", "")
READY2UP_FILE_PATH = (
    MOUNT_PATH + FILELOCATION_READY2UP + PREFIX_READY2UP + EXTENTION_READY2UP
)

# Optional helper if direct dictionary access is needed.
CONFIG = dict(_CONFIG)
