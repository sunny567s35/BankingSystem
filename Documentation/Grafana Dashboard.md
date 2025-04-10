# Prometheus and Grafana

Below is an explanation of the queries and monitoring. Each query is described in terms of its purpose and how it helps monitor the `BankingSystem` app.

### Add Prometheus as a DataSource
<img src="https://github.com/user-attachments/assets/2742a966-d0c5-4023-ad64-389b836137b5" width="700" />

---
### Dashboard
<img src="https://github.com/user-attachments/assets/022ad70a-88a1-4e5b-8189-a7c866919bc4" width="700" />
<img src="https://github.com/user-attachments/assets/e996ff51-904d-46a8-9763-0d8546c4b3bf" width="700" />

---
### Query Explanations for BankingSystem App Monitoring 🎉

- **Total Requests (Stat Panel) 📊**
  - **Query**: `sum(increase(django_http_requests_total_by_view_transport_method_total{service=~"^$service$", method=~"$method"}[15m])) by (method)`
  - **Explanation**: This query calculates the total increase in HTTP requests over a 15-minute window, filtered by service and method, and aggregates the results by the `method` label. The `increase` function handles counter resets (e.g., due to server restarts) 📈.
  - **Monitoring Benefit for BankingSystem 🌟**: Tracks the volume of requests (e.g., login, transfers) per HTTP method (GET, POST). Helps identify peak usage times or potential overloads in transaction processing 💸.
<img src="https://github.com/user-attachments/assets/67ce915c-c44a-43fd-b339-7f836cad2252" width="700" />

---
- **Success Rate (Stat Panel) ✅**
  - **Query**: 
    ```
    sum(rate(django_http_responses_total_by_status_view_method_total{namespace=~"$namespace", job=~"$job", view="$view", method=~"$method", status!~"[4-5].*"}[1w])) /
    sum(rate(django_http_responses_total_by_status_view_method_total{namespace=~"$namespace", job=~"$job", view="$view", method=~"$method"}[1w]))
    ```
  - **Explanation**: Computes the success rate by dividing the rate of successful responses (excluding 4xx and 5xx status codes) by the total rate of responses over a 1-week window, filtered by namespace, job, view, and method 📉.
  - **Monitoring Benefit for BankingSystem 🌐**: Ensures high availability of critical operations like account creation or withdrawals. A drop in success rate could indicate issues with payment gateways or server errors ⚠️.
<img src="https://github.com/user-attachments/assets/cb93d39e-4e08-402f-9806-49d5a942f1d3" width="700" />

---
- **Average Request Latency (P50) (Stat Panel) ⏱️**
  - **Query**: 
    ```
    histogram_quantile(0.50, sum(rate(django_http_requests_latency_seconds_by_view_method_bucket{namespace=~"$namespace", job=~"$job", view="$view", method=~"$method"}[$__range])) by (job, le))
    ```
  - **Explanation**: Calculates the 50th percentile (median) latency from the request latency histogram buckets over the selected time range, aggregated by job 📊.
  - **Monitoring Benefit for BankingSystem 💰**: Monitors the median response time for actions like balance checks or fund transfers. Slow P50 latency might suggest database bottlenecks affecting user experience ⏳.
<img src="https://github.com/user-attachments/assets/374d5217-ba04-41ad-a063-c54ff1768bea" width="700" />

---
- **Average Request Latency (P95) (Stat Panel) ⏲️**
  - **Query**: 
    ```
    histogram_quantile(0.95, sum(rate(django_http_requests_latency_seconds_by_view_method_bucket{namespace=~"$namespace", job=~"$job", view="$view", method=~"$method"}[$__range])) by (job, le))
    ```
  - **Explanation**: Determines the 95th percentile latency, representing the upper 5% of request times, using the same histogram data 📈.
  - **Monitoring Benefit for BankingSystem 💳**: Highlights the worst-case latency for 95% of transactions (e.g., loan applications). High P95 values could indicate infrequent but severe performance issues 🛑.
<img src="https://github.com/user-attachments/assets/1707bd9e-a125-400f-bd35-9bc58ef8794c" width="700" />

---
- **Requests (Time Series Panel) 📅**
  - **Query**: `sum(increase(django_http_requests_total_by_view_transport_method_total{service=~"^$service$", view!~"prometheus-django-metrics|healthcheck"}[5m])) by (method, view)`
  - **Explanation**: Tracks the increase in requests over a 5-minute window, excluding `prometheus-django-metrics` and `healthcheck` views, and groups by method and view 📉.
  - **Monitoring Benefit for BankingSystem 🏦**: Visualizes request trends for specific views (e.g., `deposit_view`, `withdraw_view`) over time. Helps detect unusual spikes in activity, such as a surge in withdrawals 📈.
