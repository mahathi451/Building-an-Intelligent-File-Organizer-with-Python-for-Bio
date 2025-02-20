from pathlib import Path
import shutil
import hashlib
from datetime import datetime
from .rules import load_rules

class FileOrganizer:
    def __init__(self, root_path):
        self.root = Path(root_path)
        self.rules = load_rules()
        self.log = []
        
    def _get_category(self, file_path):
        ext = file_path.suffix.lower()
        for category, rule in self.rules.items():
            if ext in rule['extensions']:
                return category
        return 'other'
    
    def _create_destination(self, category, file_path):
        timestamp = datetime.now().strftime("%Y-%m-%d")
        return self.root / category / timestamp / file_path.name
    
    def organize(self):
        for item in self.root.glob('**/*'):
            if item.is_file():
                category = self._get_category(item)
                dest = self._create_destination(category, item)
                dest.parent.mkdir(parents=True, exist_ok=True)
                
                if not dest.exists():
                    shutil.move(str(item), str(dest))
                    self.log.append(f"Moved {item} to {dest}")
                else:
                    file_hash = hashlib.md5(item.read_bytes()).hexdigest()
                    dest_hash = hashlib.md5(dest.read_bytes()).hexdigest()
                    if file_hash != dest_hash:
                        new_name = f"{item.stem}_conflict{item.suffix}"
                        shutil.move(str(item), str(dest.parent / new_name))
                        self.log.append(f"Resolved conflict: {new_name}")
