# WebGIS Course Materials Integration Guide

This guide will help you integrate all course materials from the GEOG 678 WebGIS repository into your Notion dashboard and Google Calendar.

## 📁 Generated Files

The extraction scripts have created the following files in the `output/` directory:

1. **course_materials_notion_import.csv** - Base CSV with all course materials (no due dates)
2. **course_materials_with_dates.csv** - CSV with sample due dates for easy import
3. **course_materials_full.json** - Complete JSON export of all course data
4. **course_materials_overview.md** - Markdown overview of all materials

## 🎯 What Was Extracted

- **15 Labs** - All lab assignments from labs/
- **36 Modules** - All learning modules from modules/
- **7 Project Components** - All project deliverables from project/

## 📊 Importing to Notion

### Method 1: Direct CSV Import (Recommended)

1. **Open your Notion workspace**
   - Navigate to: https://www.notion.so/288e68e9be5c811c8288e35dcdd58182?v=288e68e9be5c81309ee7000ce2021791

2. **Import the CSV**
   - Click the "⋯" menu in the top right of your database
   - Select "Merge with CSV"
   - Upload `output/course_materials_with_dates.csv`
   - Map the CSV columns to your Notion database properties:
     - Type → Type
     - Number → Number
     - Title → Title
     - Topic → Topic
     - Description → Description
     - File Path → File Path
     - Status → Status
     - Due Date → Due Date
     - Priority → Priority
     - Tags → Tags

3. **Adjust the due dates**
   - The CSV includes sample due dates based on a typical semester schedule
   - Modify these dates in Notion to match your actual course schedule

### Method 2: Manual Entry

If CSV import doesn't work with your Notion setup, you can:
1. Open `output/course_materials_overview.md`
2. Copy and paste sections into Notion
3. Use Notion's markdown import feature

## 📅 Syncing to Google Calendar

### Prerequisites

1. **Install Google Calendar API**
   ```bash
   pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
   ```

2. **Set up Google Cloud Project**
   - Go to https://console.cloud.google.com/
   - Create a new project or select existing one
   - Enable the Google Calendar API
   - Create OAuth 2.0 credentials (Desktop app)
   - Download credentials and save as `credentials.json` in the repository root

### Sync Process

1. **Adjust due dates in the CSV** (if needed)
   ```bash
   # Open and edit the CSV file
   nano output/course_materials_with_dates.csv
   ```

2. **Run the sync script**
   ```bash
   python3 google_calendar_sync.py --sync --email eric@bottomlinesa.com
   ```

3. **Follow the OAuth flow**
   - A browser window will open
   - Sign in with your Google account (eric@bottomlinesa.com)
   - Grant calendar access permissions
   - The script will create events for all items with due dates

### Calendar Event Details

Each event will include:
- **Title**: Type + Title (e.g., "Lab: GitHub Setup")
- **Description**: Task details and file path
- **Date**: All-day event on the due date
- **Reminders**:
  - Email reminder 1 day before
  - Popup reminder 1 hour before
- **Color coding**:
  - Labs: Blue
  - Modules: Green
  - Projects: Red

## 🔧 Customization

### Adjusting Due Dates

You can modify the due date logic in `google_calendar_sync.py`:

```python
# Around line 150-180
if item_type == 'Lab':
    # Change to your preferred schedule
    due_date = start_date + timedelta(weeks=week_counter, days=4)
```

### Adding Custom Fields

To add custom fields to the CSV:

1. Edit `extract_course_materials.py`
2. Modify the `generate_csv()` method (around line 120)
3. Add your custom fields to the dictionary
4. Re-run: `python3 extract_course_materials.py`

## 📋 Course Material Summary

### Labs (15 total)
- Lab 01: GitHub Setup
- Lab 02: ArcGIS Online
- Lab 03: Web Programming
- Lab 04: Javascript and JSON programming
- Lab 05: Basic Javascript Mapping with Leaflet JS
- Lab 06: Advanced Javascript Mapping with Leaflet JS
- Lab 06b: Javascript Data Merging
- Lab 08: ArcGIS StoryMaps with 3D Layers
- Lab 09: Interactive Charts
- Lab 10: Feature Layer Web Editing
- Lab 11: COVID-19 Data Collection
- Plus 4 alternate versions (_02, _05, _06, _08)

### Modules (36 total)
Modules 01-35 covering various WebGIS topics from GitHub basics to advanced mapping techniques.

### Project Components (7 total)
- Project Pitch
- Project Proposal
- Status Reports
- Team Evaluation
- Final Report
- Final Checklist
- Prior Projects (reference)

## 🚨 Troubleshooting

### Notion Import Issues

**Problem**: CSV columns don't match Notion properties
- **Solution**: In Notion, create custom properties that match the CSV columns, or modify the CSV column names to match your existing properties

**Problem**: Dates not importing correctly
- **Solution**: Ensure dates are in YYYY-MM-DD format in the CSV

### Google Calendar Sync Issues

**Problem**: "credentials.json not found"
- **Solution**: Follow the Google Cloud setup steps above to create and download credentials

**Problem**: "Authentication failed"
- **Solution**: Delete `token.pickle` and re-authenticate

**Problem**: Events not showing up
- **Solution**: Check that due dates are filled in the CSV and in correct format (YYYY-MM-DD)

## 🔄 Re-running the Extraction

If the course materials are updated, you can re-extract:

```bash
# Re-extract all materials
python3 extract_course_materials.py

# Generate new CSV with dates
python3 google_calendar_sync.py --template

# Sync to calendar
python3 google_calendar_sync.py --sync --email eric@bottomlinesa.com
```

## 📧 Support

If you need help with:
- **Notion issues**: Check Notion's help docs at https://www.notion.so/help
- **Google Calendar API**: See https://developers.google.com/calendar/api/guides/overview
- **Script errors**: Check the error messages and ensure all dependencies are installed

## 🎓 Next Steps

1. ✅ Review the generated CSV files
2. ✅ Import to Notion using the guide above
3. ✅ Adjust due dates to match your course schedule
4. ✅ Set up Google Calendar API credentials
5. ✅ Sync events to your calendar
6. ✅ Stay organized and ace your WebGIS course!

---

*Generated on 2025-11-04 for TAMU GEOG 678 WebGIS Course*
