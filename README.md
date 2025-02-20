# Intelligent File Organizer

Automated file management system with conflict resolution and custom rules.

## Features
- File categorization by type/date
- MD5 hash-based conflict detection
- Customizable organization rules
- Detailed operation logging

## Usage
python scripts/organize_files.py ~/Downloads
text

## Custom Rules
Edit `config/organization_rules.yaml`:
documents:
extensions: [.pdf, .docx, .txt]
structure: by_year
images:
extensions: [.jpg, .png, .svg]
structure: flat
text

## Safety Features
- Never deletes files
- Conflict resolution through renaming
- Dry-run mode available (use --dry-run flag)
