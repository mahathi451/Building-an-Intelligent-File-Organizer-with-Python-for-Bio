import pytest
from pathlib import Path
import shutil
from organizer.core import FileOrganizer
import tempfile

@pytest.fixture
def test_files():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create sample files
        (Path(tmpdir) / "test.pdf").touch()
        (Path(tmpdir) / "image.jpg").touch()
        (Path(tmpdir) / "conflict.pdf").touch()
        yield tmpdir

def test_file_categorization(test_files):
    organizer = FileOrganizer(test_files)
    assert organizer._get_category(Path("test.pdf")) == "documents"
    assert organizer._get_category(Path("image.jpg")) == "images"
    assert organizer._get_category(Path("unknown.xyz")) is None

def test_conflict_resolution(test_files):
    # Create duplicate files
    (Path(test_files) / "conflict.pdf").touch()
    (Path(test_files) / "documents" / "2023" / "conflict.pdf").touch()
    
    organizer = FileOrganizer(test_files)
    stats = organizer.organize(dry_run=True)
    
    assert stats['conflicts'] == 1
    assert "conflict" in organizer.log[-1]

def test_directory_creation(test_files):
    organizer = FileOrganizer(test_files)
    organizer.organize(dry_run=True)
    
    assert (Path(test_files) / "documents" / "2023").exists() is False
    assert "Would move" in organizer.log[0]

def test_real_operation(test_files):
    organizer = FileOrganizer(test_files)
    stats = organizer.organize()
    
    assert stats['moved'] == 3
    assert (Path(test_files) / "test.pdf").exists() is False
    assert (Path(test_files) / "documents" / "2023" / "test.pdf").exists()
