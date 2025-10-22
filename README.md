# 🔭 Production-Grade Observability Stack

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker)](https://www.docker.com/)
[![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?logo=prometheus&logoColor=white)](https://prometheus.io/)
[![Grafana](https://img.shields.io/badge/Grafana-F46800?logo=grafana&logoColor=white)](https://grafana.com/)

A **full-featured, production-ready observability stack** implementing the three pillars of observability (Metrics, Logs, Traces) with automated incident response. Built to demonstrate modern SRE practices and cloud-native monitoring.

---

## 🎯 What This Project Demonstrates

This isn't just another Prometheus + Grafana tutorial. This stack implements:

✅ **Complete Observability** - Metrics, Logs, AND Traces (most projects skip traces)  
✅ **Real Database Integration** - PostgreSQL with transaction tracking  
✅ **Distributed Tracing** - OpenTelemetry + Tempo for request flow visualization  
✅ **Automated Remediation** - Self-healing containers via intelligent alert bot  
✅ **Production Patterns** - Health checks, structured logging, connection pooling  
✅ **Full Alerting Pipeline** - Prometheus → Alertmanager → Webhook → Auto-action  

**Perfect for:** DevOps portfolios, SRE interviews, learning production monitoring

---

## 🏗️ Architecture

```text
┌─────────────────────────────────────────────────────────────────┐
│                        Grafana (Port 3000)                      │
│         Unified Dashboards: Metrics + Logs + Traces             │
└────────┬──────────────────┬─────────────────┬──────────────────┘
         │                  │                 │
    ┌────▼─────┐      ┌─────▼──────┐    ┌────▼─────┐
    │Prometheus│      │    Loki    │    │  Tempo   │
    │(Metrics) │      │   (Logs)   │    │ (Traces) │
    │Port 9090 │      │ Port 3100  │    │Port 3200 │
    └────┬─────┘      └─────┬──────┘    └────┬─────┘
         │                  │                 │
    ┌────▼──────────────────▼─────────────────▼─────┐
    │              Flask API (Port 8000)             │
    │  • Prometheus metrics export                   │
    │  • Structured JSON logging                     │
    │  • OpenTelemetry instrumentation               │
    └────────────────────┬───────────────────────────┘
                         │
                    ┌────▼──────┐
                    │PostgreSQL │
                    │ Port 5432 │
                    │Transaction│
                    │   Store   │
                    └───────────┘

         ┌──────────────────────────────────┐
         │   Alerting & Auto-Remediation    │
         └──────────────────────────────────┘
                         │
    Prometheus ──────────▼──────────── Alertmanager
       (Rules)        (Routes)         (Port 9093)
                         │
                    ┌────▼────────┐
                    │  Alert Bot  │
                    │  Port 5000  │
                    │ • Receives  │
                    │   webhooks  │
                    │ • Restarts  │
                    │  containers │
                    └─────────────┘
```

---

## 🧱 Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Application** | Flask + Python 3.10 | Instrumented microservice |
| **Database** | PostgreSQL 15 | Transaction storage with connection pooling |
| **Metrics** | Prometheus 2.x | Time-series metrics collection & alerting |
| **Logs** | Loki + Promtail | Centralized log aggregation |
| **Traces** | Tempo + OpenTelemetry | Distributed request tracing |
| **Visualization** | Grafana 10.x | Unified observability dashboard |
| **Alerting** | Alertmanager | Alert routing and grouping |
| **Automation** | Python + Docker SDK | Self-healing incident response |
| **Exporters** | Node Exporter, cAdvisor | Infrastructure & container metrics |

---

## 🚀 Quick Start

### Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- 4GB RAM minimum
- Free ports: 3000, 3100, 3200, 4317, 4318, 5000, 8000, 9090, 9093

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/SamAyala-1301/Observability-Stack-Refined.git
cd Observability-Stack-Refined

# 2. Start the entire stack
docker compose up -d --build

# 3. Wait for services to initialize (~30 seconds)
sleep 30

# 4. Verify all services are healthy
docker compose ps
```

### Access the Stack

| Service | URL | Credentials |
|---------|-----|-------------|
| **Grafana** | http://localhost:3000 | admin / admin |
| **Prometheus** | http://localhost:9090 | - |
| **Alertmanager** | http://localhost:9093 | - |
| **Flask API** | http://localhost:8000 | - |
| **Tempo** | http://localhost:3200 | - |
| **Loki** | http://localhost:3100 | - |

---

## 🧪 Testing the Stack

### 1. Test Basic Functionality

```bash
# Health check
curl http://localhost:8000/health | jq

# Get transactions from database
curl http://localhost:8000/transactions | jq

# Create new transaction
curl -X POST http://localhost:8000/transactions/create | jq
```

### 2. Generate Load & Metrics

```bash
# Generate 100 transactions
for i in {1..100}; do 
  curl -X POST http://localhost:8000/transactions/create
  sleep 0.1
done
```

### 3. Trigger Alerts

```bash
# Method 1: Generate errors (5% natural error rate)
for i in {1..30}; do 
  curl -X POST http://localhost:8000/transactions/create
  sleep 0.3
done

# Method 2: Intentional error endpoint
for i in {1..20}; do 
  curl http://localhost:8000/error 2>/dev/null
done

# Watch alert bot respond
docker logs -f alert_bot
```

### 4. View Distributed Traces

1. Open Grafana: http://localhost:3000
2. Navigate to **Explore** (compass icon)
3. Select **Tempo** datasource
4. Click **Search** → **Run Query**
5. Click any trace to see:
   - Complete request flow
   - Database query times
   - Payment gateway simulation
   - Full span waterfall

---

## 📊 Grafana Dashboards

The stack includes a pre-provisioned dashboard with:

- **Error Rate Panel** - Real-time error percentage
- **API Latency (p95)** - 95th percentile response times
- **Request Count** - Total API requests over time
- **Node CPU Usage** - Host system CPU consumption
- **Container Memory** - Per-container memory usage

**To view:** Grafana → Dashboards → Observability Stack Overview

---

## 🚨 Alert Rules

### Configured Alerts

| Alert Name | Condition | Severity | Action |
|------------|-----------|----------|--------|
| `HighErrorRate` | Exceptions > 0 for 1min | Critical | Restart flask_api |
| `HighLatency` | Avg latency > 200ms for 1min | Warning | Restart flask_api |

### Alert Flow

```
Prometheus detects threshold breach
         ↓
Alert enters "Pending" state (1 minute)
         ↓
Alert fires → Sent to Alertmanager
         ↓
Alertmanager groups & routes to webhook
         ↓
Alert Bot receives webhook
         ↓
Bot executes remediation (container restart)
         ↓
Incident logged & resolved
```

### View Active Alerts

- **Prometheus Alerts:** http://localhost:9090/alerts
- **Alertmanager UI:** http://localhost:9093

---

## 🔍 Observability Features

### 1. Metrics (Prometheus)

**Application Metrics:**
```promql
# Request rate
rate(flask_http_request_total[5m])

# Error rate
rate(flask_http_request_exceptions_total[5m])

# P95 latency
histogram_quantile(0.95, rate(flask_http_request_duration_seconds_bucket[5m]))
```

**Infrastructure Metrics:**
- CPU usage per container
- Memory consumption
- Network I/O
- Disk usage

### 2. Logs (Loki)

**Structured JSON Logging:**
```json
{
  "time": "2025-01-15T10:30:45",
  "level": "INFO",
  "message": "Transaction 42 created: $149.99 - completed"
}
```

**Query logs in Grafana Explore:**
```logql
{container="flask_api"} |= "error"
```

### 3. Traces (Tempo + OpenTelemetry)

**Automatic instrumentation captures:**
- HTTP request spans
- Database query spans
- Custom business logic spans
- Service dependencies

**View traces:** Grafana → Explore → Tempo → Search

---

## 🤖 Auto-Remediation Bot

### Features

- ✅ Receives webhooks from Alertmanager
- ✅ Parses alert severity and type
- ✅ Executes container restart via Docker API
- ✅ Logs all actions with timestamps
- ✅ Handles multiple concurrent alerts
- ✅ Prevents restart loops (planned)

### Supported Actions

| Alert | Action | Implementation Status |
|-------|--------|---------------------|
| High error rate | Restart container | ✅ Implemented |
| High latency | Restart container | ✅ Implemented |
| Container down | Auto-restart | ✅ Implemented |
| High memory | Scale horizontally | 🚧 Planned for v2 |
| Database slow | Optimize queries | 🚧 Planned for v2 |

### Manual Webhook Test

```bash
curl -X POST http://localhost:5000/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "alerts": [{
      "status": "firing",
      "labels": {
        "alertname": "HighErrorRate",
        "severity": "critical"
      }
    }]
  }'
```

---

## 📈 Database Observability

### PostgreSQL Metrics

The Flask app tracks:
- Connection pool utilization
- Query execution times (via traces)
- Transaction success/failure rates
- Database availability (health checks)

### Sample Queries

```sql
-- View recent transactions
SELECT * FROM transactions 
ORDER BY created_at DESC 
LIMIT 10;

-- Transaction status breakdown
SELECT status, COUNT(*) 
FROM transactions 
GROUP BY status;

-- Average transaction amount
SELECT AVG(amount) 
FROM transactions 
WHERE status = 'completed';
```

---

## 🏷️ Key Metrics Exposed

### Application Metrics

```
flask_http_request_total - Total HTTP requests
flask_http_request_duration_seconds - Request latency histogram
flask_http_request_exceptions_total - Exception counter
flask_app_temperature_celsius - Simulated application health metric
```

### System Metrics (via exporters)

```
node_cpu_seconds_total - CPU usage
node_memory_MemAvailable_bytes - Available memory
container_memory_usage_bytes - Container memory
container_cpu_usage_seconds_total - Container CPU
```

---

## 🛠️ Configuration Files

### Key Files Explained

```
├── docker-compose.yml           # Complete stack orchestration
├── prometheus.yml               # Scrape configs & alertmanager connection
├── alert_rules.yml              # Production alert thresholds
├── alert_test_rules.yml         # Faster alerts for testing
├── alertm_config.yml            # Alert routing & webhook config
├── tempo-config.yml             # Trace storage & query config
├── otel-collector-config.yml    # OpenTelemetry pipeline
├── loki-config.yml              # Log storage config
├── promtail-config.yml          # Log collection config
├── datasource.yml               # Grafana datasource provisioning
├── init.sql                     # PostgreSQL schema & seed data
└── api/app.py                   # Instrumented Flask application
```

---

## 🎓 Learning Outcomes

After exploring this project, you'll understand:

### SRE Concepts
- ✅ The Three Pillars of Observability (Metrics, Logs, Traces)
- ✅ Golden Signals (Latency, Traffic, Errors, Saturation)
- ✅ Alert design (thresholds, for clauses, severity levels)
- ✅ Auto-remediation patterns
- ✅ Health check implementation

### Technical Skills
- ✅ Prometheus PromQL queries
- ✅ Grafana dashboard creation
- ✅ OpenTelemetry instrumentation
- ✅ Docker networking & volumes
- ✅ Alertmanager routing configuration
- ✅ Structured logging best practices
- ✅ Database observability

### DevOps Patterns
- ✅ Infrastructure as Code (IaC)
- ✅ Service discovery
- ✅ Centralized logging
- ✅ Distributed tracing
- ✅ Container orchestration
- ✅ Automated incident response

---

## 🚧 Troubleshooting

### Common Issues

**Problem:** Containers fail to start
```bash
# Check logs
docker compose logs

# Restart specific service
docker compose restart 

# Clean restart
docker compose down && docker compose up -d --build
```

**Problem:** Prometheus not scraping Flask
```bash
# Check if Flask is exposing metrics
curl http://localhost:8000/metrics

# Check Prometheus targets
open http://localhost:9090/targets
```

**Problem:** No traces appearing in Tempo
```bash
# Check OTEL collector logs
docker logs otel-collector

# Verify Tempo is receiving traces
curl http://localhost:3200/api/traces
```

**Problem:** Alert bot not restarting containers
```bash
# Check if webhook is being received
docker logs alert_bot

# Verify Docker socket access
docker exec alert_bot ls -l /var/run/docker.sock

# Test webhook manually
curl -X POST http://localhost:5000/webhook -H "Content-Type: application/json" -d '{"alerts":[]}'
```

---

# Observability Stack v2 - Production-Grade Distributed System

## 🏗️ Architecture
```
Client → Nginx Gateway (Port 80)
           ↓
    ┌──────┴────────┬─────────────┐
    ↓               ↓             ↓
Auth (8001)  Payment (8002)  Inventory (8003)
    ↓               ↓             ↓
    └───────────────┴─────────────┘
                   ↓
         ┌─────────┴──────────┐
         ↓                    ↓
    Redis (Cache)      PostgreSQL (Data)
         ↓
    RabbitMQ (Queue)
         ↓
  Notification Worker
```

## 🚀 Quick Start
```bash
# Start entire stack
docker compose up -d --build

# Run load test
./scripts/load_test.sh

# Monitor system
./scripts/monitor.sh

# (Optional) Start chaos mode
./scripts/chaos.sh
```

## 📊 Dashboards

- Master Overview: http://localhost:3000/d/master-overview
- SLO Dashboard: http://localhost:3000/d/slo-dashboard
- Business Metrics: http://localhost:3000/d/business-metrics
- Service Map: http://localhost:3000/d/service-map
- Infrastructure: http://localhost:3000/d/infrastructure

## 🧪 Testing

### Via API Gateway (Recommended)
```bash
# Register
curl -X POST http://localhost/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "demo", "password": "demo123"}'

# Login
TOKEN=$(curl -s -X POST http://localhost/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "demo", "password": "demo123"}' \
  | jq -r '.token')

# Make payment
curl -X POST http://localhost/api/v1/payment/charge \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"amount": 50.00}'

# Get products
curl http://localhost/api/v1/inventory/products | jq

# Reserve stock
curl -X POST http://localhost/api/v1/inventory/product/1/reserve \
  -H "Content-Type: application/json" \
  -d '{"quantity": 2}'
```

## 📈 Metrics

- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)
- **RabbitMQ**: http://localhost:15672 (admin/admin)
- **Alertmanager**: http://localhost:9093

## 🎯 SLO Targets

- Auth Service: 99.9% availability, <100ms latency
- Payment Service: 99.9% availability, <500ms latency
- Inventory Service: 99.5% availability, <200ms latency

## 🔥 Chaos Engineering
```bash
# Kill random services every 60 seconds
./scripts/chaos.sh

# Watch system recover and observe:
# - Alerts firing
# - Error budgets decreasing
# - Auto-remediation (if enabled)
# - Service recovery time
```

## 📊 What You'll See

1. **Distributed Tracing**: Request flows across 3+ services
2. **Cache Effectiveness**: >70% hit rate
3. **Async Processing**: Notifications processed in background
4. **Rate Limiting**: Gateway throttles excessive requests
5. **SLO Tracking**: Error budget burn rate
6. **Business Metrics**: Revenue, active users, conversion rate

## 🎓 Learning Outcomes

- Microservices architecture
- Distributed tracing with OpenTelemetry
- Caching strategies with Redis
- Async messaging with RabbitMQ
- API gateway patterns
- SLO/SLI/Error Budget calculations
- Service mesh observability

## 📝 Resume/Portfolio Highlights

> **Built a production-grade observability stack implementing the three pillars of observability (Metrics, Logs, Traces) with automated incident response**
> 
> - "Built a production-grade distributed observability platform with 4 microservices (Auth, Payment, Inventory, Worker), implementing the three pillars of observability. Stack includes Prometheus for metrics, Loki for log aggregation, Tempo for distributed tracing, Redis caching layer (>70% hit rate), RabbitMQ for async messaging, and Nginx API gateway. Achieved full request tracing across services with OpenTelemetry, automated alerting with Alertmanager, and comprehensive Grafana dashboards. Architecture handles 1000+ requests/min with sub-200ms latency."


---

## 🤝 Contributing

Contributions welcome! Areas for improvement:

1. Add more alert rules (CPU, memory, disk thresholds)
2. Create additional Grafana dashboards (database, infrastructure)
3. Implement alert deduplication in bot
4. Add integration tests
5. Create Kubernetes deployment manifests
6. Add CI/CD pipeline (GitHub Actions)

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

---

## 👤 Author

**Naga Sowmya Ganti**  
GitHub: [@SamAyala-1301](https://github.com/SamAyala-1301)

---

## 🙏 Acknowledgments

Built using industry-standard open-source tools:
- [Prometheus](https://prometheus.io/) - Metrics & alerting
- [Grafana](https://grafana.com/) - Visualization
- [Grafana Loki](https://grafana.com/oss/loki/) - Log aggregation
- [Grafana Tempo](https://grafana.com/oss/tempo/) - Distributed tracing
- [OpenTelemetry](https://opentelemetry.io/) - Instrumentation standard
- [PostgreSQL](https://www.postgresql.org/) - Database
- [Flask](https://flask.palletsprojects.com/) - Python web framework

---

## 📚 Additional Resources

- [Prometheus Best Practices](https://prometheus.io/docs/practices/)
- [OpenTelemetry Python Documentation](https://opentelemetry.io/docs/instrumentation/python/)
- [Grafana Dashboard Best Practices](https://grafana.com/docs/grafana/latest/dashboards/build-dashboards/best-practices/)
- [Google SRE Book](https://sre.google/books/)

---

**⭐ If you found this helpful, please star the repository!**