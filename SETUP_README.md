# 🎓 WebGIS Course Material Integration Setup

Welcome! This repository has been set up to help you integrate all GEOG 678 WebGIS course materials into your Notion dashboard and Google Calendar.

## ✅ What's Been Done

All course materials have been extracted and organized:

- ✅ **15 Labs** extracted from `labs/` directory
- ✅ **36 Modules** extracted from `modules/` directory
- ✅ **7 Project Components** extracted from `project/` directory
- ✅ CSV files generated for Notion import
- ✅ JSON export created for backup/reference
- ✅ Google Calendar sync script created

## 📂 Generated Files

Check the `output/` directory for:

```
output/
├── course_materials_notion_import.csv      # Base CSV (no dates)
├── course_materials_with_dates.csv         # CSV with sample due dates
├── course_materials_full.json              # Complete JSON export
└── course_materials_overview.md            # Markdown overview
```

## 🚀 Quick Start

### Step 1: Import to Notion

1. Open your Notion dashboard: https://www.notion.so/288e68e9be5c811c8288e35dcdd58182
2. Click the "⋯" menu → "Merge with CSV"
3. Upload: `output/course_materials_with_dates.csv`
4. Map columns to your Notion properties
5. Adjust due dates as needed

### Step 2: Sync to Google Calendar (Optional)

**Prerequisites:**
```bash
# Install Google Calendar API
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

**Setup:**
1. Create Google Cloud project: https://console.cloud.google.com/
2. Enable Google Calendar API
3. Create OAuth 2.0 credentials (Desktop app)
4. Download credentials as `credentials.json`

**Run Sync:**
```bash
python3 google_calendar_sync.py --sync --email eric@bottomlinesa.com
```

## 📚 Course Materials Summary

### Labs (15)
1. Lab 01: GitHub Setup
2. Lab 02: ArcGIS Online
3. Lab 03: Web Programming
4. Lab 04: Javascript and JSON
5. Lab 05: Leaflet JS Basics
6. Lab 06: Advanced Leaflet JS
7. Lab 08: ArcGIS StoryMaps
8. Lab 09: Interactive Charts
9. Lab 10: Feature Layer Editing
10. Lab 11: COVID-19 Data Collection
... and more

### Modules (36)
Modules 01-35 covering:
- Git/GitHub fundamentals
- Web mapping concepts
- JavaScript programming
- Leaflet JS
- ArcGIS Online
- WebGIS architecture
- And more...

### Project Components (7)
- Pitch
- Proposal
- Status Reports
- Team Evaluation
- Final Report
- Final Checklist

## 🔄 Re-run Extraction

If course materials are updated:

```bash
# Re-extract everything
python3 extract_course_materials.py

# Generate new CSV with sample dates
python3 google_calendar_sync.py --template
```

## 📖 Detailed Instructions

For complete setup and troubleshooting guide, see:
- **[INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)** - Detailed integration instructions

## 🛠️ Available Scripts

### 1. `extract_course_materials.py`
Extracts all labs, modules, and projects from the repository.

```bash
python3 extract_course_materials.py
```

**Outputs:**
- CSV files for Notion import
- JSON file with complete data
- Markdown overview

### 2. `google_calendar_sync.py`
Syncs course materials to Google Calendar.

```bash
# Generate CSV with sample dates
python3 google_calendar_sync.py --template

# Sync to Google Calendar
python3 google_calendar_sync.py --sync --email your@email.com
```

**Options:**
- `--template` - Generate CSV with sample due dates
- `--sync` - Sync events to Google Calendar
- `--email EMAIL` - Specify Google Calendar email
- `--csv FILE` - Specify CSV file to sync

## 📊 Notion Database Properties

Your Notion database should have these properties:

| Property | Type | Description |
|----------|------|-------------|
| Type | Select | Lab, Module, or Project |
| Number | Text | Lab/Module number |
| Title | Title | Assignment title |
| Topic | Text | Topic/subject area |
| Description | Text | Brief description |
| File Path | Text | Path to file in repo |
| Status | Select | Not Started, In Progress, Complete |
| Due Date | Date | Assignment due date |
| Priority | Select | Low, Medium, High |
| Tags | Multi-select | Category tags |

## 🎯 Next Steps

1. [ ] Review generated CSV files in `output/`
2. [ ] Import CSV to your Notion dashboard
3. [ ] Adjust due dates to match your schedule
4. [ ] (Optional) Set up Google Calendar sync
5. [ ] Start working through course materials!

## 💡 Tips

- **Due Dates**: The generated CSV includes sample dates. Adjust these based on your actual course schedule.
- **Custom Fields**: Edit `extract_course_materials.py` to add custom fields to the CSV.
- **Calendar Colors**: Events are color-coded (Labs=Blue, Modules=Green, Projects=Red).
- **Backup**: Keep the JSON file as a backup of all course data.

## 🆘 Troubleshooting

### Notion import not working?
- Ensure CSV columns match your Notion properties
- Try "Merge with CSV" instead of "Import"
- Check date format is YYYY-MM-DD

### Google Calendar sync failing?
- Verify credentials.json is in the repo root
- Delete token.pickle and re-authenticate
- Check you have the correct Google account signed in

### Need help?
- See [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) for detailed troubleshooting
- Check that all dependencies are installed
- Verify file paths are correct

## 📁 Repository Structure

```
2025-TAMU-GEOG-678-WebGIS-MGsc/
├── labs/                          # Lab assignments (15)
├── modules/                       # Learning modules (36)
├── project/                       # Project components (7)
├── output/                        # Generated files
│   ├── course_materials_notion_import.csv
│   ├── course_materials_with_dates.csv
│   ├── course_materials_full.json
│   └── course_materials_overview.md
├── extract_course_materials.py   # Extraction script
├── google_calendar_sync.py       # Calendar sync script
├── SETUP_README.md               # This file
└── INTEGRATION_GUIDE.md          # Detailed guide
```

## 🎓 Good Luck!

You're all set to stay organized and ace your WebGIS course! 🚀

---

*Setup completed on 2025-11-04*
