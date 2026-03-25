# Monitoring Stack - Prometheus & Grafana

This directory contains the configuration files for the monitoring stack used in the Library Management System.

## Overview

The monitoring stack consists of:

- **Prometheus**: Metrics collection and storage
- **Grafana**: Metrics visualization and dashboards

## Architecture

```
┌─────────────────┐
│  Flask App      │──► Exposes /metrics endpoint
│  (Port 5000)    │    (prometheus-flask-exporter)
└─────────────────┘
        │
        ▼
┌─────────────────┐
│  Prometheus     │──► Scrapes metrics every 15s
│  (Port 9090)    │    Stores time-series data
└─────────────────┘
        │
        ▼
┌─────────────────┐
│  Grafana        │──► Visualizes metrics
│  (Port 3000)    │    Dashboards & alerts
└─────────────────┘
```

## Quick Start

### 1. Start the Monitoring Stack

```bash
# Start all services including monitoring
docker-compose up -d

# Or start only monitoring services
docker-compose up -d prometheus grafana
```

### 2. Access the Dashboards

**Prometheus:**
- URL: http://localhost:9090
- Use to query raw metrics and check targets

**Grafana:**
- URL: http://localhost:3000
- Default credentials:
  - Username: `admin`
  - Password: `admin`
- Pre-configured with:
  - Prometheus datasource
  - Flask application dashboard

### 3. Verify Metrics Collection

**Check Flask metrics endpoint:**
```bash
curl http://localhost:5000/metrics
```

**Check Prometheus targets:**
- Open http://localhost:9090/targets
- All targets should show "UP" status

## Directory Structure

```
monitoring/
├── prometheus/
│   └── prometheus.yml          # Prometheus configuration
├── grafana/
│   └── provisioning/
│       ├── datasources/
│       │   └── prometheus.yml  # Auto-configure Prometheus datasource
│       └── dashboards/
│           ├── dashboard.yml   # Dashboard provider config
│           └── flask-dashboard.json  # Pre-built Flask dashboard
└── README.md                   # This file
```

## Configuration Files

### prometheus.yml

Main Prometheus configuration with scrape targets:
- **prometheus**: Self-monitoring (port 9090)
- **flask-app**: Flask application metrics (port 5000, path: /metrics)
- **nginx**: Nginx stub_status (port 80, path: /nginx_status)
- **mysql**: MySQL exporter (optional, commented out)

### Grafana Provisioning

**Datasources (`datasources/prometheus.yml`):**
- Auto-configures Prometheus as the default datasource
- No manual setup required

**Dashboards (`dashboards/`):**
- `dashboard.yml`: Dashboard provider configuration
- `flask-dashboard.json`: Pre-built dashboard showing:
  - HTTP request rate
  - Average response time
  - HTTP status codes distribution
  - Application uptime status

## Metrics Collected

### Flask Application Metrics

The Flask app uses `prometheus-flask-exporter` which automatically provides:

| Metric | Description |
|--------|-------------|
| `flask_http_request_total` | Total HTTP requests by method, endpoint, status |
| `flask_http_request_duration_seconds` | HTTP request latency in seconds |
| `flask_http_request_exceptions_total` | Total HTTP requests that resulted in exceptions |
| `flask_app_info` | Application information (version, name) |

### Custom Metrics

You can add custom metrics in `app.py`:

```python
from prometheus_flask_exporter import Counter, Histogram

# Custom counter
books_borrowed = Counter(
    'books_borrowed_total',
    'Total number of books borrowed'
)

# Custom histogram
db_query_duration = Histogram(
    'db_query_duration_seconds',
    'Database query duration in seconds'
)

# Use in your routes
@app.route('/books/borrow/<id>')
def borrow_book(id):
    books_borrowed.inc()  # Increment counter
    with db_query_duration.time():  # Track query time
        # Your database query here
        pass
```

## Prometheus Queries (PromQL)

### Useful queries for the Flask app:

**Request rate (per second):**
```promql
rate(flask_http_request_total[5m])
```

**Average response time:**
```promql
flask_http_request_duration_seconds_sum / flask_http_request_duration_seconds_count
```

**Error rate (5xx responses):**
```promql
rate(flask_http_request_total{status=~"5.."}[5m])
```

**95th percentile response time:**
```promql
histogram_quantile(0.95, rate(flask_http_request_duration_seconds_bucket[5m]))
```

## Grafana Dashboards

### Pre-configured Dashboard

The included `flask-dashboard.json` provides:

1. **HTTP Request Rate Panel**
   - Shows requests per second by endpoint and method
   - Useful for identifying traffic patterns

