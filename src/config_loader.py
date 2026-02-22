"""
Configuration Loader Module
Manages application configuration.
"""

import os
import yaml
from typing import Dict, Any


def load_config(config_path: str = None) -> Dict[str, Any]:
    """
    Load application configuration.
    
    Args:
        config_path: Path to config file
        
    Returns:
        Configuration dictionary
    """
    if config_path is None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        config_path = os.path.join(project_root, 'config', 'app_config.yaml')
    
    if not os.path.exists(config_path):
        return get_default_config()
    
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def get_default_config() -> Dict[str, Any]:
    """Get default configuration."""
    return {
        'model': {
            'name': 'llama3.2:3b',
            'timeout': 60,
            'max_retries': 3,
            'temperature': 0.1
        },
        'rules': {
            'dockerfile': 'config/rules.yaml',
            'strict_mode': False
        },
        'output': {
            'add_comments': True,
            'add_explanations': True,
            'format': 'detailed'
        },
        'logging': {
            'level': 'INFO',
            'file': 'logs/app.log',
            'audit_file': 'logs/audit.log'
        }
    }


def save_config(config: Dict[str, Any], config_path: str = None):
    """Save configuration to file."""
    if config_path is None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        config_path = os.path.join(project_root, 'config', 'app_config.yaml')
    
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)
