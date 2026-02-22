"""
Explainability Engine Module
Generates explanations for AI decisions.
"""

from typing import Dict, List


def explain_dockerfile(dockerfile: str, stack: str) -> str:
    """
    Generate explanation for Dockerfile decisions.
    
    Args:
        dockerfile: Generated Dockerfile content
        stack: Detected stack
        
    Returns:
        Human-readable explanation
    """
    explanations = []
    
    # Explain base image
    if 'alpine' in dockerfile.lower():
        explanations.append(
            "Base Image: Alpine Linux\n"
            "Reason: Minimal attack surface (5-10MB vs 100MB+)\n"
            "Rule: SEC-002 (Minimal base image required)\n"
        )
    
    # Explain user
    if 'USER' in dockerfile:
        explanations.append(
            "User: Non-root user\n"
            "Reason: Running as root violates security best practices\n"
            "Rule: SEC-001 (Non-root user required)\n"
            "Impact: Limits damage if container is compromised\n"
        )
    
    # Explain ports
    if 'EXPOSE' in dockerfile:
        explanations.append(
            "Ports: Explicitly exposed\n"
            "Reason: Only necessary ports should be accessible\n"
            "Rule: SEC-003 (Explicit port exposure)\n"
        )
    
    # Explain multi-stage
    if dockerfile.count('FROM') >= 2:
        explanations.append(
            "Build: Multi-stage\n"
            "Reason: Separates build dependencies from runtime\n"
            "Rule: SEC-005 (Multi-stage builds recommended)\n"
            "Benefit: Smaller final image size\n"
        )
    
    return "\n".join(explanations)


def generate_explanation_report(dockerfile: str, validation_result, stack: str) -> str:
    """Generate complete explanation report."""
    report = "=== DOCKERFILE EXPLANATION ===\n\n"
    report += explain_dockerfile(dockerfile, stack)
    report += "\n\n=== SECURITY VALIDATION ===\n"
    report += f"Status: {'PASSED' if validation_result.passed else 'FAILED'}\n"
    report += f"Summary: {validation_result.summary}\n"
    
    return report
