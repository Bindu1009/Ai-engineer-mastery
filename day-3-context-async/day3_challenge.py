"""
DAY 3 CHALLENGE: Async Rate-Limited API Client

Build a production-ready API client that:
1. Uses context managers for connection management
2. Uses async/await for concurrent requests
3. Implements rate limiting and retries
"""

import asyncio
import time
import random
from typing import List, Dict, Any, Optional
from contextlib import asynccontextmanager
from dataclasses import dataclass

# ============================================
# PART 1: DATA MODELS
# ============================================

@dataclass
class APIResponse:
    """Represents an API response."""
    success: bool
    data: Optional[Dict] = None
    error: Optional[str] = None
    status_code: int = 200
    response_time: float = 0.0

# ============================================
# PART 2: CONTEXT MANAGER FOR API CLIENT
# ============================================

class APIClient:
    """Context manager for API client with auto-cleanup."""
    
    def __init__(self, base_url: str, rate_limit: int = 5):
        self.base_url = base_url
        self.rate_limit = rate_limit
        self.session = None
        self.request_times = []
    
    def __enter__(self):
        print(f"🔌 Connecting to {self.base_url}")
        self.session = {"connected": True, "requests": 0}
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"🔌 Disconnecting from {self.base_url}")
        self.session = None
    
    def _check_rate_limit(self):
        """Check if we're within rate limit."""
        now = time.time()
        self.request_times = [t for t in self.request_times if t > now - 1]
        
        if len(self.request_times) >= self.rate_limit:
            wait_time = 1 - (now - self.request_times[0])
            time.sleep(max(0, wait_time))
        
        self.request_times.append(time.time())
    
    def sync_call(self, endpoint: str) -> APIResponse:
        """Synchronous API call (for comparison)."""
        self._check_rate_limit()
        start = time.time()
        
        # Simulate API call
        time.sleep(random.uniform(0.1, 0.3))
        
        response_time = time.time() - start
        
        if random.random() < 0.9:  # 90% success rate
            return APIResponse(
                success=True,
                data={"endpoint": endpoint, "message": "Success"},
                status_code=200,
                response_time=response_time
            )
        else:
            return APIResponse(
                success=False,
                error="Internal server error",
                status_code=500,
                response_time=response_time
            )


# ============================================
# PART 3: ASYNC CONTEXT MANAGER
# ============================================

@asynccontextmanager
async def async_api_client(base_url: str, rate_limit: int = 10):
    """Async context manager for API client."""
    print(f"🔌 Async connecting to {base_url}")
    client = {"connected": True, "requests": 0}
    
    try:
        yield client
    finally:
        print(f"🔌 Async disconnecting from {base_url}")
        client["connected"] = False


class AsyncRateLimiter:
    """Async rate limiter using semaphore."""
    
    def __init__(self, max_concurrent: int = 5, max_per_second: int = 10):
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.max_per_second = max_per_second
        self.request_times = []
    
    async def acquire(self):
        """Acquire permission to make a request."""
        async with self.semaphore:
            # Rate limiting per second
            now = time.time()
            self.request_times = [t for t in self.request_times if t > now - 1]
            
            if len(self.request_times) >= self.max_per_second:
                wait_time = 1 - (now - self.request_times[0])
                await asyncio.sleep(max(0, wait_time))
            
            self.request_times.append(time.time())
            return True


async def async_api_call(
    endpoint: str,
    rate_limiter: AsyncRateLimiter,
    call_id: int
) -> APIResponse:
    """Make an async API call with rate limiting."""
    await rate_limiter.acquire()
    
    start = time.time()
    
    # Simulate API call
    await asyncio.sleep(random.uniform(0.1, 0.3))
    
    response_time = time.time() - start
    
    # 90% success rate
    if random.random() < 0.9:
        return APIResponse(
            success=True,
            data={"endpoint": endpoint, "call_id": call_id},
            status_code=200,
            response_time=response_time
        )
    else:
        return APIResponse(
            success=False,
            error="Rate limit exceeded",
            status_code=429,
            response_time=response_time
        )


# ============================================
# PART 4: RETRY DECORATOR (Using what you learned Day 2)
# ============================================

def retry_async(max_attempts: int = 3, delay: float = 1.0):
    """Decorator to retry async functions."""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"  🔁 Retry {attempt + 1}/{max_attempts}: {e}")
                    if attempt < max_attempts - 1:
                        await asyncio.sleep(delay)
            raise last_exception
        return wrapper
    return decorator


