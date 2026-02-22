"""
Service Detector Module
Identifies services in multi-service applications.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class Service:
    """Service definition."""
    name: str
    type: str  # web, database, cache, queue
    stack: Optional[str]
    ports: List[int]
    dependencies: List[str]
    environment: Dict[str, str]


def identify_web_service(files: List[str]) -> Optional[Service]:
    """Identify web service from files."""
    if any('app.py' in f or 'main.py' in f or 'server.js' in f for f in files):
        return Service(
            name='web',
            type='web',
            stack='detected',
            ports=[8000],
            dependencies=[],
            environment={}
        )
    return None


def identify_database(files: List[str], content: str = '') -> Optional[Service]:
    """Identify database service."""
    db_indicators = {
        'postgres': ['psycopg2', 'postgresql', 'postgres'],
        'mysql': ['mysql', 'pymysql'],
        'mongodb': ['pymongo', 'mongodb'],
        'redis': ['redis']
    }
    
    content_lower = content.lower()
    for db_type, indicators in db_indicators.items():
        if any(ind in content_lower for ind in indicators):
            return Service(
                name=db_type,
                type='database',
                stack=db_type,
                ports=[5432 if db_type == 'postgres' else 3306],
                dependencies=[],
                environment={}
            )
    return None


def identify_cache(files: List[str], content: str = '') -> Optional[Service]:
    """Identify cache service."""
    if 'redis' in content.lower():
        return Service(
            name='redis',
            type='cache',
            stack='redis',
            ports=[6379],
            dependencies=[],
            environment={}
        )
    return None


def detect_services(input_data) -> List[Service]:
    """
    Detect all services in application.
    
    Args:
        input_data: ProcessedInput object
        
    Returns:
        List of detected services
    """
    services = []
    
    # Get files and description
    files = getattr(input_data, 'files', [])
    description = getattr(input_data, 'description', '')
    
    # Detect web service
    web = identify_web_service(files)
    if web:
        services.append(web)
    
    # Detect database
    db = identify_database(files, description)
    if db:
        services.append(db)
    
    # Detect cache
    cache = identify_cache(files, description)
    if cache:
        services.append(cache)
    
    return services
