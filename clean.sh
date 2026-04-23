#!/bin/bash
# clean.sh — removes all virtual environments and git-ignored build artifacts.
# Safe to re-run. Does NOT delete source files or config.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "==> Cleaning virtual environments..."
find "$SCRIPT_DIR" -type d -name "venv310" | while read venv; do
    echo "    removing $venv"
    rm -rf "$venv"
done
find "$SCRIPT_DIR" -type d -name "mypyvm" | while read venv; do
    echo "    removing $venv"
    rm -rf "$venv"
done

echo "==> Cleaning git-ignored build artifacts..."
find "$SCRIPT_DIR" -type f \( \
    -name "*.mp3" -o \
    -name "*.wav" -o \
    -name "*.mp4" -o \
    -name "*.srt" -o \
    -name "*.ass" -o \
    -name "*.log" -o \
    -name ".env" \
\) | while read f; do
    echo "    removing $f"
    rm -f "$f"
done

echo "==> Cleaning git-ignore-files/ directory..."
rm -rf "$SCRIPT_DIR/git-ignore-files"

echo "Done. Run each submodule's start.sh to rebuild environments."
