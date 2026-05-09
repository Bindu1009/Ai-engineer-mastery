# AI Engineer Mastery - 10 Week Journey

**Start Date:** May 10, 2026  
**Current Status:** Day 2 Complete ✅

---
---

## 🐍 Day 2: Decorators & Generators (April 21, 2026)

### What I Learned Today

#### Decorators (Functions that modify functions)
- **Timer decorator** - Measure execution time of any function
- **Retry decorator** - Automatically retry failed operations (API calls, database connections)
- **Logger decorator** - Log function calls with arguments and return values
- **Cache decorator** - Store results to avoid recomputing (memoization)
- **Auth decorator** - Check permissions before executing
- **Multiple decorators** - Stacking decorators on a single function

#### Generators (Memory-efficient iteration)
- **`yield` vs `return`** - Generators remember state between calls
- **Memory efficiency** - Generator uses O(1) memory vs list's O(n)
- **Generator expressions** - `(x*2 for x in range(10))` instead of `[x*2 for x in range(10)]`
- **Infinite generators** - Generate Fibonacci, random numbers, etc. forever
- **Generator pipelines** - Chain multiple generators for data processing
- **send() method** - Send values into a running generator

### Code Files Created

| File | What It Does | Lines of Code |
| :--- | :--- | :--- |
| `decorators_mastery.py` | 6 production-ready decorators with examples | ~180 |
| `generators_mastery.py` | 8 generator patterns including infinite and pipelined | ~200 |
| `day2_challenge.py` | Log file analyzer using both decorators and generators | ~120 |

### Key Code Snippets

#### Most Useful Decorator (Retry with backoff)
```python
def retry(max_attempts: int = 3, delay: float = 1.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {attempt} failed: {e}")
                    if attempt == max_attempts:
                        raise
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

@retry(max_attempts=5, delay=2.0)
def call_unstable_api():
    # This will retry 5 times before failing
    pass
