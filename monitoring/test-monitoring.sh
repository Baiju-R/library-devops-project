#!/bin/bash

# Monitoring Stack Test Script
# Tests Prometheus and Grafana setup

set -e

echo "=========================================="
echo "  Library Management System"
echo "  Monitoring Stack Test"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check if a service is reachable
check_service() {
    local name=$1
    local url=$2
    local expected_status=${3:-200}
    
    echo -n "Checking $name... "
    
    if response=$(curl -s -o /dev/null -w "%{http_code}" "$url" 2>/dev/null); then
        if [ "$response" -eq "$expected_status" ]; then
            echo -e "${GREEN}✓ OK${NC} (HTTP $response)"
            return 0
        else
            echo -e "${YELLOW}⚠ WARNING${NC} (HTTP $response, expected $expected_status)"
            return 1
        fi
    else
        echo -e "${RED}✗ FAILED${NC} (Connection failed)"
        return 1
    fi
}

# Function to check if a container is running
check_container() {
    local name=$1
    echo -n "Checking container $name... "
    
    if docker ps --format '{{.Names}}' | grep -q "^${name}$"; then
        echo -e "${GREEN}✓ Running${NC}"
        return 0
    else
        echo -e "${RED}✗ Not running${NC}"
        return 1
    fi
}

# Function to check Prometheus targets
check_prometheus_targets() {
    echo -n "Checking Prometheus targets... "
    
    targets=$(curl -s http://localhost:9090/api/v1/targets 2>/dev/null)
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}✗ Cannot reach Prometheus API${NC}"
        return 1
    fi
    
    up_count=$(echo "$targets" | grep -o '"health":"up"' | wc -l)
    total_count=$(echo "$targets" | grep -o '"health":' | wc -l)
    
    if [ "$up_count" -eq "$total_count" ] && [ "$total_count" -gt 0 ]; then
        echo -e "${GREEN}✓ All $total_count targets UP${NC}"
        return 0
    else
        echo -e "${YELLOW}⚠ $up_count/$total_count targets UP${NC}"
        return 1
    fi
}

# Function to test Flask metrics endpoint
check_flask_metrics() {
    echo -n "Checking Flask metrics endpoint... "
    
    metrics=$(curl -s http://localhost:5000/metrics 2>/dev/null)
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}✗ Cannot reach Flask metrics${NC}"
        return 1
    fi
    
    if echo "$metrics" | grep -q "flask_http_request_total"; then
        metric_count=$(echo "$metrics" | grep -c "^flask_")
        echo -e "${GREEN}✓ OK${NC} ($metric_count Flask metrics found)"
        return 0
    else
        echo -e "${RED}✗ No Flask metrics found${NC}"
        return 1
    fi
}

# Function to check Grafana datasource
check_grafana_datasource() {
    echo -n "Checking Grafana datasource... "
    
    # Wait for Grafana to be ready
    sleep 2
    
    datasources=$(curl -s -u admin:admin http://localhost:3000/api/datasources 2>/dev/null)
    
    if [ $? -ne 0 ]; then
        echo -e "${YELLOW}⚠ Cannot reach Grafana API${NC}"
        return 1
    fi
    
    if echo "$datasources" | grep -q "Prometheus"; then
        echo -e "${GREEN}✓ Prometheus datasource configured${NC}"
        return 0
    else
        echo -e "${YELLOW}⚠ Prometheus datasource not found${NC}"
        return 1
    fi
}

echo "1. Container Status"
echo "-------------------"
check_container "library_flask"
check_container "library_prometheus"
check_container "library_grafana"
echo ""

echo "2. Service Availability"
echo "----------------------"
check_service "Flask App" "http://localhost:5000/health"
check_service "Prometheus" "http://localhost:9090/-/healthy"
check_service "Grafana" "http://localhost:3000/api/health"
echo ""

echo "3. Metrics Collection"
echo "--------------------"
check_flask_metrics
check_prometheus_targets
echo ""

echo "4. Grafana Configuration"
echo "-----------------------"
check_grafana_datasource
echo ""

echo "=========================================="
echo "  Test Summary"
echo "=========================================="
echo ""
echo "Access Points:"
echo "  • Application:  http://localhost:8090"
echo "  • Prometheus:   http://localhost:9090"
echo "  • Grafana:      http://localhost:3000"
echo ""
echo "Grafana Credentials:"
echo "  • Username: admin"
echo "  • Password: admin"
echo ""
echo "Next Steps:"
echo "  1. Open Grafana at http://localhost:3000"
echo "  2. Navigate to Dashboards"
echo "  3. View 'Library Management System - Application Metrics'"
echo "  4. Generate traffic: curl http://localhost:8090"
echo "  5. Watch metrics update in real-time"
echo ""
echo "=========================================="
