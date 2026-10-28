#!/usr/bin/env python3
"""File Organizer - sort files in a folder into category sub-folders."""
import argparse
import json
import shutil
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


def unique_path(dst: Path) -> Path:
    """Never overwrite: report.pdf -> report (1).pdf -> report (2).pdf ..."""
    if not dst.exists():
        return dst
    n = 1
    while True:
        candidate = dst.with_name(f"{dst.stem} ({n}){dst.suffix}")
        if not candidate.exists():
            return candidate
        n += 1


def apply_moves(moves):
    done = []
    for src, dst in moves:
        dst = unique_path(dst)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))
        done.append((src, dst))
    return done


LOG_NAME = ".organizer_log.json"


def save_log(folder: Path, done):
    log = folder / LOG_NAME
    entries = json.loads(log.read_text(encoding="utf-8")) if log.exists() else []
    # Paths are stored relative to the folder, so undo works from any directory.
    entries += [{"from": str(s.relative_to(folder)), "to": str(d.relative_to(folder))}
                for s, d in done]
    log.write_text(json.dumps(entries, indent=2), encoding="utf-8")


def undo(folder: Path):
    """Move files back to where they were, using the last run's log."""
    log = folder / LOG_NAME
    if not log.exists():
        print("No log found - nothing to undo.")
        return
    entries = json.loads(log.read_text(encoding="utf-8"))
    for entry in reversed(entries):
        src, dst = folder / entry["from"], folder / entry["to"]
        if not dst.exists():
            print(f"skip   {dst.name} (no longer there)")
            continue
        src = unique_path(src)
        shutil.move(str(dst), str(src))
        print(f"restored  {dst.name} -> {src.parent.name}/")
        try:
            dst.parent.rmdir()  # only succeeds if the folder is now empty
        except OSError:
            pass
    log.rename(log.with_suffix(".done.json"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", type=Path, help="folder to organize")
    parser.add_argument("--apply", action="store_true",
                        help="really move files (default is a safe preview)")
    parser.add_argument("--undo", action="store_true",
                        help="restore files moved by the previous --apply run")
    args = parser.parse_args()
    args.folder = args.folder.expanduser().resolve()
    if not args.folder.is_dir():
        parser.error(f"not a folder: {args.folder}")
    if args.undo:
        undo(args.folder)
        return

    moves = plan(args.folder)
    if not moves:
        print("Nothing to organize.")
        return
    if args.apply:
        done = apply_moves(moves)
        for src, dst in done:
            print(f"moved  {src.name} -> {dst.parent.name}/{dst.name}")
        save_log(args.folder, done)
    else:
        for src, dst in moves:
            print(f"would move  {src.name} -> {dst.parent.name}/")
        print("\nPreview only. Re-run with --apply to move the files.")


if __name__ == "__main__":
    main()
