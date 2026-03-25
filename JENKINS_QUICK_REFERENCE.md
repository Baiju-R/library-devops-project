# Jenkins CI/CD - Quick Reference Card

## 🚀 Quick Start

### 1. Start Jenkins
```bash
# Windows
java -jar jenkins.war --httpPort=8080

# Linux/Mac
sudo systemctl start jenkins
```

Access: **http://localhost:8080**

### 2. Create Pipeline Job
1. New Item → Pipeline
2. Name: `library-management-system-pipeline`
3. Pipeline from SCM → Git
4. Repository URL: `<your-git-repo-url>`
5. Script Path: `Jenkinsfile`
6. Save

### 3. Run Build
Click **"Build Now"** → Watch pipeline execute

---

## 📊 Pipeline Stages Overview

| Stage | Duration | Purpose |
|-------|----------|---------|
| 1. Environment Check | ~10s | Verify tools (Docker, Git) |
| 2. Checkout | ~15s | Clone from Git |
| 3. Code Analysis | ~20s | Code quality check |
| 4. Cleanup | ~30s | Remove old containers |
| 5. Build | ~2-5min | Build Docker images |
| 6. Unit Tests | ~45s | Run Python tests |
| 7. Security Scan | ~15s | Check for vulnerabilities |
| 8. Deploy | ~45s | Start all services |
| 9. Health Check | ~30s | Verify endpoints |
| 10. Integration Tests | ~20s | E2E testing |
| 11. Performance Test | ~15s | Response time |
| 12. Tag & Archive | ~10s | Version images |
| 13. Documentation | ~5s | Generate report |

**Total: ~6-10 minutes**

---

## 🔧 Common Commands

### Jenkins
```bash
# Start
java -jar jenkins.war

# Stop
Ctrl+C or kill <jenkins-pid>

# Restart
sudo systemctl restart jenkins
```

### Docker
```bash
# View containers
docker-compose ps

# View logs
docker-compose logs -f

# Stop all
docker-compose down

# Clean rebuild
docker-compose down -v && docker-compose up -d --build
```

### Git
```bash
# Check status
git status

# Commit changes
git add .
git commit -m "Update code"
git push origin main

# View branches
git branch -a
```

---

## ✅ Health Checks

### Application Endpoints
- **Home**: http://localhost:8090/
- **Books**: http://localhost:8090/books/
- **Search**: http://localhost:8090/books/search?keyword=test

### Quick Test
```bash
# Test home page
curl -f http://localhost:8090/

# Test books page
curl -f http://localhost:8090/books/

# Check MySQL
docker exec library_mysql mysql -uroot -proot -e "SHOW DATABASES;"
```

---

## 🐛 Troubleshooting

### Build Failed at Stage X

#### Docker Permission Denied
```bash
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

#### Port Already in Use
```bash
docker-compose down
# Or change port in docker-compose.yml
```

#### MySQL Not Ready
- Increase sleep time in Unit Tests stage
- Check logs: `docker logs library_mysql`

#### Git Checkout Failed
- Verify repository URL
- Check credentials in Jenkins
- Ensure network access

### Check Logs
```bash
# Jenkins logs
tail -f ~/.jenkins/logs/*.log

# Container logs
docker-compose logs flask
docker-compose logs nginx
docker-compose logs mysql

# All logs
docker-compose logs -f --tail=100
```

---

## 📧 Notifications (Optional)

### Email Setup
1. Manage Jenkins → Configure System
2. E-mail Notification → SMTP Server
3. Test configuration
4. Uncomment email sections in Jenkinsfile

### Slack Setup
1. Install Slack Notification Plugin
2. Get Slack webhook URL
3. Configure in Jenkins
4. Add to Jenkinsfile post section

---

## 🎯 Best Practices

### ✅ DO:
- Commit Jenkinsfile to repository
- Use Git tags for releases
- Review failed builds promptly
- Keep Jenkins and plugins updated
- Backup Jenkins home directory regularly

### ❌ DON'T:
- Commit secrets to Git
- Skip test stages
- Ignore security warnings
- Run without health checks
- Deploy without testing

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `Jenkinsfile` | Pipeline definition |
| `JENKINS_SETUP.md` | Complete setup guide |
| `docker-compose.yml` | Service configuration |
| `Dockerfile` | Flask app image |
| `.gitignore` | Exclude files from Git |
| `test_books.py` | Unit tests |
| `info.md` | Complete change log |

---

## 🔄 Deployment Flow

```
Developer Push → GitHub → Webhook → Jenkins
                                      ↓
                              Checkout Code
                                      ↓
                            Build Docker Image
                                      ↓
                              Run Tests
                                      ↓
                            Deploy Services
                                      ↓
                           Verify Health
                                      ↓
                         SUCCESS ✅ / FAIL ❌
                                      ↓
                           Send Notification
```

---

## 📱 Monitoring

### Jenkins Dashboard
- **Build History**: Left sidebar
- **Console Output**: Click build number
- **Blue Ocean**: Better visualization
- **Stage View**: Pipeline progress

### Container Status
```bash
# All containers
docker-compose ps

# Resource usage
docker stats

# Health status
docker inspect library_flask | grep -i health
```

---

## 🆘 Emergency Commands

### Stop Everything
```bash
docker-compose down -v
docker system prune -a
```

### Force Rebuild
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Reset Jenkins Job
1. Delete workspace
2. Restart build
3. Check "Clean before checkout"

---

## 📞 Support

- **Jenkins Docs**: https://jenkins.io/doc/
- **Docker Docs**: https://docs.docker.com/
- **Full Guide**: See `JENKINS_SETUP.md`
- **Changes**: See `info.md`

---

## ⚡ Quick Test Script

```bash
#!/bin/bash
# Save as test-deployment.sh

echo "Testing deployment..."

# Test endpoints
curl -f http://localhost:8090/ && echo "✅ Home OK" || echo "❌ Home FAILED"
curl -f http://localhost:8090/books/ && echo "✅ Books OK" || echo "❌ Books FAILED"

# Check containers
docker-compose ps | grep "Up" && echo "✅ Containers OK" || echo "❌ Containers FAILED"

# Check MySQL
docker exec library_mysql mysql -uroot -proot -e "SHOW DATABASES;" | grep lms && echo "✅ MySQL OK" || echo "❌ MySQL FAILED"

echo "Testing complete!"
```

---

**Remember**: Always backup before major changes! 🔒
