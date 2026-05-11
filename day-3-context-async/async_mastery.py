"""
DAY 3: ASYNC/AWAIT MASTERY

Write concurrent code for faster I/O operations
"""

import asyncio
import time
import random
from typing import List, Dict, Any

# ============================================
# PART 1: BASIC ASYNC/AWAIT
# ============================================

async def greet(name: str, delay: float) -> str:
    """A simple async function that waits and returns."""
    await asyncio.sleep(delay)  # Non-blocking sleep
    return f"Hello {name}! (waited {delay}s)"

async def basic_async_demo():
    """Demonstrate basic async/await."""
    print("\n" + "=" * 60)
    print("BASIC ASYNC/AWAIT")
    print("=" * 60)
    
    # Method 1: Await one at a time (sequential)
    print("\n[1] Sequential execution")
    start = time.time()
    
    result1 = await greet("Alice", 1)
    result2 = await greet("Bob", 1)
    result3 = await greet("Charlie", 1)
    
    print(f"  {result1}")
    print(f"  {result2}")
    print(f"  {result3}")
    print(f"  Sequential total time: {time.time() - start:.2f}s")
    
    # Method 2: Run concurrently (recommended)
    print("\n[2] Concurrent execution (gather)")
    start = time.time()
    
    results = await asyncio.gather(
        greet("Alice", 1),
        greet("Bob", 1),
        greet("Charlie", 1)
    )
    
    for result in results:
        print(f"  {result}")
    print(f"  Concurrent total time: {time.time() - start:.2f}s")


# ============================================
# PART 2: SIMULATING API CALLS
# ============================================

async def fetch_api(api_name: str, delay: float, success_rate: float = 1.0) -> Dict[str, Any]:
    """Simulate an API call with possible failure."""
    await asyncio.sleep(delay)
    
    if random.random() > success_rate:
        raise Exception(f"{api_name} failed!")
    
    return {
        "api": api_name,
        "data": f"Response from {api_name}",
        "time_taken": delay
    }

async def fetch_all_apis():
    """Fetch multiple APIs concurrently."""
    print("\n" + "=" * 60)
    print("CONCURRENT API CALLS")
    print("=" * 60)
    
    api_calls = [
        fetch_api("Weather API", 0.5),
        fetch_api("News API", 0.8),
        fetch_api("Stock API", 0.3),
        fetch_api("Social API", 0.6),
        fetch_api("Database API", 0.4),
    ]
    
    start = time.time()
    results = await asyncio.gather(*api_calls, return_exceptions=True)
    
    for result in results:
        if isinstance(result, Exception):
            print(f"  ❌ Error: {result}")
        else:
            print(f"  ✅ {result['api']}: {result['data']}")
    
    print(f"\n  Total time: {time.time() - start:.2f}s")
    print(f"  If done sequentially: ~{sum([0.5,0.8,0.3,0.6,0.4])}s")


# ============================================
# PART 3: TASKS AND ASYNCIO.CREATE_TASK
# ============================================

async def worker(name: str, queue: asyncio.Queue):
    """Worker that processes items from a queue."""
    while True:
        item = await queue.get()
        if item is None:  # Poison pill to stop
            queue.task_done()
            break
        
        print(f"  🧑‍💻 Worker {name} processing item {item}")
        await asyncio.sleep(random.uniform(0.1, 0.5))  # Simulate work
        print(f"  ✅ Worker {name} completed item {item}")
        queue.task_done()

async def task_demo():
    """Demonstrate background tasks."""
    print("\n" + "=" * 60)
    print("BACKGROUND TASKS WITH QUEUE")
    print("=" * 60)
    
    queue = asyncio.Queue()
    
    # Create 3 workers
    workers = [
        asyncio.create_task(worker(f"W{i}", queue))
        for i in range(3)
    ]
    
    # Add 10 items to queue
    for i in range(10):
        await queue.put(i)
    
    # Wait for all items to process
    await queue.join()
    
    # Stop workers
    for w in workers:
        await queue.put(None)
    await asyncio.gather(*workers)
    
    print("  ✅ All tasks completed")


# ============================================
# PART 4: TIMEOUTS AND RETRIES
# ============================================

async def slow_api_call() -> str:
    """A slow API call."""
    await asyncio.sleep(3)  # Takes 3 seconds
    return "Important data"

async def timeout_demo():
    """Demonstrate timeout handling."""
    print("\n" + "=" * 60)
    print("TIMEOUT HANDLING")
    print("=" * 60)
    
    try:
        # Wait at most 2 seconds
        result = await asyncio.wait_for(slow_api_call(), timeout=2.0)
        print(f"  ✅ Got result: {result}")
    except asyncio.TimeoutError:
        print("  ⏰ Timeout! API took too long")


