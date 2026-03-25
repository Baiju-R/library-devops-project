# Library Management System - Change Log

## Monitoring Stack Integration: Prometheus & Grafana (2026-03-25) - ADDED

### Overview
Integrated complete monitoring and observability stack using Prometheus and Grafana for real-time application metrics, performance tracking, and visualization.

### Components Added

#### 1. Prometheus (Port 9090)
**Purpose**: Time-series metrics collection and storage

**Configuration File**: `monitoring/prometheus/prometheus.yml`
- Scrape interval: 15 seconds
- Evaluation interval: 15 seconds
- External labels: monitor='library-management-monitor', environment='production'

**Scrape Targets**:
- **prometheus** (localhost:9090): Self-monitoring
- **flask-app** (flask:5000): Flask application metrics at `/metrics` endpoint
- **nginx** (nginx:80): Nginx status metrics at `/nginx_status` (optional)
- **mysql-exporter** (mysql-exporter:9104): MySQL database metrics (commented, optional)

#### 2. Grafana (Port 3000)
**Purpose**: Metrics visualization and dashboards

**Default Credentials**:
- Username: `admin`
- Password: `admin`

**Provisioning Files**:
- `monitoring/grafana/provisioning/datasources/prometheus.yml`: Auto-configures Prometheus datasource
- `monitoring/grafana/provisioning/dashboards/dashboard.yml`: Dashboard provider configuration
- `monitoring/grafana/provisioning/dashboards/flask-dashboard.json`: Pre-built Flask metrics dashboard

**Pre-built Dashboard Panels**:
1. **Flask HTTP Request Rate**: Real-time request rate by endpoint and method
2. **Average Response Time**: Gauge showing current average response time (threshold: 500ms)
3. **HTTP Status Codes**: Timeline of status code distribution
4. **Flask App Status**: Simple up/down health indicator

#### 3. Flask Metrics Exporter
**Library Added**: `prometheus-flask-exporter==0.23.0`

**Changes to `app.py`**:
```python
from prometheus_flask_exporter import PrometheusMetrics

# Initialize Prometheus metrics
metrics = PrometheusMetrics(app)

# Add info metric
metrics.info('flask_app_info', 'Application info', 
             version='1.0.0', app_name='library-management-system')
```

**Metrics Exposed at `/metrics` endpoint**:
- `flask_http_request_total`: Total HTTP requests (by method, endpoint, status)
- `flask_http_request_duration_seconds`: HTTP request latency histogram
- `flask_http_request_exceptions_total`: Total exceptions in HTTP requests
- `flask_app_info`: Application information (version, name)

#### 4. Docker Compose Updates
**File**: `docker-compose.yml`

**Added Services**:
```yaml
prometheus:
  image: prom/prometheus:latest
  container_name: library_prometheus
  ports: 9090:9090
  volumes:
    - ./monitoring/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
    - prometheus_data:/prometheus

grafana:
  image: grafana/grafana:latest
  container_name: library_grafana
  ports: 3000:3000
  environment:
    - GF_SECURITY_ADMIN_USER=admin
    - GF_SECURITY_ADMIN_PASSWORD=admin
  volumes:
    - grafana_data:/var/lib/grafana
    - ./monitoring/grafana/provisioning:/etc/grafana/provisioning
```

**Added Network**:
- `library-network`: Bridge network for all services to communicate

**Added Volumes**:
- `prometheus_data`: Persistent storage for Prometheus time-series data
- `grafana_data`: Persistent storage for Grafana dashboards and settings

**Network Configuration**:
All services (mysql, flask, nginx, prometheus, grafana) now connected via `library-network`

#### 5. Documentation & Scripts

**Created Files**:
1. **`monitoring/README.md`** (9.5 KB):
   - Complete monitoring stack documentation
   - Architecture diagrams
   - Configuration guide
   - PromQL query examples
   - Troubleshooting guide
   - Best practices for production deployment

