# Getting Started with Jenkins CI/CD

## 🎯 Objective
Set up automated CI/CD pipeline for Library Management System using Jenkins.

---

## 📋 Prerequisites Checklist

Before starting, ensure you have:

- [ ] Windows/Linux/Mac with administrator access
- [ ] Java JDK 11 or higher installed
- [ ] Docker Desktop installed and running
- [ ] Git installed and configured
- [ ] Ports 8080 (Jenkins) and 8090 (App) available
- [ ] Internet connection for downloading Jenkins

---

## 🚀 Step-by-Step Setup (30 minutes)

### Step 1: Download Jenkins (5 minutes)

#### Option A: Download Jenkins WAR file
```bash
# Download from https://www.jenkins.io/download/
# Or use wget/curl:
wget https://get.jenkins.io/war-stable/latest/jenkins.war
```

#### Option B: Install Jenkins (Windows)
```bash
# Download installer from https://www.jenkins.io/download/
# Run the installer and follow prompts
```

#### Option C: Install Jenkins (Linux)
```bash
# Ubuntu/Debian
wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo apt-key add -
sudo sh -c 'echo deb https://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
sudo apt-get update
sudo apt-get install jenkins
```

### Step 2: Start Jenkins (2 minutes)

```bash
# Using WAR file
java -jar jenkins.war --httpPort=8080

# Using service (Linux)
sudo systemctl start jenkins
sudo systemctl enable jenkins
```

**Access Jenkins**: Open browser → `http://localhost:8080`

### Step 3: Initial Jenkins Setup (5 minutes)

1. **Unlock Jenkins**
   ```bash
   # Find initial password
   # Linux/Mac: cat ~/.jenkins/secrets/initialAdminPassword
   # Windows: C:\Users\<username>\.jenkins\secrets\initialAdminPassword
   ```
   - Copy the password
   - Paste in browser

2. **Install Plugins**
   - Click "Install suggested plugins"
   - Wait for installation (~3 minutes)

3. **Create Admin User**
   - Username: `admin` (or your choice)
   - Password: (choose a strong password)
   - Full name: Your name
   - Email: your.email@example.com

4. **Configure Jenkins URL**
   - Keep default: `http://localhost:8080/`
   - Click "Save and Finish"
   - Click "Start using Jenkins"

### Step 4: Install Additional Plugins (5 minutes)

1. Go to **Manage Jenkins** → **Plugin Manager**
2. Click **Available** tab
3. Search and install (check boxes):
   - **Docker Pipeline**
   - **Blue Ocean** (optional but recommended)
   - **Email Extension Plugin**
4. Click "Install without restart"
5. Wait for completion

### Step 5: Configure Docker Access (3 minutes)

#### Windows:
- Jenkins should automatically have Docker access
- Verify: Open Jenkins → **Manage Jenkins** → **System Information**
- Look for Docker version

#### Linux:
```bash
# Add Jenkins user to docker group
sudo usermod -aG docker jenkins

# Restart Jenkins
sudo systemctl restart jenkins

# Verify
sudo -u jenkins docker ps
```

### Step 6: Push Code to Git Repository (5 minutes)

1. **Initialize Git** (if not already)
   ```bash
   cd library-management-system-master
   git init
   git add .
   git commit -m "Initial commit with Jenkins CI/CD"
   ```

2. **Create GitHub Repository**
   - Go to https://github.com/new
   - Name: `library-management-system`
   - Public or Private
   - Click "Create repository"

3. **Push to GitHub**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/library-management-system.git
   git branch -M main
   git push -u origin main
   ```

### Step 7: Create Jenkins Pipeline (5 minutes)

1. **New Item**
   - Click "New Item" in Jenkins
   - Name: `library-management-system-pipeline`
   - Type: **Pipeline**
   - Click "OK"

2. **Configure Pipeline**
   - Scroll to **Pipeline** section
   - Definition: **Pipeline script from SCM**
   - SCM: **Git**
   - Repository URL: `https://github.com/YOUR_USERNAME/library-management-system.git`
   - Branch: `*/main`
   - Script Path: `Jenkinsfile`

3. **Save**
   - Click "Save"

### Step 8: Run First Build (10 minutes..)

1. **Start Build**
   - Click "Build Now"
   - Watch progress in Build History

