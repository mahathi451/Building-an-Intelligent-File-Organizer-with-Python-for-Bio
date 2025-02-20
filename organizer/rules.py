import yaml
from pathlib import Path
from typing import Dict, Any

def load_rules(config_path: Path = None) -> Dict[str, Any]:
    """Load organization rules from YAML config"""
    default_path = Path(__file__).parent.parent / "config" / "organization_rules.yaml"
    
    with open(config_path or default_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Validate structure
    required_keys = ['categories', 'conflict']
    if not all(key in config for key in required_keys):
        raise ValueError("Invalid organization rules config")
    
    return config
