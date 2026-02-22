"""
Web UI Module
Simple Flask-based web interface.
"""

from flask import Flask, render_template, request, jsonify
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.input_processor import normalize_input
from src.stack_detector import detect_stack
from src.prompt_builder import build_prompt
from src.ollama_client import OllamaClient
from src.rule_engine import validate_dockerfile
from src.syntax_validator import validate_syntax

app = Flask(__name__)


@app.route('/')
def index():
    """Main page."""
    return render_template('index.html')


@app.route('/api/generate', methods=['POST'])
def generate():
    """Generate Dockerfile API endpoint."""
    try:
        data = request.json
        prompt_text = data.get('prompt', '')
        
        if not prompt_text:
            return jsonify({'error': 'Prompt is required'}), 400
        
        # Process input
        input_data = normalize_input(prompt_text, source_type='text')
        
        # Detect stack
        stack_info = detect_stack(input_data)
        
        # Build prompt
        prompt = build_prompt(stack_info, input_data)
        
        # Generate with Ollama
        client = OllamaClient()
        
        if not client.health_check():
            return jsonify({'error': 'Ollama not available'}), 503
        
        dockerfile = client.generate(prompt)
        
        # Validate
        syntax_result = validate_syntax(dockerfile)
        validation_result = validate_dockerfile(dockerfile)
        
        return jsonify({
            'success': True,
            'dockerfile': dockerfile,
            'stack': stack_info.name,
            'validation': {
                'passed': validation_result.passed,
                'summary': validation_result.summary,
                'results': [
                    {
                        'rule_id': r.rule_id,
                        'passed': r.passed,
                        'message': r.message,
                        'severity': r.severity
                    }
                    for r in validation_result.results
                ]
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/validate', methods=['POST'])
def validate():
    """Validate Dockerfile API endpoint."""
    try:
        data = request.json
        dockerfile = data.get('dockerfile', '')
        
        if not dockerfile:
            return jsonify({'error': 'Dockerfile content is required'}), 400
        
        # Validate
        syntax_result = validate_syntax(dockerfile)
        validation_result = validate_dockerfile(dockerfile)
        
        return jsonify({
            'success': True,
            'validation': {
                'passed': validation_result.passed,
                'summary': validation_result.summary,
                'results': [
                    {
                        'rule_id': r.rule_id,
                        'passed': r.passed,
                        'message': r.message,
                        'severity': r.severity
                    }
                    for r in validation_result.results
                ]
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