@retry_async(max_attempts=3, delay=0.5)
async def reliable_api_call(endpoint: str, call_id: int) -> APIResponse:
    """API call with automatic retry."""
    # Simulate a flaky API (70% success on first try)
    if random.random() < 0.3:
        raise Exception("Temporary network error")
    
    await asyncio.sleep(0.2)
    return APIResponse(
        success=True,
        data={"endpoint": endpoint, "call_id": call_id},
        status_code=200
    )


# ============================================
# PART 5: BENCHMARK SYNC VS ASYNC
# ============================================

def benchmark_sync():
    """Benchmark synchronous API calls."""
    print("\n📊 SYNC BENCHMARK")
    start = time.time()
    
    with APIClient("https://api.example.com", rate_limit=100) as client:
        results = []
        for i in range(20):
            result = client.sync_call(f"/api/data/{i}")
            results.append(result)
    
    success_count = sum(1 for r in results if r.success)
    total_time = time.time() - start
    
    print(f"  Success rate: {success_count}/20")
    print(f"  Total time: {total_time:.2f}s")
    
    return total_time


async def benchmark_async():
    """Benchmark asynchronous API calls."""
    print("\n📊 ASYNC BENCHMARK")
    start = time.time()
    
    rate_limiter = AsyncRateLimiter(max_concurrent=10, max_per_second=100)
    
    tasks = [
        async_api_call(f"/api/data/{i}", rate_limiter, i)
        for i in range(20)
    ]
    
    results = await asyncio.gather(*tasks)
    
    success_count = sum(1 for r in results if r.success)
    total_time = time.time() - start
    
    print(f"  Success rate: {success_count}/20")
    print(f"  Total time: {total_time:.2f}s")
    
    return total_time


# ============================================
# PART 6: MAIN CHALLENGE
# ============================================

async def run_challenge():
    """Run the complete challenge."""
    print("=" * 70)
    print("🚀 DAY 3 CHALLENGE: ASYNC RATE-LIMITED API CLIENT")
    print("=" * 70)
    
    # Part 1: Demonstrate context manager
    print("\n[Part 1] Context Manager Demo")
    with APIClient("https://api.example.com") as client:
        result = client.sync_call("/health")
        print(f"  Sync call result: {result.success}")
    
    # Part 2: Demonstrate async context manager
    print("\n[Part 2] Async Context Manager Demo")
    async with async_api_client("https://api.example.com") as client:
        print(f"  Client connected: {client['connected']}")
    
    # Part 3: Demonstrate retry decorator
    print("\n[Part 3] Retry Decorator Demo")
    try:
        result = await reliable_api_call("/important", 1)
        print(f"  ✅ Retry succeeded: {result.success}")
    except Exception as e:
        print(f"  ❌ Retry failed: {e}")
    
    # Part 4: Benchmark comparison
    print("\n[Part 4] Performance Comparison")
    
    sync_time = benchmark_sync()
    async_time = await benchmark_async()
    
    speedup = sync_time / async_time
    print(f"\n  🚀 Async is {speedup:.2f}x faster!")
    
    # Part 5: Concurrent batch processing
    print("\n[Part 5] Concurrent Batch Processing")
    
    rate_limiter = AsyncRateLimiter(max_concurrent=5, max_per_second=20)
    
    # Make 50 concurrent API calls
    batch_start = time.time()
    batch_tasks = [
        async_api_call(f"/batch/{i}", rate_limiter, i)
        for i in range(50)
    ]
    batch_results = await asyncio.gather(*batch_tasks)
    batch_time = time.time() - batch_start
    
    success_count = sum(1 for r in batch_results if r.success)
    avg_response_time = sum(r.response_time for r in batch_results) / len(batch_results)
    
    print(f"  Processed 50 requests in {batch_time:.2f}s")
    print(f"  Success rate: {success_count}/50")
    print(f"  Average response time: {avg_response_time:.3f}s")
    print(f"  Throughput: {50/batch_time:.1f} requests/second")
    
    # Summary
    print("\n" + "=" * 70)
    print("🎉 CHALLENGE COMPLETE!")
    print("=" * 70)
    print("\nSkills demonstrated:")
    print("  ✅ Class-based context managers")
    print("  ✅ Generator-based context managers (@asynccontextmanager)")
    print("  ✅ Async/await fundamentals")
    print("  ✅ Concurrent API calls with asyncio.gather()")
    print("  ✅ Rate limiting with semaphores")
    print("  ✅ Retry logic with async decorator")
    print("  ✅ Performance optimization (async is faster)")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(run_challenge())