2. **View Pipeline**
   - Click build number (#1)
   - Click "Console Output" for detailed logs
   - Or click "Open Blue Ocean" for visual view

3. **Wait for Completion**
   - Pipeline will run all 13 stages
   - Takes ~6-10 minutes first time
   - Subsequent builds are faster

4. **Verify Success**
   - Build should show green checkmark
   - All stages should pass
   - Application deployed at http://localhost:8090

---

## ✅ Verification

### Test Your Deployment:

```bash
# Test home page
curl http://localhost:8090/

# Test books page
curl http://localhost:8090/books/

# Check containers
docker-compose ps

# Check logs
docker-compose logs -f
```

### Expected Results:
- ✅ All curl commands return HTML (status 200)
- ✅ Three containers running (mysql, flask, nginx)
- ✅ No error messages in logs
- ✅ Application accessible in browser

---

## 🎊 Success! What's Next?

### 1. Set Up Automated Builds (Webhooks)

**GitHub Webhook:**
1. Go to your GitHub repo → Settings → Webhooks
2. Click "Add webhook"
3. Payload URL: `http://YOUR_JENKINS_URL:8080/github-webhook/`
4. Content type: `application/json`
5. Events: "Just the push event"
6. Click "Add webhook"

Now every `git push` triggers automatic build!

### 2. Configure Notifications

**Email Notifications:**
1. Manage Jenkins → Configure System
2. Scroll to "E-mail Notification"
3. SMTP server: `smtp.gmail.com` (for Gmail)
4. Click "Advanced"
5. Check "Use SMTP Authentication"
6. Username: your.email@gmail.com
7. Password: (app password for Gmail)
8. SMTP Port: 587
9. Test configuration

### 3. Add More Environments

Create separate branches for:
- `dev` - Development
- `staging` - Staging
- `main` - Production

Each branch can have its own pipeline configuration.

### 4. Monitor and Maintain

**Daily:**
- Check build status
- Review failed builds

**Weekly:**
- Review build performance
- Clean old containers: `docker system prune`

**Monthly:**
- Update Jenkins and plugins
- Review pipeline efficiency
- Update documentation

---

## 🐛 Common Issues & Solutions

### Issue 1: Jenkins Can't Access Docker
**Solution:**
```bash
# Linux
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

### Issue 2: Port 8080 Already in Use
**Solution:**
```bash
# Use different port
java -jar jenkins.war --httpPort=8081
```

### Issue 3: Build Fails at "Health Check"
**Solution:**
- Increase wait time in Jenkinsfile
- Check if containers are running: `docker-compose ps`
- Check logs: `docker-compose logs`

### Issue 4: Git Authentication Failed
**Solution:**
- Use Personal Access Token instead of password
- GitHub: Settings → Developer settings → Personal access tokens
- Use token as password in Jenkins

---

## 📚 Additional Resources

### Documentation:
- **Full Setup Guide**: `JENKINS_SETUP.md`
- **Quick Reference**: `JENKINS_QUICK_REFERENCE.md`
- **Change Log**: `info.md`

### Learning Resources:
- Jenkins Documentation: https://www.jenkins.io/doc/
- Docker Docs: https://docs.docker.com/
- Git Tutorial: https://git-scm.com/doc

### Community:
- Jenkins Community: https://community.jenkins.io/
- Stack Overflow: Tag `jenkins`
- GitHub Discussions

---

## 🎯 Achievement Unlocked!

You now have:
- ✅ Fully automated CI/CD pipeline
- ✅ Automated testing on every commit
- ✅ Security scanning
- ✅ Containerized deployment
- ✅ Health monitoring
- ✅ Build artifacts and reports

**Congratulations! 🎉**

Your Library Management System is now deployed with professional-grade CI/CD automation!

---

## 💡 Pro Tips

1. **Use Blue Ocean** - Much better visual interface
2. **Tag releases** - Use Git tags for production releases
3. **Backup Jenkins** - Regular backups of `~/.jenkins/`
4. **Monitor builds** - Set up email/Slack notifications
5. **Document changes** - Keep info.md updated
6. **Test locally** - Use `test-deployment.sh` before committing
7. **Review logs** - Check logs regularly for issues
8. **Keep updated** - Update Jenkins and plugins monthly

---

## 🔒 Security Best Practices

1. ✅ Never commit secrets to Git
2. ✅ Use Jenkins credentials store
3. ✅ Enable CSRF protection
4. ✅ Use HTTPS for Jenkins (production)
5. ✅ Regular security updates
6. ✅ Limit Jenkins access (firewall)
7. ✅ Use strong passwords
8. ✅ Enable audit logging

---

## 📞 Need Help?

- Review `JENKINS_SETUP.md` for detailed guides
- Check `JENKINS_QUICK_REFERENCE.md` for commands
- Check Jenkins console output for errors
- Review container logs: `docker-compose logs`
- Search Stack Overflow with error messages

---

**Remember**: CI/CD is a journey, not a destination. Keep improving! 🚀
