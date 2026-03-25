# Library Management System 📚

A production-ready Flask application with complete CI/CD pipeline for managing users and books, backed by MySQL and served through Nginx.

![Libray Management App - Flask](https://github.com/hamzaavvan/library-management-system/blob/master/ss/ss2.JPG?raw=true)

## 🔧 Technology Stack

- **Backend**: Python 3.10 + Flask 2.3.2
- **Database**: MySQL 5.7
- **Web Server**: Nginx (Reverse Proxy)
- **App Server**: Gunicorn (4 workers)
- **Container**: Docker + Docker Compose
- **CI/CD**: Jenkins Pipeline (13 stages)


## Installation

To run the app flawlessly, satisfy the requirements
```bash
$ pip install -r requirements.txt
```

## Set Environment Variables
```bash
$ export FLASK_APP=app.py
$ export FLASk_ENV=development
```

## Start Server
```bash
$ flask run
```

Or run this command 
```bash
$ python -m flask run
```

---

## 🚀 CI/CD with Jenkins

This project includes a complete Jenkins CI/CD pipeline for automated building, testing, and deployment.

### Quick Start

1. **Install Jenkins**: Download from [jenkins.io](https://www.jenkins.io/download/)
2. **Start Jenkins**: `java -jar jenkins.war --httpPort=8080`
3. **Create Pipeline**: New Item → Pipeline → Configure Git repo → Point to Jenkinsfile
4. **Build**: Click "Build Now" and watch the magic happen! ✨

### Pipeline Features

- ✅ **13 Automated Stages** - From checkout to deployment
- ✅ **Complete Testing** - Unit, integration, and performance tests
- ✅ **Security Scanning** - Automated vulnerability checks
- ✅ **Health Monitoring** - Automatic health verification
- ✅ **Auto Rollback** - Rolls back on failure
- ✅ **Build Artifacts** - Reports and tagged Docker images

### Documentation

- 📖 **[GETTING_STARTED.md](GETTING_STARTED.md)** - 30-minute setup guide
- 📖 **[JENKINS_SETUP.md](JENKINS_SETUP.md)** - Complete installation guide  
- 📖 **[JENKINS_QUICK_REFERENCE.md](JENKINS_QUICK_REFERENCE.md)** - Command cheat sheet
- 📖 **[info.md](info.md)** - Complete change log

### Pipeline Stages

1. Environment Check → 2. Checkout → 3. Code Analysis → 4. Cleanup → 5. Build →
6. Unit Tests → 7. Security Scan → 8. Deploy → 9. Health Check →
10. Integration Tests → 11. Performance Test → 12. Tag & Archive → 13. Documentation

**Total build time**: ~6-10 minutes

### Webhook Integration

Set up GitHub webhooks for automatic builds on every push:

```
Payload URL: http://your-jenkins-url:8080/github-webhook/
Content type: application/json
Events: Push events
```

---

## 📊 Monitoring with Prometheus & Grafana

Real-time application monitoring and visualization is now integrated!

### Quick Start

```bash
# Start all services including monitoring
docker-compose up -d

# Or start only monitoring stack
docker-compose up -d prometheus grafana
```

### Access Monitoring Dashboards

| Service | URL | Credentials |
|---------|-----|-------------|
| **Grafana** | http://localhost:3000 | admin / admin |
| **Prometheus** | http://localhost:9090 | None |
| **Flask Metrics** | http://localhost:5000/metrics | None |

### Features

- 📈 **Real-time Metrics**: HTTP request rates, response times, status codes
- 🎯 **Pre-built Dashboards**: Ready-to-use Flask application dashboard
- ⚠️ **Alerting**: Set up custom alerts (optional)
- 📊 **Time-series Data**: Track performance trends over time
- 🔍 **PromQL Queries**: Powerful metric querying language

### Test Monitoring Setup

```bash
# Run monitoring test script
bash monitoring/test-monitoring.sh

# Generate some traffic to see metrics
for i in {1..100}; do curl http://localhost:8090/books/; done
```

### Documentation

See **[monitoring/README.md](monitoring/README.md)** for:
- Detailed configuration guide
- Custom metrics creation
- Troubleshooting tips
- PromQL query examples

---

## 📊 Application Status

- **Docker Containers**: 5 (MySQL, Flask, Nginx, Prometheus, Grafana)
- **Application Port**: 8090
- **MySQL Port**: 3307
- **Prometheus Port**: 9090
- **Grafana Port**: 3000
- **Access**: http://localhost:8090

### Recent Improvements ✨

- ✅ Fixed 502 Bad Gateway with enhanced Nginx configuration
- ✅ Added health check endpoints
- ✅ Implemented comprehensive error handling
- ✅ Pinned Werkzeug 2.3.7 for compatibility with Flask 2.3.2
- ✅ Complete Jenkins CI/CD pipeline with 13 automated stages
- ✅ Docker container conflict resolution in pipeline
- ✅ **NEW**: Prometheus & Grafana monitoring stack
- ✅ **NEW**: Flask metrics exporter with pre-built dashboards

**Last Updated**: 2026-03-25

---

## 📝 License

This project is open source and available for educational purposes.

---

## 🤝 Contributing

Feel free to submit issues and pull requests for improvements!

---