2. **`monitoring/test-monitoring.sh`** (4.7 KB):
   - Automated test script for monitoring stack
   - Checks container status
   - Verifies service availability
   - Tests metrics collection
   - Validates Grafana datasource configuration

### Features & Benefits

#### Real-time Observability
- ✅ Track HTTP request rates per endpoint
- ✅ Monitor average response times and percentiles
- ✅ Identify slow endpoints and bottlenecks
- ✅ Track error rates by status code
- ✅ Monitor application health and uptime

#### Pre-configured Dashboards
- ✅ No manual setup required - auto-provisioned on startup
- ✅ Pre-built Flask application dashboard
- ✅ Customizable panels and queries
- ✅ 5-second refresh rate for near real-time updates

#### Metrics Collection
- ✅ Automatic instrumentation of all Flask routes
- ✅ No code changes needed for basic metrics
- ✅ Custom metrics support for business logic
- ✅ 15-second scrape interval (configurable)

#### Data Persistence
- ✅ Prometheus: 15-day retention (configurable)
- ✅ Grafana: All dashboards and settings persist
- ✅ Docker volumes for data persistence across restarts

### Usage

#### Starting the Monitoring Stack
```bash
# Start all services including monitoring
docker-compose up -d

# Check monitoring containers
docker ps | grep -E "prometheus|grafana"

# Test monitoring setup
bash monitoring/test-monitoring.sh
```

#### Accessing Dashboards
- **Grafana**: http://localhost:3000 (admin/admin)
- **Prometheus**: http://localhost:9090
- **Flask Metrics**: http://localhost:5000/metrics

#### Generating Test Traffic
```bash
# Generate traffic to see metrics
for i in {1..100}; do 
    curl -s http://localhost:8090/books/ > /dev/null
done

# Watch metrics in real-time in Grafana
```

#### Example PromQL Queries
```promql
# Request rate per second
rate(flask_http_request_total[5m])

# Average response time
flask_http_request_duration_seconds_sum / flask_http_request_duration_seconds_count

# Error rate (5xx responses)
rate(flask_http_request_total{status=~"5.."}[5m])

# 95th percentile response time
histogram_quantile(0.95, rate(flask_http_request_duration_seconds_bucket[5m]))
```

### Impact
- ✅ **Visibility**: Complete visibility into application performance
- ✅ **Debugging**: Quickly identify performance issues and errors
- ✅ **Capacity Planning**: Track trends for resource planning
- ✅ **SLA Monitoring**: Measure and track service level objectives
- ✅ **Production Ready**: Industry-standard monitoring stack

### Files Modified
1. **requirements.txt**: Added `prometheus-flask-exporter==0.23.0`
2. **app.py**: Added Prometheus metrics initialization (3 lines)
3. **docker-compose.yml**: Added prometheus, grafana services, network, volumes
4. **README.md**: Added monitoring section with quick start guide

### Files Created
1. `monitoring/prometheus/prometheus.yml` - Prometheus configuration
2. `monitoring/grafana/provisioning/datasources/prometheus.yml` - Datasource config
3. `monitoring/grafana/provisioning/dashboards/dashboard.yml` - Dashboard provider
4. `monitoring/grafana/provisioning/dashboards/flask-dashboard.json` - Pre-built dashboard
5. `monitoring/README.md` - Comprehensive monitoring documentation
6. `monitoring/test-monitoring.sh` - Monitoring test script

### Next Steps for Users
1. Start the stack: `docker-compose up -d`
2. Open Grafana: http://localhost:3000
3. Login with admin/admin
4. View pre-configured dashboard
5. Generate traffic to see live metrics
6. Customize dashboards as needed
7. Set up alerts (optional, see monitoring/README.md)

### Production Recommendations
1. Change default Grafana password
2. Configure alert rules in Prometheus
3. Set up Alertmanager for notifications
4. Adjust retention policy based on storage
5. Add MySQL exporter for database metrics
6. Configure TLS/HTTPS for Grafana
7. Set up authentication for Prometheus

