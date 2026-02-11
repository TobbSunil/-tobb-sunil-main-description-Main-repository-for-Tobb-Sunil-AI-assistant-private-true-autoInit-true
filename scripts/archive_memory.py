#!/usr/bin/env python3
"""Archive old daily memory files (older than 7 days) into memory/archive.
Updates a simple JSON index at memory/index.json with file metadata.
"""
import os
import shutil
import json
from datetime import datetime, timedelta

WORKDIR = os.path.abspath(os.path.dirname(__file__) + '/../..')
MEMORY_DIR = os.path.join(WORKDIR, 'memory')
ARCHIVE_DIR = os.path.join(MEMORY_DIR, 'archive')
INDEX_FILE = os.path.join(MEMORY_DIR, 'index.json')

# Ensure archive directory exists
os.makedirs(ARCHIVE_DIR, exist_ok=True)

# Load existing index (or start fresh)
if os.path.exists(INDEX_FILE):
    with open(INDEX_FILE, 'r') as f:
        index = json.load(f)
else:
    index = {}

now = datetime.utcnow()
cutoff = now - timedelta(days=7)

for fname in os.listdir(MEMORY_DIR):
    if not fname.endswith('.md') or fname == 'MEMORY.md' or fname == 'index.json':
        continue
    fpath = os.path.join(MEMORY_DIR, fname)
    # Get file creation/modification time
    mtime = datetime.utcfromtimestamp(os.path.getmtime(fpath))
    if mtime < cutoff:
        # Move to archive
        dest = os.path.join(ARCHIVE_DIR, fname)
        shutil.move(fpath, dest)
        # Record in index
        index_entry = {
            "original_path": f"memory/{fname}",
            "archived_path": f"memory/archive/{fname}",
            "archived_at": datetime.utcnow().isoformat() + 'Z'
        }
        index[fname] = index_entry
        print(f"Archived {fname}")

# Save updated index
with open(INDEX_FILE, 'w') as f:
    json.dump(index, f, indent=2)

print('Archive complete.')
