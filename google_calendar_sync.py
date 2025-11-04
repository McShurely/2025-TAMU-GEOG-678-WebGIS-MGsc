#!/usr/bin/env python3
"""
Google Calendar Sync Script for WebGIS Course Materials
Syncs course assignments from CSV to Google Calendar
"""

import csv
import os
import pickle
from datetime import datetime, timedelta
from pathlib import Path

# Google Calendar API imports
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googlecalendar import build
    GOOGLE_CALENDAR_AVAILABLE = True
except ImportError:
    GOOGLE_CALENDAR_AVAILABLE = False
    print("⚠️  Google Calendar API not installed.")
    print("   Install with: pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib")

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

class GoogleCalendarSync:
    def __init__(self, calendar_email: str):
        self.calendar_email = calendar_email
        self.service = None
        self.calendar_id = 'primary'  # Use primary calendar

    def authenticate(self):
        """Authenticate with Google Calendar API"""
        creds = None
        token_file = 'token.pickle'
        credentials_file = 'credentials.json'

        # Check if we have saved credentials
        if os.path.exists(token_file):
            with open(token_file, 'rb') as token:
                creds = pickle.load(token)

        # If there are no (valid) credentials available, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(credentials_file):
                    print(f"\n❌ ERROR: {credentials_file} not found!")
                    print("\n📋 To use Google Calendar sync, you need to:")
                    print("   1. Go to https://console.cloud.google.com/")
                    print("   2. Create a new project or select existing one")
                    print("   3. Enable the Google Calendar API")
                    print("   4. Create OAuth 2.0 credentials (Desktop app)")
                    print("   5. Download the credentials and save as 'credentials.json'")
                    print("   6. Run this script again")
                    return False

                flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
                creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open(token_file, 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('calendar', 'v3', credentials=creds)
        return True

    def create_event(self, title: str, description: str, due_date: str, event_type: str):
        """Create a calendar event"""
        if not self.service:
            print("❌ Not authenticated. Run authenticate() first.")
            return None

        try:
            # Parse the due date
            due_datetime = datetime.strptime(due_date, '%Y-%m-%d')

            # Create all-day event
            event = {
                'summary': f"{event_type}: {title}",
                'description': description,
                'start': {
                    'date': due_datetime.strftime('%Y-%m-%d'),
                    'timeZone': 'America/Chicago',
                },
                'end': {
                    'date': due_datetime.strftime('%Y-%m-%d'),
                    'timeZone': 'America/Chicago',
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},  # 1 day before
                        {'method': 'popup', 'minutes': 60},  # 1 hour before
                    ],
                },
                'colorId': self.get_color_id(event_type),
            }

            event = self.service.events().insert(calendarId=self.calendar_id, body=event).execute()
            return event

        except Exception as e:
            print(f"❌ Error creating event: {e}")
            return None

    def get_color_id(self, event_type: str) -> str:
        """Get color ID based on event type"""
        colors = {
            'Lab': '9',      # Blue
            'Module': '10',  # Green
            'Project': '11', # Red
            'Quiz': '5',     # Yellow
            'Exam': '11',    # Red
        }
        return colors.get(event_type, '1')

    def sync_from_csv(self, csv_file: str):
        """Sync events from CSV file to Google Calendar"""
        if not self.service:
            print("❌ Not authenticated. Cannot sync.")
            return

        created_count = 0
        skipped_count = 0

        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

            print(f"\n📅 Syncing {len(rows)} items to Google Calendar...")
            print(f"   Calendar: {self.calendar_email}\n")

            for row in rows:
                due_date = row.get('Due Date', '').strip()

                if not due_date:
                    print(f"⏭️  Skipping '{row['Title']}' - No due date")
                    skipped_count += 1
                    continue

                title = row.get('Title', 'Untitled')
                event_type = row.get('Type', 'Assignment')
                description = row.get('Description', '')

                # Add file path to description
                file_path = row.get('File Path', '')
                if file_path:
                    description += f"\n\nFile: {file_path}"

                print(f"➕ Creating: {event_type} - {title} (Due: {due_date})")
                event = self.create_event(title, description, due_date, event_type)

                if event:
                    created_count += 1
                    print(f"   ✓ Created: {event.get('htmlLink')}")
                else:
                    skipped_count += 1

            print(f"\n✅ Sync complete!")
            print(f"   Created: {created_count}")
            print(f"   Skipped: {skipped_count}")


def manual_csv_template():
    """Generate a simple CSV template without Google API"""
    print("\n📋 Generating manual CSV template with sample due dates...")

    repo_path = os.path.dirname(os.path.abspath(__file__))
    input_csv = Path(repo_path) / 'output' / 'course_materials_notion_import.csv'
    output_csv = Path(repo_path) / 'output' / 'course_materials_with_dates.csv'

    if not input_csv.exists():
        print(f"❌ Input file not found: {input_csv}")
        return

    # Read the input CSV
    with open(input_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Add sample due dates (you can modify these)
    start_date = datetime.now()
    week_counter = 1

    for i, row in enumerate(rows):
        item_type = row['Type']

        if item_type == 'Lab':
            # Labs due every week on Friday
            due_date = start_date + timedelta(weeks=week_counter, days=4)  # Friday
            row['Due Date'] = due_date.strftime('%Y-%m-%d')
            week_counter += 1

        elif item_type == 'Module':
            # Modules spread throughout the semester
            module_num = int(row['Number']) if row['Number'].isdigit() else i
            due_date = start_date + timedelta(days=module_num * 3)
            row['Due Date'] = due_date.strftime('%Y-%m-%d')

        elif item_type == 'Project':
            # Project milestones at specific points
            component = row.get('Topic', '').lower()
            if 'pitch' in component:
                due_date = start_date + timedelta(weeks=3)
            elif 'proposal' in component:
                due_date = start_date + timedelta(weeks=6)
            elif 'status' in component:
                due_date = start_date + timedelta(weeks=10)
            elif 'final' in component:
                due_date = start_date + timedelta(weeks=14)
            else:
                due_date = start_date + timedelta(weeks=12)

            row['Due Date'] = due_date.strftime('%Y-%m-%d')

    # Write the output CSV
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        if rows:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

    print(f"✅ CSV with sample due dates created: {output_csv}")
    print("\n📝 Next steps:")
    print("   1. Open the CSV and adjust the due dates to match your course schedule")
    print("   2. Import the CSV into Notion (use the 'Merge with CSV' option)")
    print("   3. Optionally, run this script with --sync to add events to Google Calendar")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Sync WebGIS course materials to Google Calendar')
    parser.add_argument('--email', default='eric@bottomlinesa.com',
                        help='Google Calendar email address')
    parser.add_argument('--csv', default='output/course_materials_with_dates.csv',
                        help='CSV file to sync')
    parser.add_argument('--sync', action='store_true',
                        help='Sync to Google Calendar (requires API setup)')
    parser.add_argument('--template', action='store_true',
                        help='Generate CSV template with sample due dates')

    args = parser.parse_args()

    if args.template or not args.sync:
        manual_csv_template()

    if args.sync:
        if not GOOGLE_CALENDAR_AVAILABLE:
            print("\n❌ Cannot sync: Google Calendar API not installed")
            print("   Install with: pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib")
            return

        print(f"\n🔐 Authenticating with Google Calendar...")
        print(f"   Email: {args.email}\n")

        syncer = GoogleCalendarSync(args.email)
        if syncer.authenticate():
            print("✅ Authentication successful!")
            syncer.sync_from_csv(args.csv)
        else:
            print("❌ Authentication failed")


if __name__ == "__main__":
    main()
