pipeline {
    agent any
    
    environment {
        COMPOSE_PROJECT_NAME = 'library-management-system'
        DOCKER_IMAGE_NAME = 'library-flask-app'
        GIT_COMMIT_SHORT = sh(script: "git rev-parse --short HEAD || echo 'unknown'", returnStdout: true).trim()
        BUILD_TIMESTAMP = sh(script: "date +%Y%m%d-%H%M%S || echo 'unknown'", returnStdout: true).trim()
    }
    
    stages {
        stage('Environment Check') {
            steps {
                script {
                    echo "======================================"
                    echo "   Library Management System CI/CD   "
                    echo "======================================"
                    echo "Build Number: ${env.BUILD_NUMBER}"
                    echo "Git Commit: ${GIT_COMMIT_SHORT}"
                    echo "Workspace: ${env.WORKSPACE}"
                    
                    // Check required tools
                    sh '''
                        echo "Checking required tools..."
                        docker --version
                        docker-compose --version
                        git --version
                    '''
                }
            }
        }
        
        stage('Checkout') {
            steps {
                script {
                    echo "Checking out source code..."
                    checkout scm
                    
                    // Display current branch and commit
                    sh '''
                        echo "Current branch: $(git branch --show-current || echo 'detached HEAD')"
                        echo "Latest commit: $(git log -1 --oneline || echo 'No commits')"
                    '''
                }
            }
        }
        
        stage('Code Analysis') {
            steps {
                script {
                    echo "Running code quality checks..."
                    
                    // Count Python files
                    sh '''
                        echo "Python files count: $(find . -name '*.py' | wc -l)"
                        echo "Total lines of Python code: $(find . -name '*.py' -exec wc -l {} + | tail -1 || echo '0')"
                    '''
                    
                    // Optional: Run flake8 if installed
                    sh '''
                        if command -v flake8 &> /dev/null; then
                            echo "Running flake8..."
                            flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics || true
                        else
                            echo "Flake8 not installed, skipping..."
                        fi
                    '''
                }
            }
        }
        
        stage('Cleanup Previous Containers') {
            steps {
                script {
                    echo "Cleaning up previous deployment..."
                    sh '''
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
                        
                        echo "Cleanup completed - all containers and networks removed"
                    '''
                }
            }
        }
        
        stage('Build Docker Images') {
            steps {
                script {
                    echo "Building Docker images..."
                    sh '''
                        # Build the Flask application image
                        docker-compose build --no-cache flask
                        
                        echo "Docker image built successfully"
                        docker images | grep library-management || true
                    '''
                }
            }
        }
        
        stage('Unit Tests') {
            steps {
                script {
                    echo "Running unit tests..."
                    
                    // Start MySQL for testing
                    sh '''
                        echo "Starting MySQL container for tests..."
                        
                        # Remove any existing MySQL container first
                        docker rm -f library_mysql 2>/dev/null || true
                        
                        # Start MySQL
                        docker-compose up -d mysql
                        
                        # Wait for MySQL to be ready
                        echo "Waiting for MySQL to be ready..."
                        sleep 20
                        
                        # Verify MySQL is running
                        if docker ps | grep library_mysql; then
                            echo "MySQL container is running"
                        else
                            echo "WARNING: MySQL container may not be running"
                            docker-compose ps mysql
                        fi
                    '''
                    
                    // Run tests inside container
                    sh '''
                        echo "Running application tests..."
                        docker-compose run --rm flask python test_books.py
                        TEST_EXIT_CODE=$?
                        if [ $TEST_EXIT_CODE -ne 0 ]; then
                            echo "Tests failed with exit code: $TEST_EXIT_CODE"
                            exit $TEST_EXIT_CODE
                        fi
                        echo "Tests passed successfully"
                    '''
                }
            }
        }
        
        stage('Security Scan') {
            steps {
                script {
                    echo "Running security checks..."
                    
                    // Check for common security issues
                    sh '''
                        echo "Checking for hardcoded secrets..."
                        if grep -r "password.*=.*" --include="*.py" --exclude-dir=".git" . | grep -v "DB_PASSWORD.*os.getenv" | grep -v "# " | grep -v "test"; then
                            echo "WARNING: Potential hardcoded passwords found!"
                        else
                            echo "No hardcoded passwords detected"
                        fi
                        
                        echo "Checking Dockerfile best practices..."
                        if grep -q "apt-get.*install" Dockerfile && grep -q "rm -rf /var/lib/apt/lists" Dockerfile; then
                            echo "Dockerfile follows cleanup best practices"
                        else
                            echo "Dockerfile check completed"
                        fi
                        
                        echo "Security scan completed"
                    '''
                }
            }
        }
        
        stage('Deploy Services') {
            steps {
                script {
                    echo "Deploying all services..."
                    sh '''
                        # Start all services
                        docker-compose up -d
                        
                        echo "Waiting for services to be healthy..."
                        sleep 30
                        
                        # Check container status
                        docker-compose ps
                    '''
                }
            }
        }
        
        stage('Health Check') {
            steps {
                script {
                    echo "Performing health checks..."
                    
                    retry(3) {
                        sh '''
                            # Wait a bit more for services to stabilize
                            sleep 10
                            
                            # Test home page
                            echo "Testing home page..."
                            curl -f -s -o /dev/null -w "Home Page Status: %{http_code}\\n" http://localhost:8090/ || exit 1
                            
                            # Test books page
                            echo "Testing books page..."
                            curl -f -s -o /dev/null -w "Books Page Status: %{http_code}\\n" http://localhost:8090/books/ || exit 1
                            
                            # Check MySQL connection
                            echo "Testing MySQL connection..."
                            docker exec library_mysql mysql -uroot -proot -e "SHOW DATABASES;" | grep lms || exit 1
                            
                            echo "✓ All health checks passed!"
                        '''
                    }
                }
            }
        }
        
        stage('Integration Tests') {
            steps {
                script {
                    echo "Running integration tests..."
                    sh '''
                        # Test various endpoints
                        echo "Testing multiple endpoints..."
                        
                        # Home page
                        STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8090/)
                        echo "Home: $STATUS"
                        [ "$STATUS" = "200" ] || exit 1
                        
                        # Books listing
                        STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8090/books/)
                        echo "Books: $STATUS"
                        [ "$STATUS" = "200" ] || exit 1
                        
                        # Search functionality
                        STATUS=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:8090/books/search?keyword=test")
                        echo "Search: $STATUS"
                        [ "$STATUS" = "200" ] || exit 1
                        
                        echo "✓ Integration tests passed!"
                    '''
                }
            }
        }
        
        stage('Performance Test') {
            steps {
                script {
                    echo "Running basic performance tests..."
                    sh '''
                        echo "Testing application response time..."
                        for i in {1..5}; do
                            TIME=$(curl -s -o /dev/null -w "%{time_total}" http://localhost:8090/books/)
                            echo "Request $i: ${TIME}s"
                        done
                        
                        echo "✓ Performance test completed"
                    '''
                }
            }
        }
        
        stage('Tag & Archive') {
            steps {
                script {
                    echo "Tagging Docker image..."
                    sh """
                        # Tag with build number
                        docker tag library-management-system-master-flask:latest \
                            ${DOCKER_IMAGE_NAME}:build-${BUILD_NUMBER}
                        
                        # Tag with git commit
                        docker tag library-management-system-master-flask:latest \
                            ${DOCKER_IMAGE_NAME}:${GIT_COMMIT_SHORT}
                        
                        echo "Images tagged successfully"
                        docker images | grep ${DOCKER_IMAGE_NAME}
                    """
                }
            }
        }
        
        stage('Documentation') {
            steps {
                script {
                    echo "Generating deployment documentation..."
                    sh """
                        cat > deployment-report.txt << EOF
========================================
Library Management System - Deployment
========================================
Build Number: ${BUILD_NUMBER}
Git Commit: ${GIT_COMMIT_SHORT}
Timestamp: ${BUILD_TIMESTAMP}
Jenkins Job: ${JOB_NAME}
Build URL: ${BUILD_URL}

Services Deployed:
- MySQL (Port 3307)
- Flask Application (4 workers)
- Nginx Reverse Proxy (Port 8090)

Application URL: http://localhost:8090

Status: SUCCESS
========================================
EOF
                        cat deployment-report.txt
                    """
                    
                    archiveArtifacts artifacts: 'deployment-report.txt', allowEmptyArchive: false
                }
            }
        }
    }
    
    post {
        success {
            script {
                echo "======================================"
                echo "   ✓ DEPLOYMENT SUCCESSFUL!           "
                echo "======================================"
                echo "Application is now running at:"
                echo "  → http://localhost:8090"
                echo ""
                echo "Container Status:"
                sh 'docker-compose ps'
            }
        }
        
        failure {
            script {
                echo "======================================"
                echo "   ✗ DEPLOYMENT FAILED!               "
                echo "======================================"
                echo "Check the logs above for details"
                
                // Collect logs for debugging
                sh '''
                    echo "Collecting container logs..."
                    docker-compose logs --tail=50 > failed-deployment-logs.txt || true
                '''
                
                archiveArtifacts artifacts: 'failed-deployment-logs.txt', allowEmptyArchive: true
            }
        }
        
        always {
            script {
                echo "Pipeline execution completed"
                echo "Build artifacts archived"
                
                // Optional: Cleanup old images
                sh '''
                    echo "Cleaning up old Docker images..."
                    docker image prune -f --filter "until=72h" || true
                '''
            }
        }
        
        unstable {
            script {
                echo "Build is unstable. Please review test results."
            }
        }
    }
}