async def fetch_with_retry(api_name: str, max_retries: int = 3) -> Any:
    """Fetch API with automatic retry."""
    for attempt in range(max_retries):
        try:
            print(f"  Attempt {attempt + 1}/{max_retries} for {api_name}")
            result = await fetch_api(api_name, 0.5, success_rate=0.6)  # 60% success rate
            return result
        except Exception as e:
            print(f"  ❌ Failed: {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(1)  # Wait before retry
    
    raise Exception(f"{api_name} failed after {max_retries} retries")


async def retry_demo():
    """Demonstrate retry logic."""
    print("\n" + "=" * 60)
    print("RETRY LOGIC")
    print("=" * 60)
    
    try:
        result = await fetch_with_retry("Unreliable API")
        print(f"  ✅ Success: {result}")
    except Exception as e:
        print(f"  ❌ Final failure: {e}")


# ============================================
# PART 5: SEMAPHORES (Rate Limiting)
# ============================================

async def limited_call(semaphore: asyncio.Semaphore, call_id: int):
    """Make a call with rate limiting."""
    async with semaphore:
        print(f"  🚀 Call {call_id} started")
        await asyncio.sleep(0.5)  # Simulate work
        print(f"  ✅ Call {call_id} completed")

async def semaphore_demo():
    """Demonstrate rate limiting with semaphores."""
    print("\n" + "=" * 60)
    print("RATE LIMITING WITH SEMAPHORES")
    print("=" * 60)
    
    # Allow only 2 concurrent calls
    semaphore = asyncio.Semaphore(2)
    
    start = time.time()
    tasks = [limited_call(semaphore, i) for i in range(10)]
    await asyncio.gather(*tasks)
    
    print(f"  Total time: {time.time() - start:.2f}s")
    print(f"  If sequential: 5.0s (10 * 0.5)")


# ============================================
# PART 6: REAL-WORLD WEB SCRAPER
# ============================================

async def fetch_url(session, url: str) -> Dict[str, Any]:
    """Fetch a single URL (simulated)."""
    await asyncio.sleep(random.uniform(0.1, 0.3))  # Simulate network
    
    return {
        "url": url,
        "status": 200,
        "content_length": random.randint(1000, 10000)
    }

async def scrape_websites(urls: List[str]) -> List[Dict]:
    """Scrape multiple websites concurrently."""
    # In real code, use aiohttp.ClientSession()
    tasks = [fetch_url(None, url) for url in urls]
    results = await asyncio.gather(*tasks)
    return results

async def web_scraper_demo():
    """Real-world web scraping example."""
    print("\n" + "=" * 60)
    print("REAL-WORLD: CONCURRENT WEB SCRAPER")
    print("=" * 60)
    
    urls = [
        "https://example.com/page1",
        "https://example.com/page2",
        "https://example.com/page3",
        "https://example.com/page4",
        "https://example.com/page5",
        "https://example.com/page6",
        "https://example.com/page7",
        "https://example.com/page8",
        "https://example.com/page9",
        "https://example.com/page10",
    ]
    
    start = time.time()
    results = await scrape_websites(urls)
    
    for result in results:
        print(f"  ✅ {result['url']}: {result['status']} ({result['content_length']} bytes)")
    
    print(f"\n  Scraped {len(urls)} pages in {time.time() - start:.2f}s")
    print(f"  Sequential time: ~{len(urls) * 0.2}s (20s)")


# ============================================
# PART 7: STREAMS (Processing Data as it Arrives)
# ============================================

async def produce_data(queue: asyncio.Queue, num_items: int):
    """Producer that puts items into queue."""
    for i in range(num_items):
        await asyncio.sleep(random.uniform(0.1, 0.2))
        await queue.put(f"Item-{i}")
        print(f"  📦 Produced Item-{i}")
    await queue.put(None)  # Signal end

async def consume_data(queue: asyncio.Queue):
    """Consumer that processes items from queue."""
    while True:
        item = await queue.get()
        if item is None:
            break
        await asyncio.sleep(0.1)  # Process item
        print(f"  🔧 Processed {item}")
        queue.task_done()

async def stream_demo():
    """Demonstrate streaming data processing."""
    print("\n" + "=" * 60)
    print("STREAMING DATA PROCESSING")
    print("=" * 60)
    
    queue = asyncio.Queue()
    
    # Run producer and consumer concurrently
    producer = asyncio.create_task(produce_data(queue, 10))
    consumer = asyncio.create_task(consume_data(queue))
    
    await producer
    await consumer
    
    print("  ✅ Streaming complete")


# ============================================
# RUN ALL DEMOS
# ============================================

async def main():
    """Run all async demos."""
    await basic_async_demo()
    await fetch_all_apis()
    await task_demo()
    await timeout_demo()
    await retry_demo()
    await semaphore_demo()
    await web_scraper_demo()
    await stream_demo()
    
    print("\n" + "=" * 60)
    print("✅ ALL ASYNC/AWAIT TESTS COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())