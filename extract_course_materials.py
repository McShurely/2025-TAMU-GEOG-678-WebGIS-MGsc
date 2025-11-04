#!/usr/bin/env python3
"""
WebGIS Course Material Extractor
Extracts all labs, modules, and project information from the course repository
Generates CSV and JSON files for import into Notion and Google Calendar
"""

import os
import re
import json
import csv
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any

class CourseExtractor:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.labs = []
        self.modules = []
        self.projects = []

    def extract_markdown_title(self, content: str) -> str:
        """Extract the first H1 title from markdown content"""
        lines = content.split('\n')
        for line in lines:
            if line.startswith('# '):
                return line.replace('# ', '').strip()
        return "Untitled"

    def extract_topic(self, content: str) -> str:
        """Extract topic from markdown content (usually in quotes or after 'Topic:')"""
        # Look for **Topic:** pattern
        topic_match = re.search(r'\*\*Topic:\*\*\s*(.+)', content)
        if topic_match:
            return topic_match.group(1).strip()

        # Look for quoted topic
        quote_match = re.search(r'>\s*\*\*Topic:\*\*\s*(.+)', content)
        if quote_match:
            return quote_match.group(1).strip()

        return ""

    def extract_learning_objectives(self, content: str) -> List[str]:
        """Extract learning objectives from markdown content"""
        objectives = []
        in_objectives = False

        lines = content.split('\n')
        for line in lines:
            if 'Learning Objectives' in line or 'learning objectives' in line:
                in_objectives = True
                continue
            if in_objectives:
                if line.strip().startswith('- ') or line.strip().startswith('* '):
                    objectives.append(line.strip()[2:].strip())
                elif line.strip().startswith('#'):
                    break
                elif line.strip() == '' or line.strip().startswith('>'):
                    continue
                else:
                    if objectives:  # Stop if we've collected objectives and hit non-objective content
                        break

        return objectives

    def parse_lab(self, lab_file: Path) -> Dict[str, Any]:
        """Parse a lab file and extract relevant information"""
        with open(lab_file, 'r', encoding='utf-8') as f:
            content = f.read()

        lab_number = re.search(r'(\d+|_\d+)', lab_file.stem)
        lab_num = lab_number.group(1) if lab_number else lab_file.stem

        title = self.extract_markdown_title(content)
        topic = self.extract_topic(content)

        # Extract tasks
        tasks = []
        task_section = re.search(r'# \*\*Tasks:\*\*(.+?)(?=\n#|$)', content, re.DOTALL)
        if task_section:
            task_lines = task_section.group(1).split('\n')
            for line in task_lines:
                if re.match(r'^\d+\.', line.strip()):
                    tasks.append(line.strip())

        return {
            'type': 'Lab',
            'number': lab_num,
            'title': title,
            'topic': topic,
            'tasks': tasks,
            'file_path': str(lab_file.relative_to(self.repo_path)),
            'status': 'Not Started'
        }

    def parse_module(self, module_file: Path) -> Dict[str, Any]:
        """Parse a module file and extract relevant information"""
        with open(module_file, 'r', encoding='utf-8') as f:
            content = f.read()

        module_number = re.search(r'(\d+)', module_file.stem)
        mod_num = module_number.group(1) if module_number else module_file.stem

        title = self.extract_markdown_title(content)
        objectives = self.extract_learning_objectives(content)

        return {
            'type': 'Module',
            'number': mod_num,
            'title': title,
            'learning_objectives': objectives,
            'file_path': str(module_file.relative_to(self.repo_path)),
            'status': 'Not Started'
        }

    def parse_project_component(self, project_dir: Path) -> Dict[str, Any]:
        """Parse a project component directory"""
        readme_file = project_dir / 'readme.md'
        if not readme_file.exists():
            readme_file = project_dir / 'README.md'
            if not readme_file.exists():
                # Check for numbered files
                md_files = list(project_dir.glob('*.md'))
                if md_files:
                    readme_file = md_files[0]
                else:
                    return None

        with open(readme_file, 'r', encoding='utf-8') as f:
            content = f.read()

        title = self.extract_markdown_title(content)

        return {
            'type': 'Project',
            'component': project_dir.name,
            'title': title,
            'file_path': str(readme_file.relative_to(self.repo_path)),
            'status': 'Not Started'
        }

    def extract_all(self):
        """Extract all course materials"""
        # Extract labs
        labs_dir = self.repo_path / 'labs'
        if labs_dir.exists():
            for lab_file in sorted(labs_dir.glob('*.md')):
                if lab_file.name != 'README.md':
                    lab_data = self.parse_lab(lab_file)
                    self.labs.append(lab_data)

        # Extract modules
        modules_dir = self.repo_path / 'modules'
        if modules_dir.exists():
            for module_file in sorted(modules_dir.glob('*.md')):
                if module_file.name != 'README.md':
                    module_data = self.parse_module(module_file)
                    self.modules.append(module_data)

        # Extract project components
        project_dir = self.repo_path / 'project'
        if project_dir.exists():
            for component_dir in sorted(project_dir.iterdir()):
                if component_dir.is_dir():
                    project_data = self.parse_project_component(component_dir)
                    if project_data:
                        self.projects.append(project_data)

    def generate_csv(self, output_file: str):
        """Generate CSV file for Notion import"""
        all_items = []

        # Add labs
        for lab in self.labs:
            all_items.append({
                'Type': lab['type'],
                'Number': lab['number'],
                'Title': lab['title'],
                'Topic': lab['topic'],
                'Description': '; '.join(lab['tasks'][:3]) if lab['tasks'] else '',
                'File Path': lab['file_path'],
                'Status': lab['status'],
                'Due Date': '',  # To be filled in by user
                'Priority': 'Medium',
                'Tags': 'Lab'
            })

        # Add modules
        for module in self.modules:
            all_items.append({
                'Type': module['type'],
                'Number': module['number'],
                'Title': module['title'],
                'Topic': '',
                'Description': '; '.join(module['learning_objectives'][:3]) if module['learning_objectives'] else '',
                'File Path': module['file_path'],
                'Status': module['status'],
                'Due Date': '',  # To be filled in by user
                'Priority': 'Medium',
                'Tags': 'Module'
            })

        # Add projects
        for project in self.projects:
            all_items.append({
                'Type': project['type'],
                'Number': '',
                'Title': f"{project['component']}: {project['title']}",
                'Topic': project['component'],
                'Description': project['component'],
                'File Path': project['file_path'],
                'Status': project['status'],
                'Due Date': '',  # To be filled in by user
                'Priority': 'High',
                'Tags': 'Project'
            })

        # Write CSV
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            if all_items:
                writer = csv.DictWriter(f, fieldnames=all_items[0].keys())
                writer.writeheader()
                writer.writerows(all_items)

    def generate_json(self, output_file: str):
        """Generate JSON file with all extracted data"""
        data = {
            'course': 'GEOG 678 - WebGIS',
            'extracted_date': datetime.now().isoformat(),
            'labs': self.labs,
            'modules': self.modules,
            'projects': self.projects,
            'summary': {
                'total_labs': len(self.labs),
                'total_modules': len(self.modules),
                'total_projects': len(self.projects)
            }
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def generate_notion_markdown(self, output_file: str):
        """Generate a markdown file formatted for easy Notion import"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# GEOG 678 - WebGIS Course Materials\n\n")
            f.write(f"*Extracted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")

            # Labs section
            f.write("## Labs\n\n")
            for lab in self.labs:
                f.write(f"### Lab {lab['number']}: {lab['title']}\n")
                if lab['topic']:
                    f.write(f"**Topic:** {lab['topic']}\n\n")
                if lab['tasks']:
                    f.write("**Tasks:**\n")
                    for task in lab['tasks']:
                        f.write(f"- {task}\n")
                f.write(f"\n**File:** `{lab['file_path']}`\n")
                f.write(f"**Status:** {lab['status']}\n\n")
                f.write("---\n\n")

            # Modules section
            f.write("## Modules\n\n")
            for module in self.modules:
                f.write(f"### Module {module['number']}: {module['title']}\n")
                if module['learning_objectives']:
                    f.write("**Learning Objectives:**\n")
                    for obj in module['learning_objectives']:
                        f.write(f"- {obj}\n")
                f.write(f"\n**File:** `{module['file_path']}`\n")
                f.write(f"**Status:** {module['status']}\n\n")
                f.write("---\n\n")

            # Projects section
            f.write("## Project Components\n\n")
            for project in self.projects:
                f.write(f"### {project['component'].title()}\n")
                f.write(f"**Title:** {project['title']}\n")
                f.write(f"**File:** `{project['file_path']}`\n")
                f.write(f"**Status:** {project['status']}\n\n")
                f.write("---\n\n")


def main():
    # Get the repository path (current directory)
    repo_path = os.path.dirname(os.path.abspath(__file__))

    print("🔍 WebGIS Course Material Extractor")
    print("=" * 50)
    print(f"📁 Repository: {repo_path}\n")

    # Create extractor instance
    extractor = CourseExtractor(repo_path)

    # Extract all materials
    print("📚 Extracting course materials...")
    extractor.extract_all()

    # Print summary
    print(f"\n✅ Extraction complete!")
    print(f"   - Labs: {len(extractor.labs)}")
    print(f"   - Modules: {len(extractor.modules)}")
    print(f"   - Project Components: {len(extractor.projects)}")

    # Generate output files
    print("\n📝 Generating output files...")

    output_dir = Path(repo_path) / 'output'
    output_dir.mkdir(exist_ok=True)

    csv_file = output_dir / 'course_materials_notion_import.csv'
    json_file = output_dir / 'course_materials_full.json'
    md_file = output_dir / 'course_materials_overview.md'

    extractor.generate_csv(str(csv_file))
    print(f"   ✓ CSV file: {csv_file}")

    extractor.generate_json(str(json_file))
    print(f"   ✓ JSON file: {json_file}")

    extractor.generate_notion_markdown(str(md_file))
    print(f"   ✓ Markdown file: {md_file}")

    print("\n🎉 All files generated successfully!")
    print("\n📋 Next steps:")
    print("   1. Open the CSV file in the 'output' directory")
    print("   2. Add due dates to the 'Due Date' column")
    print("   3. Import the CSV into your Notion database")
    print("   4. Use the Google Calendar integration script to sync due dates")


if __name__ == "__main__":
    main()
