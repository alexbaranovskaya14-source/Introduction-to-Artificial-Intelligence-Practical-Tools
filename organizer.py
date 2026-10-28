#!/usr/bin/env python3
"""File Organizer - sort files in a folder into category sub-folders."""
import argparse
from pathlib import Path

CATEGORIES = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".bmp"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".md", ".odt", ".rtf"},
    "Spreadsheets": {".xls", ".xlsx", ".csv", ".ods"},
    "Presentations": {".ppt", ".pptx", ".odp", ".key"},
    "Archives": {".zip", ".tar", ".gz", ".7z", ".rar"},
    "Audio": {".mp3", ".wav", ".flac", ".ogg", ".m4a"},
    "Video": {".mp4", ".mkv", ".avi", ".mov", ".webm"},
    "Code": {".py", ".js", ".html", ".css", ".java", ".c", ".cpp", ".sh", ".json"},
}


def category_for(path: Path) -> str:
    ext = path.suffix.lower()
    for name, exts in CATEGORIES.items():
        if ext in exts:
            return name
    return "Other"


def plan(folder: Path):
    """Return a list of (source, destination) moves."""
    moves = []
    for item in sorted(folder.iterdir()):
        if item.is_file() and not item.name.startswith("."):
            moves.append((item, folder / category_for(item) / item.name))
    return moves


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", type=Path, help="folder to organize")
    args = parser.parse_args()
    for src, dst in plan(args.folder):
        print(f"{src.name} -> {dst.parent.name}/")


if __name__ == "__main__":
    main()
