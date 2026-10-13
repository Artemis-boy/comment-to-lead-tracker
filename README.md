# Comment-to-Lead Tracker

## What it does
The tool parses Instagram/TikTok comments and classifies them into four categories:
- **MAU BELI** (potential buyers)
- **KOMPLAIN** (complaints that need quick handling)
- **TANYA‑TANYA** (inquiries)
- **LAINNYA** (others)
It also flags high‑priority entries (priority 1) and exports the results to an `xlsx` file for follow‑up.

## How to use
1. Prepare a CSV file named `komen.csv` with the columns:
   ```csv
   username,komen,platform,tanggal
   ```
   See `contoh_komen.csv` for an example.
2. Run the script:
   ```bash
   python komen_ke_pelanggan.py
   ```
3. The script creates `hasil_pilah_komen.xlsx` containing a **Follow‑up** sheet (sorted by priority) and a **Ringkasan** sheet with counts per category.

## Known limitations
- Keyword matching is simplistic; sarcasm or nuanced language may be mis‑categorized.
- Manual review is recommended before responding to customers.

*License: MIT*