---

---

## Issue Fix: 502 Bad Gateway on Books Tab (2026-03-25) - RESOLVED

### Problem Identified
Users were experiencing intermittent 502 Bad Gateway errors when accessing the books tab.

### Root Cause Analysis
- Nginx configuration was minimal and lacked proper error handling
- Missing MIME types configuration causing issues with static files
- No connection pooling or keepalive settings
- Missing timeout configurations
- Debug log level causing excessive logging
- Gunicorn workers had no timeout configurations
- Flask app lacked comprehensive error handling and logging
- No health check endpoint for monitoring

### Changes Made

#### 1. Enhanced Nginx Configuration (`nginx/nginx.conf`)
**Added/Modified:**
- `events { worker_connections 1024; }` - Increased worker connections for better concurrency
- `include /etc/nginx/mime.types;` - Proper MIME type handling for static files
- `default_type application/octet-stream;` - Default MIME type
- `upstream flask_app` block enhanced with:
  - `max_fails=3 fail_timeout=30s` - Better failure handling
  - `keepalive 32` - Connection pooling to Flask backend
- Connection settings:
  - `keepalive_timeout 65;` - Maintain connections
  - `client_max_body_size 10M;` - Allow larger uploads
- Timeout settings:
  - `proxy_connect_timeout 60s;`
  - `proxy_send_timeout 60s;`
  - `proxy_read_timeout 60s;`
- Compression: `gzip on` with proper types
- Proxy settings enhanced:
  - `proxy_http_version 1.1` - Use HTTP/1.1
  - `proxy_buffering off` - Disable buffering for real-time responses
  - `Connection ""` - Enable keepalive to upstream
- Changed error log level from `debug` to `info` - Reduce log noise

#### 2. Improved Gunicorn Configuration (`Dockerfile`)
**Added:**
- `--timeout 120` - Worker timeout for long-running requests
- `--graceful-timeout 30` - Graceful shutdown period
- `--access-logfile -` - Log access to stdout
- `--error-logfile -` - Log errors to stdout
- `--log-level info` - Appropriate log level

#### 3. Enhanced Flask Application (`app.py`)
**Added:**
- Comprehensive error handler with `@app.errorhandler(Exception)`
- Request logging in `@app.before_request` with IP address
- Response logging in `@app.after_request` with status codes
- Health check endpoint at `/health` for monitoring
- Better exception handling with full stack traces logged to both stderr and stdout

#### 4. Improved Dockerfile
**Added:**
- `curl` package for health checks
- Proper cleanup with `rm -rf /var/lib/apt/lists/*`

#### 5. Docker Compose Enhancement (`docker-compose.yml`)
**Added:**
- Health check configuration for Flask container:
  - Test: curl to /health endpoint
  - Interval: 30s
  - Timeout: 10s
  - Retries: 3
  - Start period: 40s

### Testing & Verification ✅
After comprehensive rebuild:
- **Container Status**: All 3 containers running healthily
- **Nginx configuration**: ✅ PASSED (`nginx -t`)
- **Flask Gunicorn workers**: ✅ 4 workers running with proper timeouts
- **Books endpoint tests**:
  - `/books` (no trailing slash): ✅ 200 OK - Returns HTML
  - `/books/` (with trailing slash): ✅ 200 OK - Returns HTML
  - Books are being displayed correctly with data from MySQL
- **Home page**: ✅ 200 OK
- **Static files**: ✅ Loading correctly (bootstrap, CSS, images)
- **Stress test**: ✅ 10 consecutive requests - All successful
- **No 502 errors observed** after full rebuild and configuration changes
- **Comprehensive logging**: Request/Response logging active for debugging
- **Health monitoring**: Container health checks configured

### Final Status: ✅ FULLY OPERATIONAL
Application is now stable with proper error handling, logging, and monitoring.

### Services Running
1. **MySQL** (library_mysql) - Port 3307:3306
2. **Flask** (library_flask) - 4 Gunicorn workers on port 5000
3. **Nginx** (library_nginx) - Port 8090:80 (reverse proxy)

