"""
Metrics Collector Module
Collects usage and performance metrics.
"""

import json
import os
from datetime import datetime
from typing import Dict


class MetricsCollector:
    """Collects and stores metrics."""
    
    def __init__(self, metrics_file: str = 'logs/metrics.json'):
        """Initialize metrics collector."""
        self.metrics_file = metrics_file
        os.makedirs(os.path.dirname(metrics_file), exist_ok=True)
        self.metrics = self._load_metrics()
    
    def _load_metrics(self) -> Dict:
        """Load existing metrics."""
        if os.path.exists(self.metrics_file):
            with open(self.metrics_file, 'r') as f:
                return json.load(f)
        return {
            'total_generations': 0,
            'successful_generations': 0,
            'failed_generations': 0,
            'total_validations': 0,
            'validation_passes': 0,
            'validation_failures': 0,
            'stacks': {},
            'avg_generation_time': 0
        }
    
    def record_generation(self, duration: float, success: bool, stack: str = 'unknown'):
        """Record generation metrics."""
        self.metrics['total_generations'] += 1
        if success:
            self.metrics['successful_generations'] += 1
        else:
            self.metrics['failed_generations'] += 1
        
        # Update stack count
        if stack not in self.metrics['stacks']:
            self.metrics['stacks'][stack] = 0
        self.metrics['stacks'][stack] += 1
        
        # Update average time
        total = self.metrics['total_generations']
        current_avg = self.metrics['avg_generation_time']
        self.metrics['avg_generation_time'] = (current_avg * (total - 1) + duration) / total
        
        self._save_metrics()
    
    def record_validation(self, passed: bool):
        """Record validation metrics."""
        self.metrics['total_validations'] += 1
        if passed:
            self.metrics['validation_passes'] += 1
        else:
            self.metrics['validation_failures'] += 1
        
        self._save_metrics()
    
    def get_summary(self) -> Dict:
        """Get metrics summary."""
        return {
            'total_generations': self.metrics['total_generations'],
            'success_rate': self.metrics['successful_generations'] / max(1, self.metrics['total_generations']),
            'validation_pass_rate': self.metrics['validation_passes'] / max(1, self.metrics['total_validations']),
            'avg_generation_time': self.metrics['avg_generation_time'],
            'most_used_stack': max(self.metrics['stacks'].items(), key=lambda x: x[1])[0] if self.metrics['stacks'] else 'none'
        }
    
    def _save_metrics(self):
        """Save metrics to file."""
        with open(self.metrics_file, 'w') as f:
            json.dump(self.metrics, f, indent=2)


# Global metrics collector
_metrics_collector = None


def get_metrics_collector() -> MetricsCollector:
    """Get global metrics collector."""
    global _metrics_collector
    if _metrics_collector is None:
        _metrics_collector = MetricsCollector()
    return _metrics_collector
