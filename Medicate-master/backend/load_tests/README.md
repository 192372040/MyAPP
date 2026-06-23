# 🏥 Medicate API — Load Testing

> **Baseline / Load Test** | 100 Virtual Users | 1 Minute Duration

---

## 📁 Folder Structure

```
backend/
└── load_tests/
    ├── locustfile.py          ← Virtual user behaviour (tasks, weights)
    ├── run_load_test.py       ← One-click runner: runs Locust + builds Excel
    ├── README.md              ← This file
    └── reports/               ← Generated Excel reports saved here (auto-created)
```

---

## 🚀 How to Run

### Prerequisites
1. **Python 3.8+** must be installed.
2. **Medicate backend** must be running on `http://localhost:5000`.  
   Start it with:
   ```powershell
   cd backend
   python run.py
   ```

### Run the Load Test (One Command)
```powershell
cd backend\load_tests
python run_load_test.py
```

The script will automatically:
- Install `locust` and `openpyxl` if missing
- Spin up **100 virtual users** over 10 seconds
- Run the test for **1 minute**
- Save raw CSV results in this folder
- Generate a professional **Excel report** in `reports/`

---

## ⚙️ Options

| Flag | Default | Description |
|------|---------|-------------|
| `--host` | `http://localhost:5000` | Target server URL |
| `--users` | `100` | Number of concurrent virtual users |
| `--spawn-rate` | `10` | Users added per second during ramp-up |
| `--run-time` | `1m` | Test duration (`1m`, `90s`, `2m`, etc.) |

**Example with custom settings:**
```powershell
python run_load_test.py --host http://localhost:5000 --users 100 --run-time 1m
```

---

## 📊 What the Excel Report Contains

| Sheet | Contents |
|-------|----------|
| 📊 **Summary** | Total requests, failures, RPS, Avg/Min/Max response times, percentiles (p50/p90/p95/p99), SLA verdict |
| 📋 **Endpoint Details** | Per-endpoint breakdown: requests, failures, response times |
| 📈 **Charts** | Bar charts: Response Time per endpoint, RPS per endpoint |
| ⏱ **History** | Per-second timeline of users, RPS, and response times |

---

## 📈 Understanding the Results

### Requests per Second (RPS)
```
120 req/sec
```
Your API handles ~120 requests every second across all 100 users.

### Response Time
| Metric | Meaning |
|--------|---------|
| **Average** | Typical response time for all requests |
| **Min** | Fastest single response |
| **Max** | Slowest single response |
| **p50 (Median)** | 50% of requests are faster than this |
| **p90** | 90% of requests are faster than this |
| **p95** | 95% of requests are faster than this |
| **p99** | 99% of requests are faster than this |

### SLA Thresholds
| Metric | ✅ Pass | ❌ Fail |
|--------|---------|---------|
| Avg Response Time | < 500 ms | ≥ 500 ms |
| Error Rate | < 5% | ≥ 5% |

---

## 🧪 Endpoints Tested

| Category | Endpoint | Weight |
|----------|----------|--------|
| Health | `GET /` | ★★★★★ |
| Auth | `POST /api/admin/login` | ★★★ |
| Auth | `POST /api/doctor/login` | ★★★ |
| Auth | `POST /api/patient/login` | ★★★ |
| Admin | `GET /api/admin/doctors` | ★★ |
| Admin | `GET /api/admin/patients` | ★★ |
| Admin | `GET /api/admin/appointments` | ★★ |
| Doctor | `GET /api/doctor/appointments` | ★★★ |
| Doctor | `GET /api/doctor/prescriptions` | ★★★ |
| Doctor | `GET /api/doctor/slots` | ★★ |
| Doctor | `POST /api/doctor/slots` | ★ |
| Patient | `GET /api/patient/hospitals` | ★★★★ |
| Patient | `GET /api/patient/appointments` | ★★★★ |
| Patient | `GET /api/patient/prescriptions` | ★★★ |
| Patient | `GET /api/patient/hospital/{id}/doctors` | ★★ |
| Patient | `GET /api/patient/doctor/{id}/slots` | ★★ |

> **Weight** = relative frequency of the endpoint being hit. Higher = more realistic traffic.

---

## 🌐 Locust Web UI (Optional)

To use the interactive browser dashboard instead of headless mode:
```powershell
cd backend\load_tests
locust -f locustfile.py --host http://localhost:5000
```
Then open **http://localhost:8089** in your browser and set 100 users.