### Future Recommendations
- Consider adding health check endpoints
- Monitor Nginx access logs for patterns
- Add rate limiting if needed
- Consider adding caching for static content

### Quick Commands Reference
```bash
# Start all containers
docker-compose up -d --build

# Check container status
docker-compose ps

# View logs
docker-compose logs nginx
docker-compose logs flask
docker-compose logs mysql

# Restart specific service
docker-compose restart nginx

# Stop all containers
docker-compose down

# Test Nginx configuration
docker exec library_nginx nginx -t

# Access the application
http://localhost:8090
```

### Container Details
- **MySQL Container**: library_mysql
  - Port: 3307:3306
  - Database: lms
  - Root Password: root
  
- **Flask Container**: library_flask
  - Internal Port: 5000
  - Workers: 4 (Gunicorn)
  - Wait script: Ensures MySQL is ready before starting
  
- **Nginx Container**: library_nginx
  - Port: 8090:80
  - Config: ./nginx/nginx.conf
  - Role: Reverse proxy to Flask app

---

## Reference Links
http://www.utm.mx/~caff/doc/OpenUPWeb/openup/guidances/guidelines/entity_control_boundary_pattern_C4047897.html

An example of an entity for a customer service application is a Customer entity that manages all information about a customer. **A design element for this entity would include data about the customer, behavior to manage the data, behavior to validate customer information and to perform other business calculations, such as "Is this customer allowed to purchase product X?"**
---

## Jenkins CI/CD Pipeline Setup (2026-03-25)

### Overview
Implemented complete CI/CD pipeline using Jenkins for automated building, testing, and deployment.

### Pipeline Components

#### Jenkinsfile Created
**Location**: ./Jenkinsfile
**Type**: Declarative Pipeline

#### Pipeline Stages (13 stages):
1. **Environment Check** - Verify Docker, Git, Docker Compose availability
2. **Checkout** - Clone repository from Git SCM
3. **Code Analysis** - Count files, lines of code, optional flake8
4. **Cleanup Previous Containers** - Remove old deployments
5. **Build Docker Images** - Build Flask application image with no-cache
6. **Unit Tests** - Run Python tests in container
7. **Security Scan** - Check for hardcoded secrets and Dockerfile best practices
8. **Deploy Services** - Start all containers (MySQL, Flask, Nginx)
9. **Health Check** - Verify all endpoints respond (retry 3 times)
10. **Integration Tests** - Test home, books, and search endpoints
11. **Performance Test** - Basic response time testing (5 requests)
12. **Tag & Archive** - Tag images with build number and git commit
13. **Documentation** - Generate deployment report

#### Post Actions:
- **Success**: Display success message and container status
- **Failure**: Collect logs and archive for debugging
- **Always**: Cleanup old Docker images (72+ hours old)
- **Unstable**: Log warning message

### Files Created
1. **Jenkinsfile** - Complete pipeline definition with all stages
2. **JENKINS_SETUP.md** - Comprehensive setup guide

### Features Implemented

#### ✅ Automated Testing
- Unit tests with Python test framework
- Integration tests for all endpoints (/, /books/, /books/search)
- Health checks with automatic retry (3 attempts)
- Performance testing (response time measurement)
- MySQL connection verification

#### ✅ Security & Quality
- Secret scanning (checks for hardcoded passwords)
- Dockerfile best practices validation
- Code quality metrics (file count, LOC)

#### ✅ Build Management
- Git commit tagging
- Build number versioning
- Docker image tagging system
- Artifact archiving (deployment reports, logs)

### How to Use

#### Manual Build:
1. Open Jenkins at http://localhost:8080
2. Create new Pipeline job
3. Configure Git repository URL
4. Point to Jenkinsfile
5. Click "Build Now"

#### Automated Build (Webhook):
1. Configure GitHub webhook to Jenkins
2. Every push triggers automatic build
3. Pipeline runs all stages automatically

