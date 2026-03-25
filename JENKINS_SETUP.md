# Jenkins CI/CD Setup Guide for Library Management System

## Overview
This guide will help you set up Jenkins CI/CD pipeline for automated building, testing, and deployment of the Library Management System.

## Prerequisites

### 1. Jenkins Installation
- **Download Jenkins**: https://www.jenkins.io/download/
- **Recommended**: Jenkins LTS version 2.x or higher
- **Java**: JDK 11 or higher

### 2. Required Jenkins Plugins
Install these plugins via Jenkins Dashboard → Manage Jenkins → Plugin Manager:
- **Docker Pipeline Plugin**
- **Git Plugin** (usually pre-installed)
- **Pipeline Plugin** (usually pre-installed)
- **Blue Ocean** (optional, for better UI)
- **Email Extension Plugin** (for notifications)

### 3. System Requirements
- Docker and Docker Compose installed on Jenkins server
- Git installed
- Port 8090 available for application
- Port 3307 available for MySQL

## Jenkins Configuration Steps

### Step 1: Start Jenkins

#### On Windows:
```bash
java -jar jenkins.war --httpPort=8080
```

#### On Linux/Mac:
```bash
sudo systemctl start jenkins
# or
java -jar jenkins.war
```

Access Jenkins at: `http://localhost:8080`

### Step 2: Initial Setup
1. Unlock Jenkins using the initial admin password
   - Location shown in console output
   - Usually at: `~/.jenkins/secrets/initialAdminPassword`
2. Install suggested plugins
3. Create first admin user
4. Configure Jenkins URL

### Step 3: Install Required Plugins
1. Go to **Manage Jenkins** → **Plugin Manager**
2. Click **Available** tab
3. Search and install:
   - Docker Pipeline
   - Git Plugin
   - Pipeline
   - Blue Ocean (optional)

### Step 4: Configure Docker Access
Jenkins needs access to Docker daemon:

#### On Linux:
```bash
# Add Jenkins user to docker group
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

#### On Windows:
- Ensure Docker Desktop is running
- Jenkins should have access to Docker commands

### Step 5: Create New Pipeline Job

1. **New Item** → Enter name: `library-management-system-pipeline`
2. Select **Pipeline** project type
3. Click **OK**

### Step 6: Configure Pipeline

#### Option A: Pipeline from SCM (Recommended)
1. In Pipeline section, select **Pipeline script from SCM**
2. **SCM**: Git
3. **Repository URL**: Your Git repository URL
   ```
   https://github.com/yourusername/library-management-system.git
   ```
4. **Branch**: `*/main` or `*/master`
5. **Script Path**: `Jenkinsfile`
6. Save

#### Option B: Direct Pipeline Script
1. In Pipeline section, select **Pipeline script**
2. Copy the entire Jenkinsfile content
3. Paste into the script text area
4. Save

### Step 7: Configure Git Repository

If your repository is private:
1. Go to **Manage Jenkins** → **Credentials**
2. Click **System** → **Global credentials**
3. **Add Credentials**
   - Kind: Username with password
   - Username: Your Git username
   - Password: Personal Access Token (GitHub) or password
   - ID: `git-credentials`
4. Save

### Step 8: Build Triggers (Optional)

Configure automatic builds:

#### Poll SCM:
- In job configuration, check **Poll SCM**
- Schedule: `H/5 * * * *` (checks every 5 minutes)

#### GitHub Webhook:
1. In GitHub repository: Settings → Webhooks → Add webhook
2. Payload URL: `http://your-jenkins-url:8080/github-webhook/`
3. Content type: `application/json`
4. Events: Just push event
5. Active: ✓

### Step 9: Environment Variables (Optional)

If you need custom configuration:
1. Go to **Manage Jenkins** → **Configure System**
2. **Global properties** → **Environment variables**
3. Add variables:
   - `DOCKER_REGISTRY`: Your Docker registry
   - `NOTIFICATION_EMAIL`: Your email

## Running the Pipeline

### Manual Build:
1. Open your pipeline job
2. Click **Build Now**
3. Watch the build progress in **Console Output**

### Pipeline Stages:
1. **Environment Check** - Verify tools are available
2. **Checkout** - Pull code from Git
3. **Code Analysis** - Static code analysis
4. **Cleanup** - Remove old containers
5. **Build** - Build Docker images
6. **Unit Tests** - Run automated tests
7. **Security Scan** - Check for vulnerabilities
8. **Deploy** - Start all services
9. **Health Check** - Verify deployment
10. **Integration Tests** - End-to-end testing
11. **Performance Test** - Basic load testing
12. **Tag & Archive** - Version the build
13. **Documentation** - Generate reports

