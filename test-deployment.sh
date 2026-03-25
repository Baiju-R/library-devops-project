#!/bin/bash

# Library Management System - Test Deployment Script
# This script simulates what Jenkins pipeline does

set -e  # Exit on error

echo "======================================"
echo "   Testing Deployment Process        "
echo "======================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
PASSED=0
FAILED=0

# Function to test endpoint
test_endpoint() {
    local url=$1
    local name=$2
    
    if curl -f -s -o /dev/null "$url"; then
        echo -e "${GREEN}✅ $name: OK${NC}"
        ((PASSED++))
    else
        echo -e "${RED}❌ $name: FAILED${NC}"
        ((FAILED++))
    fi
}

# 1. Check required tools
echo "1. Checking required tools..."
command -v docker >/dev/null 2>&1 && echo "  ✓ Docker installed" || { echo "  ✗ Docker not found"; exit 1; }
command -v docker-compose >/dev/null 2>&1 && echo "  ✓ Docker Compose installed" || { echo "  ✗ Docker Compose not found"; exit 1; }
command -v git >/dev/null 2>&1 && echo "  ✓ Git installed" || { echo "  ✗ Git not found"; exit 1; }
echo ""

# 2. Code analysis
echo "2. Running code analysis..."
PY_FILES=$(find . -name "*.py" | wc -l)
echo "  Python files: $PY_FILES"
echo ""

# 3. Cleanup
echo "3. Cleaning up previous deployment..."
docker-compose down -v 2>&1 | grep -v "No resource found" || true
echo "  ✓ Cleanup complete"
echo ""

# 4. Build
echo "4. Building Docker images..."
docker-compose build --no-cache flask 2>&1 | tail -5
echo "  ✓ Build complete"
echo ""

# 5. Deploy
echo "5. Deploying services..."
docker-compose up -d
echo "  Waiting for services to start (30 seconds)..."
sleep 30
docker-compose ps
echo ""

# 6. Health checks
echo "6. Running health checks..."
echo "  Waiting additional 10 seconds for stability..."
sleep 10

test_endpoint "http://localhost:8090/" "Home Page"
test_endpoint "http://localhost:8090/books/" "Books Page"
test_endpoint "http://localhost:8090/books/search?keyword=test" "Search Function"

# Check MySQL
if docker exec library_mysql mysql -uroot -proot -e "SHOW DATABASES;" 2>/dev/null | grep -q "lms"; then
    echo -e "${GREEN}✅ MySQL Database: OK${NC}"
    ((PASSED++))
else
    echo -e "${RED}❌ MySQL Database: FAILED${NC}"
    ((FAILED++))
fi
echo ""

# 7. Container status
echo "7. Container status:"
docker-compose ps
echo ""

# 8. Performance test
echo "8. Running performance test..."
for i in {1..3}; do
    TIME=$(curl -s -o /dev/null -w "%{time_total}" http://localhost:8090/books/)
    echo "  Request $i: ${TIME}s"
done
echo ""

# Final report
echo "======================================"
echo "   Test Results                      "
echo "======================================"
echo -e "Passed: ${GREEN}$PASSED${NC}"
echo -e "Failed: ${RED}$FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ ALL TESTS PASSED!${NC}"
    echo ""
    echo "Application is running at:"
    echo "  → http://localhost:8090"
    exit 0
else
    echo -e "${RED}❌ SOME TESTS FAILED${NC}"
    echo ""
    echo "Check the logs above for details"
    exit 1
fi
