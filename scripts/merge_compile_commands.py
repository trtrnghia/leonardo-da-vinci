#!/usr/bin/env python3
import glob
import json
import os
import sys

ws_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
build_dir = os.path.join(ws_dir, 'build')
output_file = os.path.join(build_dir, 'compile_commands.json')
symlink_file = os.path.join(ws_dir, 'compile_commands.json')

all_entries = []
pattern = os.path.join(build_dir, '*', 'compile_commands.json')
for file_path in glob.glob(pattern):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                all_entries.extend(data)
    except Exception as e:
        print(f'Warning: could not read {file_path}: {e}', file=sys.stderr)

if all_entries:
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_entries, f, indent=2)
    try:
        if os.path.islink(symlink_file) or os.path.exists(symlink_file):
            os.remove(symlink_file)
        os.symlink(os.path.relpath(output_file, ws_dir), symlink_file)
    except Exception as e:
        print(f'Warning: could not create symlink: {e}', file=sys.stderr)
    print(f'Successfully merged {len(all_entries)} compile commands -> {symlink_file}')
else:
    print('No compile_commands.json found yet in build/ (run build first).')
