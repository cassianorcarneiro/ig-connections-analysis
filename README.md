# 📷 Instagram Connections Analysis

> Find out which Instagram accounts you follow that don't follow you back.

A Python-based tool that processes your exported Instagram connection data and generates a spreadsheet of non-reciprocal follows — with clickable profile links, and no third-party services involved.

<p align="center">
  <img alt="Stack" src="https://img.shields.io/badge/Stack-Python%20%2B%20Pandas-blue?style=for-the-badge">
  <img alt="License" src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge">
  <img alt="Privacy" src="https://img.shields.io/badge/Privacy-Local%20Only-success?style=for-the-badge">
</p>

---

## 📦 Features

- 🔍 **Reciprocity analysis** — identifies accounts you follow that don't follow you back
- 📊 **Spreadsheet output** — XLSX with clickable links, filters and frozen header
- 🔒 **100% local** — works on your exported data; no Instagram API, no network access
- ⚡ **Lightweight** — runs in seconds, even for thousands of connections

---

## 📋 Prerequisites

- **Python 3.9+**
- An Instagram account (to export your data from)
- A few minutes — Instagram takes some time to prepare the export

---

## 🚀 Quick start

The flow is: **export your data from Instagram → drop it in the project folder → run the script → open the spreadsheet**.

### Step 1 — Request your data from Instagram

1. Open Instagram on your phone
2. Go to **your profile**
3. Open **Settings** (three lines in the top-right corner)
4. Open **Accounts Center**
5. Open **Your information and permissions**
6. Click **Export your information**
7. Click **Create export**
8. Select the account
9. Select **Export to device**
10. Click **Customize information**
11. Uncheck everything, leaving only **Followers and following** under the **Connections** section
12. Click **Save**
13. Under **Format**, select **JSON**
14. Under **Date range**, select **All time**
15. Click **Start export**
16. Enter your password and wait — Instagram emails you when it's ready (usually a few minutes to a few hours)

### Step 2 — Place the export in the project

1. Download the `.zip` file Instagram sent you
2. Extract it
3. Move the `connections/` folder into the project root:

```
ig-connections-analysis/
├── ig_connections_analysis.py
├── requirements.txt
└── connections/
    └── followers_and_following/
        ├── followers_1.json      # large accounts also have followers_2.json, ...
        └── following.json
```

### Step 3 — Install dependencies

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate   |   Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```

### Step 4 — Run the analysis

```bash
python ig_connections_analysis.py
```

The script can be run from any directory; paths are resolved relative to the script itself.

---

## 📊 Output

`not_following_back.xlsx`, with one row per account you follow that doesn't follow you back:

| Column | Description |
|---|---|
| `username` | Account username |
| `profile_url` | Clickable link to the profile |
| `followed_since` | When you started following the account (UTC) |

The sheet has a frozen header and column filters.

### Limitations

- The export is a snapshot. Accounts that followed you after the export date still appear in the list. Request a fresh export before a cleanup session.
- Links of accounts that were deleted, deactivated or renamed open Instagram's "page not available" screen. Deleted accounts are removed from your following list by Instagram itself, so they need no action.

---

## 📁 Project structure

```
ig-connections-analysis/
├── ig_connections_analysis.py    # Main script
├── requirements.txt
├── README.md
├── LICENSE
├── connections/                  # ← drop your Instagram export here (git-ignored)
│   └── followers_and_following/
│       ├── followers_*.json
│       └── following.json
└── not_following_back.xlsx       # Output (git-ignored)
```

---

## 🔐 Privacy

- ✅ Your Instagram data stays on your machine — the script makes no network requests
- ✅ No API keys, no authentication, no remote services
- ✅ The output spreadsheet is local and git-ignored; share it only if you choose to

---

## 🛣️ Roadmap

- [ ] CLI flags for custom input/output paths
- [ ] Optional CSV output (in addition to XLSX)
- [ ] Detect mutual follows + visualize as a Venn diagram
- [ ] Support for "close friends" / "blocked" / "muted" lists from the same export
- [ ] Pip-installable package

---

## 📜 License

MIT — see `LICENSE` file.

## 👤 Author

**Cassiano Ribeiro Carneiro** — [@cassianorcarneiro](https://github.com/cassianorcarneiro)

---

### 🤖 AI Assistance Disclosure

The codebase architecture, organizational structure, and stylistic formatting of this repository were refactored and optimized leveraging [Claude](https://www.anthropic.com/claude) by Anthropic. All core business logic and intellectual property remain the work of the repository authors and are governed by the project's license.

---

> *Curiosity about your Instagram followers, satisfied without selling your data to a sketchy third-party tool.*