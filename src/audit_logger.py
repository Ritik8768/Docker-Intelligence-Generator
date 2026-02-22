"""
Audit Logger Module
Comprehensive audit logging for all operations.
"""

import json
import os
from datetime import datetime
from typing import Dict, Any


class AuditLogger:
    """Audit logger for tracking all operations."""
    
    def __init__(self, log_file: str = 'logs/audit.log'):
        """Initialize audit logger."""
        self.log_file = log_file
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    def log_generation(self, input_data: Dict, output: str, metadata: Dict):
        """Log Dockerfile generation."""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'event_type': 'generation',
            'input': {
                'type': input_data.get('type', 'unknown'),
                'stack': input_data.get('stack', 'unknown')
            },
            'output': {
                'size': len(output),
                'lines': output.count('\n')
            },
            'metadata': metadata
        }
        self._write_log(entry)
    
    def log_validation(self, result: Dict, metadata: Dict):
        """Log validation result."""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'event_type': 'validation',
            'result': result,
            'metadata': metadata
        }
        self._write_log(entry)
    
    def log_error(self, error: str, context: Dict):
        """Log error."""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'event_type': 'error',
            'error': error,
            'context': context
        }
        self._write_log(entry)
    
    def _write_log(self, entry: Dict[str, Any]):
        """Write log entry to file."""
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(entry) + '\n')


# Global audit logger instance
_audit_logger = None


def get_audit_logger() -> AuditLogger:
    """Get global audit logger instance."""
    global _audit_logger
    if _audit_logger is None:
        _audit_logger = AuditLogger()
    return _audit_logger
