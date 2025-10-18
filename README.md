

# ⚙️ Observability Stack — Flask | Prometheus | Grafana | Alertmanager | Automation Bot

A full-featured, containerized **Observability & SRE simulation project** built from the ground up to mimic a production-like monitoring environment.  
It integrates **Flask (as the monitored service)**, **Prometheus & Alertmanager (for metrics and alerting)**, **Grafana (for visualization)**, and a **Python-based automation bot** for self-healing container management.

---

## 🧭 Project Overview

This system demonstrates how **modern SRE teams** monitor applications, visualize health metrics, and automate incident responses — all using open-source tools.  

It’s designed to:
- Simulate **a small microservice ecosystem** (Flask API, worker, database).
- Expose and collect **custom metrics** for latency, errors, and resource usage.
- Visualize everything through **Grafana dashboards**.
- Trigger and route alerts via **Prometheus + Alertmanager**.
- Execute **auto-remediation actions** (restart containers, scale services) using a **Python bot**.

---

## 🧩 Architecture

```text
                        ┌──────────────────────────────┐
                        │        Grafana UI            │
                        │   Dashboards & Alert Views    │
                        └─────────────┬────────────────┘
                                      │
                        ┌─────────────▼────────────────┐
                        │        Prometheus            │
                        │ Scrapes Flask, Node, cAdvisor│
                        │     Applies Alert Rules       │
                        └──────┬────────────────────────┘
                               │
        ┌──────────────────────▼──────────────────────┐
        │               Flask API                    │
        │   /health & /transactions endpoints         │
        │   Exposes metrics for latency, errors       │
        └───────────┬────────────────────────────────┘
                    │
          ┌─────────▼────────┐     ┌───────────┐
          │ PostgreSQL (DB)  │◀────│ Worker Job │
          │ Transaction Store│     │  Inserts   │
          └──────────────────┘     └────────────┘

                               │
                  ┌────────────▼─────────────┐
                  │      Alertmanager        │
                  │ Routes → Slack / Bot     │
                  └────────────┬─────────────┘
                               │
                        ┌──────▼───────┐
                        │ Alert Bot 🤖 │
                        │ Auto-restarts│
                        │  containers  │
                        └──────────────┘
```

---

## 🧱 Tech Stack

| Layer | Tool | Purpose |
|-------|------|----------|
| **App** | Flask | Mock API exposing endpoints and metrics |
| **Database** | PostgreSQL | Stores mock transaction data |
| **Metrics** | Prometheus | Scrapes metrics from API and exporters |
| **Visualization** | Grafana | Pre-provisioned dashboards |
| **Alerting** | Alertmanager | Routes alerts to Slack/email |
| **Automation** | Python Bot | Auto-remediation and scaling |
| **System Metrics** | Node Exporter, cAdvisor | Monitor system and container resources |

---

## ⚙️ Setup & Run

### 1️⃣ Prerequisites
- Docker + Docker Compose installed  
- Free ports: **8000**, **9090**, **9093**, **3000**

### 2️⃣ Clone Repository
```bash
git clone https://github.com/SamAyala-1301/Observability-Stack.git
cd Observability-Stack
```

### 3️⃣ Run Stack
```bash
docker compose up -d --build
```

### 4️⃣ Access Services
| Service | URL | Description |
|----------|-----|-------------|
| Flask API | [http://localhost:8000](http://localhost:8000) | Mock API |
| Prometheus | [http://localhost:9090](http://localhost:9090) | Metrics collection |
| Grafana | [http://localhost:3000](http://localhost:3000) | Dashboards |
| Alertmanager | [http://localhost:9093](http://localhost:9093) | Alert routing |

---

## 🧪 Alert Simulation

To test alerts:
1. Generate high traffic using `hey`:
   ```bash
   hey -n 5000 -c 50 http://localhost:8000/transactions
   ```
2. Or stop a container temporarily:
   ```bash
   docker stop flask_api
   sleep 15
   docker start flask_api
   ```
3. Check Prometheus Alerts page → turns **green → orange → red**
4. Confirm in Alertmanager → alert routes to Slack/bot.

---

## 📊 Dashboards

Grafana provides panels for:
- API latency (p95)
- Request throughput
- Error rates
- Container CPU/memory
- Node health
- Alert status

---

## 🤖 Automation

The alert bot listens for incoming alerts and performs:
- **Container restart**
- **Service scaling**
- **Incident logging**

---

## 🧾 Example Resume Line

> Built a containerized observability system (Prometheus, Grafana, Flask, PostgreSQL) with custom metrics, SLA dashboards, and Alertmanager integration. Implemented Python-based auto-remediation for container failures and worker scaling, simulating self-healing infrastructure.

---

## 🧠 Learning Takeaways

- How to design a **monitoring stack** from scratch  
- Prometheus metric scraping & alert rule writing  
- Grafana dashboard provisioning  
- End-to-end incident flow & automation principles  

---

**Author:** Naga Sowmya Ganti (SamAyala-1301)  
**License:** MIT  