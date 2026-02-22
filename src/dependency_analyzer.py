"""
Dependency Analyzer Module
Analyzes service dependencies.
"""

from typing import List, Dict
from src.service_detector import Service


def analyze_dependencies(services: List[Service]) -> Dict[str, List[str]]:
    """
    Analyze dependencies between services.
    
    Args:
        services: List of Service objects
        
    Returns:
        Dictionary mapping service names to their dependencies
    """
    dependencies = {}
    
    for service in services:
        deps = []
        
        # Web services typically depend on databases and caches
        if service.type == 'web':
            for other in services:
                if other.type in ['database', 'cache']:
                    deps.append(other.name)
        
        dependencies[service.name] = deps
    
    return dependencies


def validate_no_circular_deps(dependencies: Dict[str, List[str]]) -> bool:
    """
    Check for circular dependencies.
    
    Args:
        dependencies: Dependency graph
        
    Returns:
        True if no circular dependencies
    """
    def has_cycle(node, visited, rec_stack):
        visited.add(node)
        rec_stack.add(node)
        
        for neighbor in dependencies.get(node, []):
            if neighbor not in visited:
                if has_cycle(neighbor, visited, rec_stack):
                    return True
            elif neighbor in rec_stack:
                return True
        
        rec_stack.remove(node)
        return False
    
    visited = set()
    for node in dependencies:
        if node not in visited:
            if has_cycle(node, visited, set()):
                return False
    
    return True


def determine_startup_order(dependencies: Dict[str, List[str]]) -> List[str]:
    """
    Determine service startup order based on dependencies.
    
    Args:
        dependencies: Dependency graph
        
    Returns:
        List of service names in startup order
    """
    # Services with no dependencies start first
    no_deps = [node for node in dependencies if not dependencies[node]]
    has_deps = [node for node in dependencies if dependencies[node]]
    
    return no_deps + has_deps
