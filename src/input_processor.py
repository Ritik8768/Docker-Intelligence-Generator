"""
Input Processor Module
Handles parsing and normalization of user input for Dockerfile generation.
"""

import os
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class ProcessedInput:
    """Data class for processed input."""
    description: str
    files: List[str]
    dependencies: Dict[str, str]
    source_type: str  # 'readme', 'directory', 'text'
    raw_content: Optional[str] = None


def read_readme(path: str) -> str:
    """
    Read README file from specified path.
    
    Args:
        path: Path to README file or directory containing README
        
    Returns:
        Content of README file
        
    Raises:
        FileNotFoundError: If README file not found
    """
    if os.path.isdir(path):
        # Look for common README filenames
        readme_names = ['README.md', 'README.txt', 'README', 'readme.md', 'readme.txt']
        for name in readme_names:
            readme_path = os.path.join(path, name)
            if os.path.exists(readme_path):
                path = readme_path
                break
        else:
            raise FileNotFoundError(f"No README file found in directory: {path}")
    
    if not os.path.exists(path):
        raise FileNotFoundError(f"README file not found: {path}")
    
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def read_directory(path: str) -> Dict[str, List[str]]:
    """
    Read directory structure and identify key files.
    
    Args:
        path: Path to directory
        
    Returns:
        Dictionary with file categories and lists of found files
        
    Raises:
        NotADirectoryError: If path is not a directory
    """
    if not os.path.isdir(path):
        raise NotADirectoryError(f"Not a directory: {path}")
    
    result = {
        'dependency_files': [],
        'config_files': [],
        'source_files': [],
        'all_files': []
    }
    
    # Dependency files to look for
    dependency_patterns = [
        'requirements.txt', 'setup.py', 'pyproject.toml',  # Python
        'package.json', 'package-lock.json', 'yarn.lock',  # Node.js
        'pom.xml', 'build.gradle', 'build.gradle.kts'     # Java
    ]
    
    for root, dirs, files in os.walk(path):
        # Skip hidden directories and common ignore patterns
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv', 'env']]
        
        for file in files:
            if file.startswith('.'):
                continue
                
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, path)
            result['all_files'].append(relative_path)
            
            if file in dependency_patterns:
                result['dependency_files'].append(relative_path)
            elif file.endswith(('.py', '.js', '.java', '.go')):
                result['source_files'].append(relative_path)
            elif file.endswith(('.yml', '.yaml', '.json', '.toml', '.ini')):
                result['config_files'].append(relative_path)
    
    return result


def extract_text_input(text: str) -> Dict[str, str]:
    """
    Extract information from text input.
    
    Args:
        text: Raw text description
        
    Returns:
        Dictionary with extracted information
    """
    return {
        'description': text.strip(),
        'length': len(text),
        'has_content': bool(text.strip())
    }


def normalize_input(raw_input, source_type: str = 'text') -> ProcessedInput:
    """
    Normalize input to standard ProcessedInput format.
    
    Args:
        raw_input: Raw input (path, text, or dict)
        source_type: Type of input ('readme', 'directory', 'text')
        
    Returns:
        ProcessedInput object with normalized data
    """
    if source_type == 'readme':
        content = read_readme(raw_input)
        return ProcessedInput(
            description=content,
            files=[],
            dependencies={},
            source_type='readme',
            raw_content=content
        )
    
    elif source_type == 'directory':
        dir_info = read_directory(raw_input)
        # Try to read README if exists
        description = ""
        try:
            description = read_readme(raw_input)
        except FileNotFoundError:
            description = f"Project directory: {raw_input}"
        
        return ProcessedInput(
            description=description,
            files=dir_info['all_files'],
            dependencies={},  # Will be populated by stack detector
            source_type='directory',
            raw_content=None
        )
    
    elif source_type == 'text':
        text_info = extract_text_input(raw_input)
        return ProcessedInput(
            description=text_info['description'],
            files=[],
            dependencies={},
            source_type='text',
            raw_content=raw_input
        )
    
    else:
        raise ValueError(f"Unknown source_type: {source_type}")
