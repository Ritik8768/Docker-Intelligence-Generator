"""
Stack Detector Module
Identifies technology stack from project files.
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class StackInfo:
    """Information about detected technology stack."""
    name: str
    framework: Optional[str]
    confidence: float
    files: List[str]


def detect_python(files: List[str]) -> bool:
    """
    Check if project is Python-based.
    
    Args:
        files: List of file paths
        
    Returns:
        True if Python stack detected
    """
    python_indicators = [
        'requirements.txt',
        'setup.py',
        'pyproject.toml',
        'Pipfile',
        'poetry.lock'
    ]
    return any(any(indicator in f for indicator in python_indicators) for f in files)


def detect_nodejs(files: List[str]) -> bool:
    """
    Check if project is Node.js-based.
    
    Args:
        files: List of file paths
        
    Returns:
        True if Node.js stack detected
    """
    nodejs_indicators = [
        'package.json',
        'package-lock.json',
        'yarn.lock',
        'pnpm-lock.yaml'
    ]
    return any(any(indicator in f for indicator in nodejs_indicators) for f in files)


def detect_java(files: List[str]) -> bool:
    """
    Check if project is Java-based.
    
    Args:
        files: List of file paths
        
    Returns:
        True if Java stack detected
    """
    java_indicators = [
        'pom.xml',
        'build.gradle',
        'build.gradle.kts',
        'gradlew'
    ]
    return any(any(indicator in f for indicator in java_indicators) for f in files)


def get_framework(stack: str, files: List[str]) -> str:
    """
    Identify framework within stack.
    
    Args:
        stack: Stack name (python, nodejs, java)
        files: List of file paths
        
    Returns:
        Framework name or 'unknown'
    """
    if stack == 'python':
        # Check for common Python frameworks
        file_content_lower = ' '.join(files).lower()
        if 'flask' in file_content_lower:
            return 'Flask'
        elif 'fastapi' in file_content_lower:
            return 'FastAPI'
        elif 'django' in file_content_lower:
            return 'Django'
        return 'unknown'
    
    elif stack == 'nodejs':
        file_content_lower = ' '.join(files).lower()
        if 'express' in file_content_lower:
            return 'Express'
        elif 'nest' in file_content_lower:
            return 'NestJS'
        elif 'next' in file_content_lower:
            return 'Next.js'
        return 'unknown'
    
    elif stack == 'java':
        file_content_lower = ' '.join(files).lower()
        if 'spring' in file_content_lower or 'springboot' in file_content_lower:
            return 'Spring Boot'
        return 'unknown'
    
    return 'unknown'


def detect_stack(input_data) -> StackInfo:
    """
    Detect technology stack from input data.
    
    Args:
        input_data: ProcessedInput object or dict with 'files' key
        
    Returns:
        StackInfo object with detection results
    """
    # Extract files list
    if hasattr(input_data, 'files'):
        files = input_data.files
    elif isinstance(input_data, dict) and 'files' in input_data:
        files = input_data['files']
    else:
        files = []
    
    # Priority order: Python > Node.js > Java
    detected_stacks = []
    
    if detect_python(files):
        detected_stacks.append(('python', 0.9))
    
    if detect_nodejs(files):
        detected_stacks.append(('nodejs', 0.85))
    
    if detect_java(files):
        detected_stacks.append(('java', 0.8))
    
    # If no stack detected
    if not detected_stacks:
        return StackInfo(
            name='unknown',
            framework=None,
            confidence=0.0,
            files=[]
        )
    
    # Use highest priority (first in list)
    stack_name, confidence = detected_stacks[0]
    framework = get_framework(stack_name, files)
    
    # Find relevant files
    relevant_files = [f for f in files if any(
        indicator in f for indicator in [
            'requirements.txt', 'package.json', 'pom.xml',
            'setup.py', 'build.gradle', '.py', '.js', '.java'
        ]
    )]
    
    return StackInfo(
        name=stack_name,
        framework=framework if framework != 'unknown' else None,
        confidence=confidence,
        files=relevant_files[:10]  # Limit to first 10 relevant files
    )