## Pipeline Features

### ✅ Automated Testing
- Unit tests with Python
- Integration tests for all endpoints
- Health checks for services
- Performance testing

### ✅ Security Scanning
- Checks for hardcoded secrets
- Dockerfile best practices validation
- Dependency scanning

### ✅ Deployment Automation
- Clean deployment with no downtime
- Automatic rollback on failure
- Health verification before completion

### ✅ Build Artifacts
- Deployment reports
- Tagged Docker images
- Build logs

## Monitoring Build Status

### Blue Ocean View (Recommended):
1. Install Blue Ocean plugin
2. Click **Open Blue Ocean** in Jenkins sidebar
3. Visual pipeline view with stage-by-stage progress

### Classic View:
- Build history in left sidebar
- Console output for detailed logs
- Stage View shows pipeline progress

## Troubleshooting

### Common Issues:

#### 1. Docker Permission Denied
```bash
# Solution: Add Jenkins to docker group
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

#### 2. Port Already in Use
```bash
# Solution: Stop existing containers
docker-compose down
# Or change port in docker-compose.yml
```

#### 3. Git Checkout Failed
- Verify repository URL is correct
- Check credentials are configured
- Ensure Jenkins has network access to Git server

#### 4. Build Takes Too Long
- Increase timeout in Jenkinsfile
- Use `--no-cache` flag for clean builds
- Check network speed for image pulls

#### 5. MySQL Not Ready
- Increase wait time in Unit Tests stage
- Check MySQL logs: `docker logs library_mysql`

## Advanced Configuration

### Email Notifications
Add to Jenkinsfile post section:
```groovy
emailext (
    subject: "Build ${env.BUILD_NUMBER} - ${currentBuild.result}",
    body: """
        Build: ${env.BUILD_NUMBER}
        Status: ${currentBuild.result}
        Job: ${env.JOB_NAME}
        URL: ${env.BUILD_URL}
    """,
    to: "your-email@example.com"
)
```

### Slack Notifications
1. Install Slack Notification plugin
2. Configure Slack workspace in Jenkins
3. Add to Jenkinsfile:
```groovy
slackSend (
    color: 'good',
    message: "Build ${env.BUILD_NUMBER} succeeded!"
)
```

### Multi-Branch Pipeline
For multiple branches (dev, staging, prod):
1. Create **Multibranch Pipeline** job
2. Point to Git repository
3. Jenkins auto-discovers branches with Jenkinsfile

## CI/CD Best Practices

### 1. Version Control Everything
- Keep Jenkinsfile in repository
- Track all configuration changes
- Use Git tags for releases

### 2. Fast Feedback
- Run quick tests first
- Parallel stages where possible
- Fail fast on critical issues

### 3. Reproducible Builds
- Use specific version tags
- Lock dependency versions
- Clean build environments

### 4. Security
- Never commit secrets to Git
- Use Jenkins credentials store
- Scan for vulnerabilities

### 5. Documentation
- Keep this guide updated
- Document pipeline changes
- Archive build artifacts

## Maintenance

### Regular Tasks:
- **Weekly**: Review failed builds
- **Monthly**: Update plugins
- **Quarterly**: Review and optimize pipeline

### Backup Jenkins:
```bash
# Backup Jenkins home directory
tar -czf jenkins-backup.tar.gz ~/.jenkins/
```

### Update Jenkins:
1. Backup first!
2. Download new jenkins.war
3. Stop Jenkins
4. Replace jenkins.war
5. Start Jenkins

## Support

### Resources:
- Jenkins Documentation: https://www.jenkins.io/doc/
- Docker Documentation: https://docs.docker.com/
- Pipeline Syntax: https://www.jenkins.io/doc/book/pipeline/syntax/

### Log Locations:
- Jenkins logs: `~/.jenkins/logs/`
- Container logs: `docker-compose logs`
- Build logs: Jenkins UI → Console Output

## Next Steps

1. ✅ Set up Jenkins following this guide
2. ✅ Create pipeline job with Git integration
3. ✅ Run first build and verify success
4. ✅ Configure webhooks for automatic builds
5. ✅ Set up notifications (email/Slack)
6. ✅ Document custom configurations
7. ✅ Train team on using Jenkins

---

**Note**: This CI/CD pipeline is designed for the Library Management System but can be adapted for other projects by modifying the Jenkinsfile stages and configuration.
