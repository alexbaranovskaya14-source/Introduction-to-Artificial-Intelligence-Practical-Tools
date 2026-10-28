# File Organizer

A small console tool that tidies up a messy folder (like `Downloads`) by moving
files into category sub-folders: `Images`, `Documents`, `Spreadsheets`,
`Presentations`, `Archives`, `Audio`, `Video`, `Code` and `Other`.

## The everyday task

Downloads folders turn into a dump of PDFs, screenshots and zip files. Sorting
them by hand is boring and repetitive, so this script does it in one command.
It is built with the safety rules from the course in mind:

- **Preview by default** – nothing is moved unless you pass `--apply`.
- **Never deletes and never overwrites** – a name clash becomes `report (1).pdf`.
- **Undo** – every `--apply` is logged, and `--undo` puts the files back.
- Hidden files and sub-folders are left alone; only the top level is sorted.

## Requirements

Python 3.8+ and nothing else (standard library only).

## How to run

```bash
git clone <this-repo-url>
cd file-organizer

# 1. Preview what would happen (safe, changes nothing)
python3 organizer.py ~/Downloads

# 2. Actually move the files
python3 organizer.py ~/Downloads --apply

# 3. Changed your mind? Restore everything from the last run(s)
python3 organizer.py ~/Downloads --undo
```

Example output:

```
$ python3 organizer.py demo
would move  a.png -> Images/
would move  b.pdf -> Documents/
would move  c.zip -> Archives/

Preview only. Re-run with --apply to move the files.
```

Run the tests with `python3 -m unittest -v`.

To add or change categories, edit the `CATEGORIES` dictionary at the top of
`organizer.py`.

## How AI was used

I used an AI assistant (Claude) for the whole workflow, and treated its output as
a *draft* to be run and checked, as taught in the course.

1. **Generating the script** – prompt (roughly): *"Write a Python 3 console
   script, standard library only, that sorts the files of a folder into
   category sub-folders. It must be safe: preview by default, never delete,
   never overwrite, support undo. Use argparse."* The script was built in small
   steps (categorizer → moving → undo → tests), one Git commit each.
2. **Debugging with AI** – I ran the script on test folders and asked the AI to
   diagnose what went wrong. Two real bugs were found and fixed:
   - *Undo failed from another directory* (`skip a.png (no longer there)`):
     the log stored paths relative to where the script was started. Fix: resolve
     the folder to an absolute path and store log entries relative to the folder.
   - *A second `--apply` overwrote the log*, so the first run could no longer be
     undone. Fix: append to the existing log instead of replacing it.

   Unit tests for both cases were added so they cannot come back.
3. **README** – drafted by the AI from the finished code, then reviewed by me
   for accuracy (every command above was actually run).

See `git log` for the step-by-step history.
