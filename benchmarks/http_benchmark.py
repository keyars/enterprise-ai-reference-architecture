"""Small standard-library benchmark for the health endpoint.

Usage after starting the API:
    python benchmarks/http_benchmark.py

This is a measurement helper, not a production load-testing system.
"""

import statistics
import time
import urllib.request

URL = "http://127.0.0.1:8000/health"
REQUESTS = 20


def main() -> None:
    samples: list[float] = []
    for _ in range(REQUESTS):
        started = time.perf_counter()
        with urllib.request.urlopen(URL, timeout=5) as response:
            if response.status != 200:
                raise RuntimeError(f"Unexpected status: {response.status}")
        samples.append((time.perf_counter() - started) * 1000)
    print(f"requests={REQUESTS}")
    print(f"min_ms={min(samples):.2f}")
    print(f"median_ms={statistics.median(samples):.2f}")
    print(f"max_ms={max(samples):.2f}")


if __name__ == "__main__":
    main()
