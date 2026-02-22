"""
Rule Engine Module
Validates Dockerfile against security rules.
"""

import os
import re
import yaml
from dataclasses import dataclass
from typing import List, Callable


@dataclass
class Rule:
    """Security rule definition."""
    id: str
    name: str
    severity: str
    validator: Callable


@dataclass
class RuleResult:
    """Result of a single rule check."""
    rule_id: str
    passed: bool
    message: str
    severity: str


@dataclass
class ValidationResult:
    """Complete validation result."""
    passed: bool
    results: List[RuleResult]
    summary: str


def load_rules(rules_file: str = None) -> List[dict]:
    """Load rules from YAML file."""
    if rules_file is None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        rules_file = os.path.join(project_root, 'config', 'rules.yaml')
    
    with open(rules_file, 'r') as f:
        data = yaml.safe_load(f)
    return data.get('rules', [])


def check_non_root_user(content: str) -> RuleResult:
    """Check if Dockerfile uses non-root user."""
    lines = content.upper().split('\n')
    has_user = any('USER ' in line and 'USER ROOT' not in line for line in lines)
    
    return RuleResult(
        rule_id='SEC-001',
        passed=has_user,
        message='Non-root user found' if has_user else 'No USER instruction or using root',
        severity='ERROR'
    )


def check_minimal_image(content: str) -> RuleResult:
    """Check if using minimal base image."""
    minimal_images = ['alpine', 'distroless', 'slim']
    from_lines = [line for line in content.split('\n') if line.strip().upper().startswith('FROM')]
    
    if not from_lines:
        return RuleResult('SEC-002', False, 'No FROM instruction found', 'ERROR')
    
    has_minimal = any(any(img in line.lower() for img in minimal_images) for line in from_lines)
    
    return RuleResult(
        rule_id='SEC-002',
        passed=has_minimal,
        message='Minimal base image used' if has_minimal else 'Use alpine, slim, or distroless images',
        severity='ERROR'
    )


def check_exposed_ports(content: str) -> RuleResult:
    """Check if ports are explicitly exposed."""
    has_expose = 'EXPOSE' in content.upper()
    
    return RuleResult(
        rule_id='SEC-003',
        passed=has_expose,
        message='Ports explicitly exposed' if has_expose else 'No EXPOSE instruction found',
        severity='ERROR'
    )


def check_no_secrets(content: str) -> RuleResult:
    """Check for hardcoded secrets."""
    secret_patterns = [
        r'password\s*=\s*["\']',
        r'api[_-]?key\s*=\s*["\']',
        r'secret\s*=\s*["\']',
        r'token\s*=\s*["\']',
        r'AWS_SECRET',
        r'PRIVATE_KEY'
    ]
    
    for pattern in secret_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            return RuleResult('SEC-004', False, 'Potential hardcoded secret detected', 'ERROR')
    
    return RuleResult('SEC-004', True, 'No hardcoded secrets detected', 'ERROR')


def check_multi_stage(content: str) -> RuleResult:
    """Check if using multi-stage build."""
    from_count = content.upper().count('FROM ')
    is_multi_stage = from_count >= 2
    
    return RuleResult(
        rule_id='SEC-005',
        passed=is_multi_stage,
        message='Multi-stage build used' if is_multi_stage else 'Consider using multi-stage build',
        severity='WARNING'
    )


def check_healthcheck(content: str) -> RuleResult:
    """Check if healthcheck is defined."""
    has_healthcheck = 'HEALTHCHECK' in content.upper()
    
    return RuleResult(
        rule_id='SEC-006',
        passed=has_healthcheck,
        message='Healthcheck defined' if has_healthcheck else 'Consider adding HEALTHCHECK',
        severity='WARNING'
    )


def validate_dockerfile(content: str, rules: List[dict] = None) -> ValidationResult:
    """Validate Dockerfile against all rules."""
    if rules is None:
        rules = load_rules()
    
    # Map rule IDs to validator functions
    validators = {
        'SEC-001': check_non_root_user,
        'SEC-002': check_minimal_image,
        'SEC-003': check_exposed_ports,
        'SEC-004': check_no_secrets,
        'SEC-005': check_multi_stage,
        'SEC-006': check_healthcheck
    }
    
    results = []
    for rule in rules:
        rule_id = rule['id']
        if rule_id in validators:
            result = validators[rule_id](content)
            results.append(result)
    
    # Check if all ERROR rules passed
    error_results = [r for r in results if r.severity == 'ERROR']
    all_errors_passed = all(r.passed for r in error_results)
    
    # Generate summary
    passed_count = sum(1 for r in results if r.passed)
    failed_count = len(results) - passed_count
    error_count = sum(1 for r in error_results if not r.passed)
    
    summary = f"{passed_count} checks passed, {failed_count} failed"
    if error_count > 0:
        summary += f" ({error_count} critical errors)"
    
    return ValidationResult(
        passed=all_errors_passed,
        results=results,
        summary=summary
    )
