import hashlib
import logging
from pathlib import Path
import shutil
from datetime import datetime
from typing import Dict, Optional
from .rules import load_rules

logger = logging.getLogger(__name__)

class FileOrganizer:
    def __init__(self, root_path: str):
        self.root = Path(root_path).resolve()
        self.config = load_rules()
        self.log = []
        self.stats = {'moved': 0, 'conflicts': 0}

    def _get_category(self, file_path: Path) -> Optional[str]:
        """Determine file category based on extension"""
        ext = file_path.suffix.lower()
        for category, settings in self.config['categories'].items():
            if ext in settings['extensions']:
                return category
        return None

    def _generate_destination(self, category: str, file_path: Path) -> Path:
        """Generate destination path based on organization rules"""
        date_str = datetime.now().strftime("%Y-%m-%d")
        structure = self.config['categories'][category]['structure']
        
        if structure == 'by_year':
            dest_dir = self.root / category / datetime.now().strftime("%Y")
        elif structure == 'by_month':
            dest_dir = self.root / category / datetime.now().strftime("%Y-%m")
        else:  # flat
            dest_dir = self.root / category
            
        return dest_dir / file_path.name

    def _handle_conflict(self, source: Path, dest: Path) -> Path:
        """Resolve file conflicts using configured strategy"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_name = self.config['conflict']['pattern'].format(
            name=source.stem,
            ext=source.suffix,
            timestamp=timestamp
        )
        resolved_path = dest.parent / new_name
        self.log.append(f"Resolved conflict: {source} → {resolved_path}")
        self.stats['conflicts'] += 1
        return resolved_path

    def _file_hash(self, path: Path) -> str:
        """Calculate MD5 hash of file contents"""
        hash_md5 = hashlib.md5()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def organize(self, dry_run=False) -> Dict[str, int]:
        """Main organization workflow"""
        for item in self.root.rglob('*'):
            if item.is_file() and not item.name.startswith('.'):
                category = self._get_category(item)
                if not category:
                    continue

                dest = self._generate_destination(category, item)
                dest.parent.mkdir(parents=True, exist_ok=True)

                if dest.exists():
                    if self._file_hash(item) == self._file_hash(dest):
                        logger.info(f"Duplicate found: {item}")
                        continue
                    dest = self._handle_conflict(item, dest)

                if not dry_run:
                    shutil.move(str(item), str(dest))
                    self.log.append(f"Moved {item} → {dest}")
                    self.stats['moved'] += 1
                else:
                    self.log.append(f"[DRY RUN] Would move {item} → {dest}")

        return self.stats