### See JENKINS_SETUP.md for complete installation and configuration guide

---

## Jenkins Build Fix: Werkzeug Version Conflict & Security Scan (2026-03-25) - RESOLVED

### Problem Identified
After fixing the container name conflict, the Jenkins build encountered TWO new issues:

**Issue 1 - Unit Tests Stage:**
```
AttributeError: module 'werkzeug' has no attribute '__version__'
File "/usr/local/lib/python3.10/site-packages/flask/testing.py", line 118, in __init__
    "HTTP_USER_AGENT": f"werkzeug/{werkzeug.__version__}",
```

**Issue 2 - Security Scan Stage:**
```
Syntax error: Unterminated quoted string
```

### Root Cause Analysis

#### Issue 1: Werkzeug Version Incompatibility
- Flask 2.3.2 was installed without explicitly pinning Werkzeug version
- Docker build pulled Werkzeug 3.x (latest) which removed `__version__` attribute
- Flask 2.3.2's test client expects Werkzeug 2.x with `__version__` attribute
- Version mismatch caused test framework to crash before tests could run

#### Issue 2: Shell Script Syntax Error
- Security Scan stage used complex grep patterns with nested quotes: `password.*=.*['\"]`
- Jenkins shell executor couldn't properly escape the quotes in heredoc (`'''`)
- The pattern `['\"]` created unterminated string errors in sh context

### Changes Made

#### 1. Pin Werkzeug Version in requirements.txt
```diff
flask==2.3.2
+ werkzeug==2.3.7
flask-mysql==1.5.2
```

**Why Werkzeug 2.3.7?**
- Compatible with Flask 2.3.2
- Has `__version__` attribute needed by Flask test client
- Stable and well-tested combination

#### 2. Simplify Security Scan Shell Script
**Before:**
```groovy
if grep -r "password.*=.*['\"]" --include="*.py" ...
```

**After:**
```groovy
if grep -r "password.*=.*" --include="*.py" ... | grep -v "test"; then
```

**Benefits:**
- Removed problematic nested quotes `['\"]`
- Simplified regex pattern
- Added filter to exclude test files
- Added completion messages for better visibility

#### 3. Improve Unit Tests Error Handling
**Before:**
```groovy
docker-compose run --rm flask python test_books.py || echo "Tests completed with warnings"
```

**After:**
```groovy
docker-compose run --rm flask python test_books.py
TEST_EXIT_CODE=$?
if [ $TEST_EXIT_CODE -ne 0 ]; then
    echo "Tests failed with exit code: $TEST_EXIT_CODE"
    exit $TEST_EXIT_CODE
fi
```

**Benefits:**
- No longer masks test failures with `|| echo`
- Captures actual exit code
- Reports failures clearly
- Fails fast when tests fail (proper CI/CD behavior)

### Impact
- ✅ Flask test client now works correctly with compatible Werkzeug version
- ✅ Security Scan no longer has shell syntax errors
- ✅ Test failures are properly reported (not hidden)
- ✅ More reliable CI/CD pipeline

### Git Commit
- **Commit**: 9728fd8
- **Message**: "fix: Resolve Werkzeug version conflict and Security Scan shell errors"
- **Files Changed**: 
  - requirements.txt (+1 line: werkzeug==2.3.7)
  - Jenkinsfile (15 insertions, 5 deletions)

### Verification Steps
1. Pull latest code: `git pull origin main`
2. Rebuild Docker images: `docker-compose build --no-cache`
3. Run Jenkins build - should now pass Unit Tests and Security Scan stages

---

---

## Jenkins Build Fix: Container Name Conflict (2026-03-25) - RESOLVED

### Problem Identified
Jenkins build failed during "Unit Tests" stage with the following error:
```
Error response from daemon: Conflict. The container name "/library_mysql" is already in use by container "69da279d8f0c..."
```

### Root Cause Analysis
- Manual `docker-compose up` created containers with specific names (library_mysql, library_flask, library_nginx)
- Jenkins pipeline tried to create containers with the same names
- Docker doesn't allow duplicate container names
- The "Cleanup Previous Containers" stage wasn't comprehensive enough
- It only used `docker-compose down -v` which doesn't remove containers created outside of the current compose context

### Changes Made

#### 1. Enhanced Cleanup Stage in Jenkinsfile
**Added comprehensive cleanup steps:**
```groovy
# Stop and remove existing containers (including ones not managed by compose)
docker-compose down -v || true

# Force remove specific containers if they still exist
docker rm -f library_mysql library_flask library_nginx 2>/dev/null || true

# Remove any stopped containers
docker container prune -f || true

# Clean up dangling images
docker image prune -f || true

# Remove orphan networks
docker network prune -f || true
```

**Benefits:**
- Removes containers by specific names (handles containers from manual deployments)
- Prunes stopped containers system-wide
- Cleans up orphan networks
- Ensures clean slate before each Jenkins build
- Uses `|| true` to prevent failures if containers don't exist

#### 2. Improved Unit Tests Stage
**Added pre-cleanup check:**
```groovy
# Remove any existing MySQL container first
docker rm -f library_mysql 2>/dev/null || true

# Start MySQL
docker-compose up -d mysql
```

**Enhanced verification:**
```groovy
# Verify MySQL is running
if docker ps | grep library_mysql; then
    echo "MySQL container is running"
else
    echo "WARNING: MySQL container may not be running"
    docker-compose ps mysql
fi
```

### Impact
- ✅ Jenkins builds no longer fail due to container name conflicts
- ✅ Pipeline can run successfully even if manual containers are running
- ✅ Better cleanup ensures consistent build environment
- ✅ More robust error handling and logging

### Git Commit
- **Commit**: efd9958
- **Message**: "Fix: Improve container cleanup to handle name conflicts"
- **Files Changed**: Jenkinsfile (23 insertions, 4 deletions)

### Next Steps for Users
1. Pull the latest code: `git pull origin main`
2. Stop any running containers: `docker-compose down`
3. Trigger new Jenkins build
4. Build should now complete successfully

---

---

## GitHub Repository Update (2026-03-25)

### Code Successfully Pushed to GitHub ✅

**Repository**: https://github.com/Baiju-R/library-devops-project  
**Commit**: 157b439 - Add complete Jenkins CI/CD pipeline with comprehensive documentation  
**Branch**: main

### Files Pushed (11 files, 2,480 lines):

#### New Files:
1. **Jenkinsfile** - Complete 13-stage CI/CD pipeline
2. **JENKINS_SETUP.md** - Comprehensive installation guide (8.6 KB)
3. **JENKINS_QUICK_REFERENCE.md** - Command cheat sheet (6.2 KB)
4. **GETTING_STARTED.md** - 30-minute quick start guide (8.9 KB)
5. **CI_CD_IMPLEMENTATION.md** - Implementation overview (12.9 KB)
6. **JENKINSFILE_VERIFICATION_REPORT.md** - Verification report (12.2 KB)
7. **test-deployment.sh** - Local testing script (3.2 KB)
8. **.gitattributes** - Line ending configuration

#### Updated Files:
1. **.gitignore** - Added CI/CD artifacts exclusion
2. **README.md** - Added CI/CD section
3. **info.md** - Complete changelog (this file)

### Ready for Jenkins Integration

All CI/CD components are now in the GitHub repository and ready to be used by Jenkins:
- ✅ Pipeline definition (Jenkinsfile)
- ✅ Complete documentation
- ✅ Verification reports
- ✅ Testing scripts
- ✅ Configuration files

### Next Steps:
1. Install Jenkins: `java -jar jenkins.war --httpPort=8080`
2. Create Pipeline job pointing to: https://github.com/Baiju-R/library-devops-project
3. Configure to use Jenkinsfile from repository
4. Run build and deploy automatically!

---
