"""
Main CLI Module
Command-line interface for Dockerfile generation.
"""

import click
import sys
from src.input_processor import normalize_input
from src.stack_detector import detect_stack
from src.prompt_builder import build_prompt
from src.ollama_client import OllamaClient
from src.rule_engine import validate_dockerfile
from src.syntax_validator import validate_syntax
from src.output_formatter import format_dockerfile, format_validation_report


@click.group()
def cli():
    """Production Ready Docker Intelligence Generator"""
    pass


@cli.command()
@click.option('--input', '-i', help='Input directory or README path')
@click.option('--text', '-t', help='Text description')
@click.option('--output', '-o', default='Dockerfile', help='Output file path')
def generate(input, text, output):
    """Generate Dockerfile from input."""
    try:
        # Step 1: Process input
        if text:
            input_data = normalize_input(text, source_type='text')
        elif input:
            input_data = normalize_input(input, source_type='directory')
        else:
            click.echo("Error: Provide --input or --text", err=True)
            sys.exit(1)
        
        click.echo("✓ Input processed")
        
        # Step 2: Detect stack
        stack_info = detect_stack(input_data)
        click.echo(f"✓ Stack detected: {stack_info.name}")
        
        # Step 3: Build prompt
        prompt = build_prompt(stack_info, input_data)
        click.echo("✓ Prompt built")
        
        # Step 4: Generate with Ollama
        click.echo("⏳ Generating Dockerfile...")
        client = OllamaClient()
        
        if not client.health_check():
            click.echo("Error: Ollama not available", err=True)
            sys.exit(1)
        
        dockerfile_content = client.generate(prompt)
        click.echo("✓ Dockerfile generated")
        
        # Step 5: Validate
        syntax_result = validate_syntax(dockerfile_content)
        if not syntax_result.valid:
            click.echo("Warning: Syntax issues detected", err=True)
            for error in syntax_result.errors:
                click.echo(f"  - {error}", err=True)
        
        validation_result = validate_dockerfile(dockerfile_content)
        click.echo(f"✓ Validation: {validation_result.summary}")
        
        # Step 6: Format and save
        formatted = format_dockerfile(dockerfile_content, validation_result)
        
        with open(output, 'w') as f:
            f.write(formatted)
        
        click.echo(f"✓ Dockerfile saved to: {output}")
        
        # Show validation report
        click.echo(format_validation_report(validation_result))
        
        if not validation_result.passed:
            click.echo("\n⚠ Warning: Some security checks failed", err=True)
            sys.exit(1)
        
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--input', '-i', required=True, help='Input directory')
@click.option('--output', '-o', default='docker-compose.yml', help='Output file')
def compose(input, output):
    """Generate docker-compose.yml from input."""
    try:
        import yaml
        from src.service_detector import detect_services
        from src.dependency_analyzer import analyze_dependencies
        from src.compose_builder import build_compose
        
        # Process input
        input_data = normalize_input(input, source_type='directory')
        click.echo("✓ Input processed")
        
        # Detect services
        services = detect_services(input_data)
        click.echo(f"✓ Services detected: {len(services)}")
        
        # Analyze dependencies
        dependencies = analyze_dependencies(services)
        click.echo("✓ Dependencies analyzed")
        
        # Build compose
        compose_dict = build_compose(services, dependencies)
        
        # Save to file
        with open(output, 'w') as f:
            yaml.dump(compose_dict, f, default_flow_style=False, sort_keys=False)
        
        click.echo(f"✓ Compose file saved to: {output}")
        
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--file', '-f', required=True, help='Dockerfile path')
def validate(file):
    """Validate existing Dockerfile."""
    try:
        with open(file, 'r') as f:
            content = f.read()
        
        # Syntax validation
        syntax_result = validate_syntax(content)
        if not syntax_result.valid:
            click.echo("Syntax Errors:")
            for error in syntax_result.errors:
                click.echo(f"  ✗ {error}")
        
        # Security validation
        validation_result = validate_dockerfile(content)
        click.echo(format_validation_report(validation_result))
        
        if validation_result.passed:
            click.echo("\n✓ All security checks passed")
        else:
            click.echo("\n✗ Some security checks failed")
            sys.exit(1)
            
    except FileNotFoundError:
        click.echo(f"Error: File not found: {file}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
def version():
    """Show version information."""
    click.echo("Production Ready Docker Intelligence Generator v1.0.0")
    click.echo("Phase 1: Dockerfile Generator")


if __name__ == '__main__':
    cli()
