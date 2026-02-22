"""
Syntax Validator Module
Parses and validates Dockerfile syntax.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class Instruction:
    """Dockerfile instruction."""
    line_number: int
    instruction: str
    arguments: str


@dataclass
class ParsedDockerfile:
    """Parsed Dockerfile structure."""
    instructions: List[Instruction]
    valid: bool
    errors: List[str]


@dataclass
class SyntaxResult:
    """Syntax validation result."""
    valid: bool
    errors: List[str]
    warnings: List[str]


VALID_INSTRUCTIONS = {
    'FROM', 'RUN', 'COPY', 'ADD', 'WORKDIR', 'USER', 'EXPOSE',
    'CMD', 'ENTRYPOINT', 'ENV', 'ARG', 'LABEL', 'HEALTHCHECK',
    'VOLUME', 'ONBUILD', 'STOPSIGNAL', 'SHELL'
}


def parse_dockerfile(content: str) -> ParsedDockerfile:
    """
    Parse Dockerfile content.
    
    Args:
        content: Dockerfile content as string
        
    Returns:
        ParsedDockerfile object
    """
    instructions = []
    errors = []
    lines = content.split('\n')
    
    for i, line in enumerate(lines, 1):
        line = line.strip()
        
        # Skip empty lines and comments
        if not line or line.startswith('#'):
            continue
        
        # Handle line continuations
        while line.endswith('\\'):
            if i < len(lines):
                line = line[:-1] + ' ' + lines[i].strip()
                i += 1
        
        # Parse instruction
        parts = line.split(None, 1)
        if not parts:
            continue
        
        instruction = parts[0].upper()
        arguments = parts[1] if len(parts) > 1 else ''
        
        if instruction not in VALID_INSTRUCTIONS:
            errors.append(f"Line {i}: Invalid instruction '{instruction}'")
        
        instructions.append(Instruction(i, instruction, arguments))
    
    return ParsedDockerfile(
        instructions=instructions,
        valid=len(errors) == 0,
        errors=errors
    )


def validate_syntax(content: str) -> SyntaxResult:
    """
    Validate Dockerfile syntax.
    
    Args:
        content: Dockerfile content
        
    Returns:
        SyntaxResult with validation details
    """
    errors = []
    warnings = []
    
    parsed = parse_dockerfile(content)
    errors.extend(parsed.errors)
    
    if not parsed.instructions:
        errors.append("Dockerfile is empty")
        return SyntaxResult(False, errors, warnings)
    
    # Check FROM is first instruction
    first_instruction = parsed.instructions[0].instruction
    if first_instruction != 'FROM':
        errors.append(f"First instruction must be FROM, found {first_instruction}")
    
    # Check for required instructions
    instruction_names = [i.instruction for i in parsed.instructions]
    
    if 'FROM' not in instruction_names:
        errors.append("Missing FROM instruction")
    
    # Warnings for best practices
    if 'USER' not in instruction_names:
        warnings.append("No USER instruction found (consider adding)")
    
    if 'EXPOSE' not in instruction_names:
        warnings.append("No EXPOSE instruction found (consider adding)")
    
    return SyntaxResult(
        valid=len(errors) == 0,
        errors=errors,
        warnings=warnings
    )


def check_instruction_validity(instruction: str) -> bool:
    """
    Check if instruction name is valid.
    
    Args:
        instruction: Instruction name
        
    Returns:
        True if valid
    """
    return instruction.upper() in VALID_INSTRUCTIONS


def extract_instructions(content: str) -> List[Instruction]:
    """
    Extract all instructions from Dockerfile.
    
    Args:
        content: Dockerfile content
        
    Returns:
        List of Instruction objects
    """
    parsed = parse_dockerfile(content)
    return parsed.instructions
