\# Load Testing Results



\## Low Level (10 requests)

\- Success rate: 100%

\- Avg latency: 1664.76ms

\- Min latency: 1381.78ms

\- Max latency: 1993.78ms

\- Throughput: 0.60 req/sec



\## Medium Level (100 requests)

\- Success rate: 99.0% (1 failed - timeout)

\- Avg latency: 1959.81ms

\- Min latency: 1367.79ms

\- Max latency: 10654.80ms

\- Throughput: 0.51 req/sec



\## High Level (500 requests)

\- Success rate: 97.4% (13 failed, clustered around requests 389-401)

\- Avg latency: 1702.39ms

\- Min latency: 3.45ms

\- Max latency: 13150.54ms

\- Throughput: 0.59 req/sec



\## Observations

\- System maintains high success rate (97%+) even under high load

\- Failures were clustered (consecutive) rather than randomly scattered, suggesting a transient bottleneck window rather than consistent weakness

\- Latency remains stable across load levels (\~1.6-2s average), showing the async SQS-based architecture absorbs load without major performance degradation

