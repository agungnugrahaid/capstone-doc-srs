#!/bin/sh
# 1) Word: open the built docx, refresh all fields (TOC, lists, citations, bibliography), save.
# 2) link_dois.py: make DOIs in Daftar Pustaka clickable (needs python-docx: set PYTHON=/path/to/venv/bin/python).
# 3) Word: open again WITHOUT refreshing fields (that would drop the links) and export the PDF.
set -e
DIR="$(cd "$(dirname "$0")/.." && pwd)"
HERE="$(cd "$(dirname "$0")" && pwd)"
F="$DIR/Laporan Capstone Project Kelompok 1 - Final.docx"
P="$DIR/Laporan Capstone Project Kelompok 1 - Final.pdf"
PYTHON="${PYTHON:-python3}"
osascript <<OSA
tell application "Microsoft Word"
	open POSIX file "$F"
	delay 8
	set theDoc to active document
	repeat 2 times
		set n to count of fields of theDoc
		repeat with i from 1 to n
			try
				update field (field i of theDoc)
			end try
		end repeat
	end repeat
	save theDoc
	close active document saving no
end tell
OSA
"$PYTHON" "$HERE/link_dois.py" "$F"
osascript <<OSA
tell application "Microsoft Word"
	open POSIX file "$F"
	delay 8
	set theDoc to active document
	save as theDoc file name "$P" file format format PDF
	close active document saving no
end tell
OSA
echo "updated: $F"
echo "pdf: $P"