<img src="https://github.com/user-attachments/assets/0cba8af3-a806-4fa0-97f7-f46cba62249c" width="700" />

---
- **Request Latency (Time Series Panel) ⏳**
  - **Queries**:
    - `histogram_quantile(0.50, sum(rate(django_http_requests_latency_seconds_by_view_method_bucket{service=~"^$service$",view!~"prometheus-django-metrics|healthcheck"}[5m])) by (job, le))` (50th percentile)
    - `histogram_quantile(0.95, sum(rate(django_http_requests_latency_seconds_by_view_method_bucket{service=~"^$service$",view!~"prometheus-django-metrics|healthcheck"}[5m])) by (job, le))` (95th percentile)
    - `histogram_quantile(0.99, sum(rate(django_http_requests_latency_seconds_by_view_method_bucket{service=~"^$service$",view!~"prometheus-django-metrics|healthcheck"}[5m])) by (job, le))` (99th percentile)
    - `histogram_quantile(0.999, sum(rate(django_http_requests_latency_seconds_by_view_method_bucket{service=~"^$service$",view!~"prometheus-django-metrics|healthcheck"}[5m])) by (job, le))` (99.9th percentile)
  - **Explanation**: Computes multiple percentile latencies (50, 95, 99, 99.9) from the latency histogram over 5 minutes, excluding specific views 📊.
  - **Monitoring Benefit for BankingSystem 💸**: Provides a comprehensive view of latency distribution for transactions. High 99.9th percentile latency could signal rare but critical delays in high-value transfers 🚨.
<img src="https://github.com/user-attachments/assets/1dace2a2-64cb-4b37-a976-f5a9e1800da8" width="700" />

---
- **Responses (Time Series Panel) 📤**
  - **Query**: `sum(irate(django_http_responses_before_middlewares_total{service=~"^$service$", view!~"prometheus-django-metrics|healthcheck"}[30s])) by(job)`
  - **Explanation**: Measures the instantaneous rate of responses before middlewares over a 30-second window, grouped by job 📈.
  - **Monitoring Benefit for BankingSystem 🏧**: Tracks response rates for jobs handling banking operations (e.g., authentication). A sudden drop might indicate middleware failures affecting login or payment processing ⚡.

- **Response Status (Time Series Panel) 🚦**
  - **Query**: `sum(irate(django_http_responses_total_by_status_total{service=~"^$service$", view!~"prometheus-django-metrics|healthcheck"}[30s])) by(status)`
  - **Explanation**: Calculates the rate of responses by status code over a 30-second window, excluding specific views 📊.
  - **Monitoring Benefit for BankingSystem 💵**: Monitors the distribution of status codes (e.g., 200 OK, 500 Internal Server Error). An increase in 4xx/5xx codes could indicate issues with account management or transaction endpoints 🔔.
<img src="https://github.com/user-attachments/assets/39d4fc4e-0f47-4dae-8087-bb8a46ea38b0" width="700" />

---
- **HTTP Request per View (Pie Chart Panel) 🥧**
  - **Query**: `sum by (view)(rate(django_http_responses_total_by_status_view_method_total[1d]))`
  - **Explanation**: Summarizes the rate of responses over the last day, grouped by view, with some views excluded from the legend 📉.
  - **Monitoring Benefit for BankingSystem 📊**: Shows the proportion of requests across views (e.g., `transfer_view`, `statement`). Helps identify which features (e.g., transfers) are most used or underperforming 🎯.
<img src="https://github.com/user-attachments/assets/b8cd3c48-07c1-4c1c-a6fc-a0ebb5661cdc" width="700" />

---
- **Process CPU Total Process (Time Series Panel) 💻**
  - **Query**: `sum(rate(process_cpu_seconds_total{}[$__rate_interval]))`
  - **Explanation**: Aggregates the rate of CPU seconds used by processes over the selected rate interval 📈.
  - **Monitoring Benefit for BankingSystem 🖥️**: Tracks overall CPU usage, which is critical for handling high transaction volumes. Spikes could indicate resource contention during peak banking hours ⚡.
<img src="https://github.com/user-attachments/assets/864f9e03-4ce2-4cb5-b853-7ea4692745fb" width="700" />

---
