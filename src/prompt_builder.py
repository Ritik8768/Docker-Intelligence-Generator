"""
Prompt Builder Module
Constructs prompts for LLM with context and security rules.
"""

import os
from typing import Optional


def load_template(stack_name: str) -> str:
    """
    Load prompt template for specified stack.
    
    Args:
        stack_name: Name of stack (python, nodejs, java)
        
    Returns:
        Template content as string
        
    Raises:
        FileNotFoundError: If template file not found
    """
    # Map stack names to template files
    template_map = {
        'python': 'python_template.txt',
        'nodejs': 'nodejs_template.txt',
        'java': 'java_template.txt',
        'unknown': 'base_template.txt'
    }
    
    template_file = template_map.get(stack_name.lower(), 'base_template.txt')
    
    # Get template path relative to this file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    template_path = os.path.join(project_root, 'config', 'prompts', template_file)
    
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template not found: {template_path}")
    
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()


def build_prompt(stack_info, input_data) -> str:
    """
    Build complete prompt with context.
    
    Args:
        stack_info: StackInfo object with detected stack
        input_data: ProcessedInput object with input details
        
    Returns:
        Complete prompt string ready for LLM
    """
    # Load appropriate template
    template = load_template(stack_info.name)
    
    # Extract information
    framework = stack_info.framework or 'Not specified'
    description = getattr(input_data, 'description', 'No description provided')
    
    # Determine dependencies
    dependencies = 'See project files'
    if hasattr(input_data, 'files') and input_data.files:
        dep_files = [f for f in input_data.files if any(
            dep in f for dep in ['requirements.txt', 'package.json', 'pom.xml', 'build.gradle']
        )]
        if dep_files:
            dependencies = ', '.join(dep_files)
    
    # Determine ports (default based on framework)
    ports = _get_default_ports(stack_info.name, framework)
    
    # Inject variables into template
    prompt = template.format(
        stack_name=stack_info.name,
        framework=framework,
        dependencies=dependencies,
        ports=ports,
        description=description[:500]  # Limit description length
    )
    
    return prompt


def _get_default_ports(stack: str, framework: Optional[str]) -> str:
    """
    Get default ports for stack/framework.
    
    Args:
        stack: Stack name
        framework: Framework name
        
    Returns:
        Port string
    """
    port_map = {
        'Flask': '5000',
        'FastAPI': '8000',
        'Django': '8000',
        'Express': '3000',
        'NestJS': '3000',
        'Spring Boot': '8080'
    }
    
    if framework and framework in port_map:
        return port_map[framework]
    
    # Default ports by stack
    if stack == 'python':
        return '8000'
    elif stack == 'nodejs':
        return '3000'
    elif stack == 'java':
        return '8080'
    
    return '8080'


def inject_security_rules(prompt: str) -> str:
    """
    Inject security rules into prompt (already in templates).
    
    Args:
        prompt: Prompt string
        
    Returns:
        Prompt with security rules emphasized
    """
    # Security rules are already in templates
    # This function can add additional emphasis if needed
    return prompt


def format_for_model(prompt: str) -> str:
    """
    Format prompt for model consumption.
    
    Args:
        prompt: Raw prompt string
        
    Returns:
        Formatted prompt
    """
    # Clean up extra whitespace
    lines = [line.rstrip() for line in prompt.split('\n')]
    formatted = '\n'.join(lines)
    
    # Ensure no trailing whitespace
    return formatted.strip()
