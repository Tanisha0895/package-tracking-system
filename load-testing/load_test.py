import requests
import time
import json
import statistics
import sys

URL = "https://7oonmpd91g.execute-api.us-west-1.amazonaws.com/dev/events"
TOKEN="eyJraWQiOiI5eHA3S2V5RXVaUEMxN2l4dHpwQ0x4VXlaUkFMM2VlWXAzQkJCMGFqTmFrPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiI3OWY5MTk2ZS0wMGMxLTcwNzEtOGNmOC1lNjI5NTBmYjNlZjUiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiaXNzIjoiaHR0cHM6Ly9jb2duaXRvLWlkcC51cy13ZXN0LTEuYW1hem9uYXdzLmNvbS91cy13ZXN0LTFfdzlob2doN2QxIiwiY29nbml0bzp1c2VybmFtZSI6Ijc5ZjkxOTZlLTAwYzEtNzA3MS04Y2Y4LWU2Mjk1MGZiM2VmNSIsIm9yaWdpbl9qdGkiOiI5MzRjM2U2YS03MTdkLTQyYTUtYWExYy1kZTM1ZGY2MjJjN2EiLCJhdWQiOiI3c2dtb3FhN2luNWx1NjMyczUzb3Q5OXNtZyIsImV2ZW50X2lkIjoiOWQ5YWEzMDYtMzQ1Zi00YTVjLWExZTEtZGNiYWQzN2Q0ODM4IiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE3OTA3NTI4MTMsImV4cCI6MTc5MDc1NjQxMywiaWF0IjoxNzkwNzUyODE0LCJqdGkiOiJhNGE3YjNjYy05NTYyLTRlMzYtYWFmYS1jNDZhNmQ4MWMxNDYiLCJlbWFpbCI6InRhbmlzaGF0aGFrdXIwODk1QGdtYWlsLmNvbSJ9.EsQgAZ5fpDUk2i0LWOlhyPAW72-PF73HZCV_YxU7qK7gpuRoav7YRiI9HridRuzKlJl9zXWwspY_locf4H9pvKJ8_2FvKk0jgvlLSJO9c25MaMhXgbpqc3ExmsALHDmpB_naMipHaE8mX1ZxzShRfQDVWzSbhDy6axFpu5PWFaNP2C5LqslPvHCJyN_2RX1NVTbjXNaGLBvGbsRDk6GhkhWDOsG9J_D35-jbu5OIMWnxHb3xXC4PhM0qme0jtjBo_PbMTkjIdnOcUd9NdxLU3JliOpVhH2EPCadIdbANszxqHPWDmXAao9azAJXcQu53cBYfmWE3YrHylCsTKYeH5g"

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": TOKEN
}

def send_event(package_id, event_id, timestamp):
    payload = {
        "packageId": package_id,
        "eventId": event_id,
        "status": "SHIPPED",
        "eventTimestamp": timestamp
    }
    start = time.time()
    try:
        resp = requests.post(URL, headers=HEADERS, json=payload, timeout=10)
        latency = (time.time() - start) * 1000  # ms
        return resp.status_code, latency
    except Exception as e:
        latency = (time.time() - start) * 1000
        return None, latency

def run_load_test(num_requests, label):
    print(f"\n=== {label} LOAD TEST: {num_requests} requests ===")
    latencies = []
    success_count = 0
    fail_count = 0

    overall_start = time.time()

    for i in range(num_requests):
        package_id = f"LOADTEST-{label}-{i}"
        event_id = f"evt-{label}-{i}"
        timestamp = int(time.time() * 1000) + i  # ensure increasing timestamps

        status_code, latency = send_event(package_id, event_id, timestamp)
        latencies.append(latency)

        if status_code == 200:
            success_count += 1
        else:
            fail_count += 1
            print(f"  Request {i} failed: status={status_code}")

    overall_duration = time.time() - overall_start

    print(f"\nResults for {label} ({num_requests} requests):")
    print(f"  Total time: {overall_duration:.2f}s")
    print(f"  Success: {success_count}, Failed: {fail_count}")
    print(f"  Success rate: {(success_count/num_requests)*100:.1f}%")
    print(f"  Avg latency: {statistics.mean(latencies):.2f}ms")
    print(f"  Min latency: {min(latencies):.2f}ms")
    print(f"  Max latency: {max(latencies):.2f}ms")
    print(f"  Throughput: {num_requests/overall_duration:.2f} req/sec")

if __name__ == "__main__":
    level = sys.argv[1] if len(sys.argv) > 1 else "low"

    if level == "low":
        run_load_test(10, "LOW")
    elif level == "medium":
        run_load_test(100, "MEDIUM")
    elif level == "high":
        run_load_test(500, "HIGH")