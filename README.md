# Docker Intelligence Generator

AI-powered Dockerfile and Docker Compose generator with security validation.

## Quick Start

### Using Docker Compose (Recommended)
```bash
docker-compose up -d
```

Access at: http://localhost:4000

### Using Docker
```bash
docker build -t docker-intelligence-generator .
docker run -d -p 5000:5000 --name docker-intelligence-generator docker-intelligence-generator
```

### Local Development
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python web_ui.py
```

## Features

✅ AI-powered Dockerfile generation  
✅ Docker Compose support  
✅ Security validation (11 rules)  
✅ Web UI interface  
✅ Offline operation  
✅ Multi-stage builds  

## Project Structure

```
Docker Intelligence Generator/
├── src/                    # Application modules
├── config/                 # Configuration files
├── templates/              # Web UI templates
├── logs/                   # Application logs
├── web_ui.py              # Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile             # Container image
└── docker-compose.yml     # Orchestration
```

## Management

### Start
```bash
docker-compose up -d
```

### Stop
```bash
docker-compose down
```

### View Logs
```bash
docker-compose logs -f
```

### Rebuild
```bash
docker-compose up -d --build
```

## Configuration

Edit `config/app_config.yaml` to customize:
- Model settings
- Security rules
- Logging levels

## Security

- Runs as non-root user
- Multi-stage build
- Minimal Alpine base
- Health checks enabled
- Resource limits set

## Requirements

- Docker 20.10+
- Docker Compose 2.0+
- 1GB RAM minimum
- Ollama (for AI generation)

## Support

Documentation: See `/Documention/` folder  
Issues: Contact project team