2. **Average Response Time Gauge**
   - Current average response time
   - Red threshold at 500ms

3. **HTTP Status Codes Timeline**
   - Distribution of status codes over time
   - Quickly spot error spikes

4. **Flask App Status Gauge**
   - Simple up/down indicator
   - Shows if Prometheus can reach the app

### Creating Custom Dashboards

1. Log into Grafana (http://localhost:3000)
2. Click **+** → **Dashboard**
3. Click **Add new panel**
4. Select **Prometheus** as datasource
5. Enter PromQL query
6. Customize visualization
7. Click **Apply** and **Save**

## Troubleshooting

### Prometheus can't scrape Flask metrics

**Check:**
1. Flask app is running: `docker ps | grep library_flask`
2. Metrics endpoint works: `curl http://localhost:5000/metrics`
3. Check Prometheus targets: http://localhost:9090/targets
4. Check container network: `docker network inspect library-management-system_library-network`

**Solution:**
```bash
# Restart Flask container
docker-compose restart flask

# Check Flask logs
docker-compose logs flask
```

### Grafana dashboard shows "No Data"

**Check:**
1. Prometheus datasource is working:
   - Grafana → Configuration → Data Sources → Prometheus → Test
2. Time range is appropriate (try "Last 15 minutes")
3. Queries are returning data in Prometheus: http://localhost:9090

**Solution:**
```bash
# Restart Grafana
docker-compose restart grafana

# Re-provision datasources
docker-compose down
docker-compose up -d
```

### Can't access Grafana at localhost:3000

**Check:**
```bash
# Verify container is running
docker ps | grep library_grafana

# Check port mapping
docker port library_grafana

# Check logs
docker-compose logs grafana
```

## Advanced Configuration

### Adding Alerting

1. Create alert rules in `prometheus/alert_rules.yml`:

```yaml
groups:
  - name: flask_alerts
    interval: 30s
    rules:
      - alert: HighErrorRate
        expr: rate(flask_http_request_total{status=~"5.."}[5m]) > 0.1
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
```

2. Uncomment alert rules in `prometheus.yml`
3. Configure Alertmanager (optional)

### Adding More Exporters

**MySQL Exporter:**
Uncomment mysql scrape config in `prometheus.yml` and add to `docker-compose.yml`:

```yaml
  mysql-exporter:
    image: prom/mysqld-exporter:latest
    container_name: library_mysql_exporter
    environment:
      DATA_SOURCE_NAME: "root:root@(mysql:3306)/"
    ports:
      - "9104:9104"
    networks:
      - library-network
    depends_on:
      - mysql
```

## Retention and Storage

### Prometheus Data Retention

Default: 15 days

Change in `docker-compose.yml`:
```yaml
prometheus:
  command:
    - '--storage.tsdb.retention.time=30d'  # Keep 30 days
```

### Grafana Data

Stored in Docker volume `grafana_data`. Persists across container restarts.

**Backup:**
```bash
docker run --rm -v library-management-system_grafana_data:/data -v $(pwd):/backup ubuntu tar czf /backup/grafana-backup.tar.gz -C /data .
```

**Restore:**
```bash
docker run --rm -v library-management-system_grafana_data:/data -v $(pwd):/backup ubuntu tar xzf /backup/grafana-backup.tar.gz -C /data
```

## Security Considerations

### Production Deployment

1. **Change default Grafana password:**
   ```yaml
   environment:
     - GF_SECURITY_ADMIN_PASSWORD=<strong-password>
   ```

2. **Enable authentication on Prometheus:**
   Use reverse proxy with basic auth

3. **Use HTTPS:**
   Configure TLS certificates in Grafana and Nginx

4. **Restrict network access:**
   Don't expose ports 9090 and 3000 publicly

5. **Set up proper user roles in Grafana:**
   Create read-only viewers for dashboards

## Monitoring Best Practices

1. **Set up alerts** for critical metrics (error rate, response time)
2. **Monitor trends** over time, not just current values
3. **Create SLOs** (Service Level Objectives) based on metrics
4. **Document** what each metric means for your team
5. **Review dashboards** regularly and remove unused panels
6. **Use labels** effectively in Prometheus for filtering

## Resources

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [prometheus-flask-exporter](https://github.com/rycus86/prometheus_flask_exporter)
- [PromQL Basics](https://prometheus.io/docs/prometheus/latest/querying/basics/)

## Support

For issues related to monitoring:
1. Check Docker container logs: `docker-compose logs prometheus grafana`
2. Verify network connectivity between containers
3. Check configuration files for syntax errors
4. Review the troubleshooting section above
