# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ANALYSIS OF CONNECTIONS ON INSTAGRAM
# REPOSITORY: https://github.com/cassianorcarneiro/ig-connections-analysis
# CASSIANO RIBEIRO CARNEIRO
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

"""
Lists the accounts you follow that do not follow you back, based on the
JSON data export from Instagram.
"""

import json
from pathlib import Path

import pandas as pd
from openpyxl.utils import get_column_letter
from rich.console import Console

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Settings
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Paths are relative to this file, so the script works from any working directory

BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / 'connections' / 'followers_and_following'
OUTPUT_FILE = BASE_DIR / 'not_following_back.xlsx'

console = Console()

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Data extraction
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def load_entries(file_path):
    """Reads one export file and returns a list of {'username', 'timestamp'}."""

    with open(file_path, 'r', encoding='utf-8') as f:
        raw = json.load(f)

    # followers_*.json is a bare list; following.json wraps the list in a key
    # ('relationships_following'). Take the first list found in either case.

    if isinstance(raw, list):
        items = raw
    elif isinstance(raw, dict):
        items = next((v for v in raw.values() if isinstance(v, list)), [])
    else:
        items = []

    entries = []

    for item in items:

        data = (item.get('string_list_data') or [{}])[0]

        # followers pattern: username in 'value'; following pattern: username in 'title'

        username = data.get('value') or item.get('title')

        if username:
            entries.append({
                'username': username.strip().lower(),  # Instagram usernames are case-insensitive
                'timestamp': data.get('timestamp'),
            })

    return entries

def load_followers():

    files = sorted(INPUT_DIR.glob('followers_*.json'))  # Large accounts are split across files

    if not files:
        raise FileNotFoundError(f'No followers_*.json found in {INPUT_DIR}')

    entries = [e for f in files for e in load_entries(f)]

    return pd.DataFrame(entries, columns=['username', 'timestamp']).drop_duplicates('username')

def load_following():

    path = INPUT_DIR / 'following.json'

    if not path.exists():
        raise FileNotFoundError(f'{path} not found')

    entries = load_entries(path)

    return pd.DataFrame(entries, columns=['username', 'timestamp']).drop_duplicates('username')

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Spreadsheet export
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def export_excel(df, path):

    sheet = 'not_following_back'

    with pd.ExcelWriter(path, engine='openpyxl', datetime_format='YYYY-MM-DD HH:MM') as writer:

        df.to_excel(writer, index=False, sheet_name=sheet)
        ws = writer.sheets[sheet]

        ws.freeze_panes = 'A2'
        ws.auto_filter.ref = ws.dimensions

        # Clickable links

        url_col = df.columns.get_loc('profile_url') + 1

        for row in range(2, len(df) + 2):
            cell = ws.cell(row=row, column=url_col)
            cell.hyperlink = cell.value
            cell.style = 'Hyperlink'

        # Column widths fitted to content

        for idx, col in enumerate(df.columns, 1):
            width = max([len(str(col))] + [len(str(v)) for v in df[col]]) + 2
            ws.column_dimensions[get_column_letter(idx)].width = min(width, 60)

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Execution
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def main():

    console.clear()

    try:
        followers = load_followers()
        following = load_following()
    except FileNotFoundError as e:
        console.print(f'[red]{e}\nSee README, step 2.')
        raise SystemExit(1)

    # Accounts that do NOT follow back

    not_back = following[~following['username'].isin(followers['username'])].copy()
    not_back['profile_url'] = 'https://www.instagram.com/' + not_back['username'] + '/'
    not_back['followed_since'] = pd.to_datetime(not_back['timestamp'], unit='s')
    not_back = not_back[['username', 'profile_url', 'followed_since']].reset_index(drop=True)

    # Summary

    console.print(f'\n[blue]Followers:[/] {len(followers)}')
    console.print(f'[blue]Following:[/] {len(following)}')
    console.print(f'[blue]Not following back:[/] {len(not_back)}')

    # Export

    try:
        export_excel(not_back, OUTPUT_FILE)
    except PermissionError:
        console.print(f'[red]Cannot write {OUTPUT_FILE.name}. Close it in Excel and run again.')
        raise SystemExit(1)

    console.print(f'\n[green]Spreadsheet saved to {OUTPUT_FILE}\n')

if __name__ == '__main__':
    main()