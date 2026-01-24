# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Analysis of Connections on Instagram
# CASSIANO RIBEIRO CARNEIRO
# VERSION: 26/11/2025
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Framework imports

import json
import pandas as pd
import os
from rich.console import Console

# Directory names

code_directory = os.getcwd()
inputs_directory = code_directory + '/connections/followers_and_following'

# Clear the terminal

os.system('cls')

# Tool for customized terminal printing

console = Console()

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Function to extract data
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def extract_data(file_path, root_key=None):
    
    with open(file_path, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
    
    # Logic to define the source of the list (root or specific key)
    
    items_list = []

    if isinstance(raw_data, list):
        items_list = raw_data                         # Case of followers_1.json (direct list)
    elif isinstance(raw_data, dict):
        if root_key and root_key in raw_data:
            items_list = raw_data[root_key]           # Case of following.json
        else:
            for key in raw_data:                      # Try to find the first available list if no key is provided
                if isinstance(raw_data[key], list):
                    items_list = raw_data[key]
                    break

    data_list = []

    for item in items_list:

        # Prepare temporary variables

        internal_data = {}
        if 'string_list_data' in item and len(item['string_list_data']) > 0:
            internal_data = item['string_list_data'][0]
        
        # Username extraction

        # Try to get 'value' from inside the list (followers pattern)
        
        username = internal_data.get('value')
        
        # If 'value' does not exist or is empty, get 'title' (following pattern)
        
        if not username:
            username = item.get('title')

        # Only add if a valid username was found

        if username:
            data_list.append({
                'value': username,
                'timestamp': internal_data.get('timestamp'),  # May be None if not available
                'href': internal_data.get('href')
            })
            
    return data_list

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Execution
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Processing FOLLOWERS file

try:
    followers_data = extract_data(inputs_directory + '/followers_1.json')  # Sometimes there is no root key or it varies
except Exception:
    followers_data = extract_data(inputs_directory + '/followers_1.json', 'relationships_followers')

df_followers = pd.DataFrame(followers_data)

# Processing FOLLOWING file

try:
    following_data = extract_data(inputs_directory + '/following.json', 'relationships_following')
except Exception:
    following_data = extract_data(inputs_directory + '/following.json')

df_following = pd.DataFrame(following_data)

# Convert timestamp to readable date

if not df_followers.empty:
    df_followers['readable_date'] = pd.to_datetime(df_followers['timestamp'], unit='s')
if not df_following.empty:
    df_following['readable_date'] = pd.to_datetime(df_following['timestamp'], unit='s')

# Create DataFrame of accounts that do NOT follow back

if not df_following.empty and not df_followers.empty:
    df_not_following_back = df_following[~df_following['value'].isin(df_followers['value'])].copy()
else:
    df_not_following_back = pd.DataFrame()

df_followers.drop(columns=['timestamp'], inplace=True)
df_following.drop(columns=['timestamp'], inplace=True)
df_not_following_back.drop(columns=['timestamp'], inplace=True)

# Display results

console.print('\n\n')
console.print(f"\n[blue]Followers ({len(df_followers)}):\n")
print(df_followers)
console.print(f'\n[blue]Following ({len(df_following)}):\n')
print(df_following)
console.print(f"\n[blue]Not following back ({len(df_not_following_back)})\n")
print(df_not_following_back)
console.print('\n\n')

# Export to spreadsheet

df_not_following_back.to_excel(code_directory + "/not_following_back.xlsx", index=False)
