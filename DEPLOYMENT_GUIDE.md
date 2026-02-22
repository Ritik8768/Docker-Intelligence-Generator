# 🚀 DEPLOYMENT GUIDE

## Project Location
```
/home/ritik/Desktop/My_Project/Docker Intelligence Generator/
```

## 📁 Folder Structure

```
Docker Intelligence Generator/
├── src/                    # Application source code (15 modules)
│   ├── input_processor.py
│   ├── stack_detector.py
│   ├── prompt_builder.py
│   ├── ollama_client.py
│   ├── rule_engine.py
│   ├── syntax_validator.py
│   ├── output_formatter.py
│   ├── main.py
│   ├── service_detector.py
│   ├── dependency_analyzer.py
│   ├── compose_builder.py
│   ├── config_loader.py
│   ├── audit_logger.py
│   ├── explainability_engine.py
│   └── metrics_collector.py
├── config/                 # Configuration files
│   ├── app_config.yaml
│   ├── rules.yaml
│   └── prompts/
├── templates/              # Web UI templates
│   └── index.html
├── logs/                   # Application logs
├── web_ui.py              # Flask web application
├── requirements.txt       # Python dependencies
├── Dockerfile             # Production-ready container image
├── docker-compose.yml     # Container orchestration
├── deploy.sh              # Deployment script
├── .dockerignore          # Docker ignore file
└── README.md              # Documentation

```

## 🐳 DEPLOYMENT OPTIONS

### Option 1: Docker Compose (Recommended)

```bash
cd "/home/ritik/Desktop/My_Project/Docker Intelligence Generator"

# Deploy
./deploy.sh

# Or manually
docker-compose up -d
```

### Option 2: Docker Only

```bash
cd "/home/ritik/Desktop/My_Project/Docker Intelligence Generator"

# Build
docker build -t docker-intelligence-generator .

# Run
docker run -d \
  -p 5000:5000 \
  -v $(pwd)/logs:/app/logs \
  --name docker-intelligence-generator \
  docker-intelligence-generator
```

### Option 3: Local Development

```bash
cd "/home/ritik/Desktop/My_Project/Docker Intelligence Generator"

# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run
python web_ui.py
```

## 🔧 MANAGEMENT COMMANDS

### Start Application
```bash
docker-compose up -d
```

### Stop Application
```bash
docker-compose down
```

### View Logs
```bash
docker-compose logs -f
```

### Restart
```bash
docker-compose restart
```

### Rebuild
```bash
docker-compose up -d --build
```

### Check Status
```bash
docker-compose ps
```

## 🌐 ACCESS

**Local:** http://localhost:4000  
**Network:** http://YOUR_IP:4000

## 📊 CONTAINER DETAILS

**Image:** Multi-stage Alpine-based  
**Size:** ~150MB  
**User:** Non-root (appuser)  
**Port:** 5000  
**Resources:** 1GB RAM limit, 1 CPU  
**Health Check:** Every 30s  
**Restart Policy:** unless-stopped  

## 🔒 SECURITY FEATURES

✅ Multi-stage build  
✅ Non-root user  
✅ Minimal Alpine base  
✅ No hardcoded secrets  
✅ Health checks enabled  
✅ Resource limits set  
✅ Read-only config mount  

## 📝 CONFIGURATION

Edit `config/app_config.yaml`:
```yaml
model:
  name: llama3.2:3b
  timeout: 60
  
logging:
  level: INFO
  file: logs/app.log
```

## 🧪 TESTING

### Test Container Build
```bash
docker build -t test-build .
```

### Test Application
```bash
curl http://localhost:5000
```

### Test API
```bash
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Python Flask API"}'
```

## 📈 MONITORING

### View Logs
```bash
tail -f logs/app.log
tail -f logs/audit.log
tail -f logs/metrics.json
```

### Container Stats
```bash
docker stats docker-intelligence-generator
```

### Health Check
```bash
docker inspect --format='{{.State.Health.Status}}' docker-intelligence-generator
```

## 🔄 UPDATES

### Update Application
```bash
# Stop container
docker-compose down

# Update code
git pull  # or copy new files

# Rebuild and restart
docker-compose up -d --build
```

## 🐛 TROUBLESHOOTING

### Container won't start
```bash
docker-compose logs
```

### Port already in use
```bash
# Change port in docker-compose.yml
ports:
  - "8080:5000"  # Use 8080 instead
```

### Permission issues
```bash
chmod -R 755 logs/
```

### Rebuild from scratch
```bash
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

## 📦 BACKUP

### Backup Configuration
```bash
tar -czf config-backup.tar.gz config/
```

### Backup Logs
```bash
tar -czf logs-backup.tar.gz logs/
```

## 🚀 PRODUCTION CHECKLIST

- [ ] Ollama is running and accessible
- [ ] Port 5000 is available
- [ ] Docker and Docker Compose installed
- [ ] Sufficient resources (1GB RAM, 1 CPU)
- [ ] Logs directory has write permissions
- [ ] Configuration files are present
- [ ] Network connectivity verified

## 📞 SUPPORT

**Documentation:** `/Documention/` folder  
**Logs:** `logs/` directory  
**Configuration:** `config/` directory

---

**✅ Your application is ready for deployment!**
