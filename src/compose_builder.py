"""
Compose Builder Module
Generates docker-compose.yml files.
"""

from typing import List, Dict
from src.service_detector import Service


def generate_service_definition(service: Service) -> Dict:
    """Generate compose service definition."""
    definition = {
        'image': f'{service.stack}:latest' if service.type != 'web' else None,
        'build': '.' if service.type == 'web' else None,
        'ports': [f'{p}:{p}' for p in service.ports] if service.ports else None,
        'environment': service.environment if service.environment else None,
        'depends_on': service.dependencies if service.dependencies else None,
        'networks': ['app_network'],
        'deploy': {
            'resources': {
                'limits': {
                    'cpus': '0.5',
                    'memory': '512M'
                }
            }
        },
        'restart': 'unless-stopped'
    }
    
    # Remove None values
    return {k: v for k, v in definition.items() if v is not None}


def generate_network_config() -> Dict:
    """Generate network configuration."""
    return {
        'app_network': {
            'driver': 'bridge'
        }
    }


def generate_volume_config(services: List[Service]) -> Dict:
    """Generate volume configuration."""
    volumes = {}
    for service in services:
        if service.type == 'database':
            volumes[f'{service.name}_data'] = None
    return volumes


def build_compose(services: List[Service], dependencies: Dict[str, List[str]]) -> Dict:
    """
    Build complete docker-compose structure.
    
    Args:
        services: List of Service objects
        dependencies: Service dependencies
        
    Returns:
        Complete compose dictionary
    """
    # Update service dependencies
    for service in services:
        service.dependencies = dependencies.get(service.name, [])
    
    compose = {
        'version': '3.8',
        'services': {},
        'networks': generate_network_config(),
        'volumes': generate_volume_config(services)
    }
    
    for service in services:
        compose['services'][service.name] = generate_service_definition(service)
    
    return compose
