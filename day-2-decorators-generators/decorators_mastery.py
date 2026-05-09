"""
DAY 2: DECORATORS MASTERY

Learn by building real, useful decorators
"""

import time
import functools
from typing import Any, Callable

# ============================================
# DECORATOR 1: Timer (Measure execution time)
# ============================================

def timer(func: Callable) -> Callable:
    """Measure how long a function takes to execute."""
    
    @functools.wraps(func)  # Preserves original function name and docstring
    def wrapper(*args, **kwargs) -> Any:
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"⏱️ {func.__name__} took {end - start:.4f} seconds")
        return result
    
    return wrapper


# Using the timer decorator
@timer
def slow_function():
    """This function sleeps for 1 second."""
    time.sleep(1)
    return "Done"

# ============================================
# DECORATOR 2: Retry (Try again if fails)
# ============================================

def retry(max_attempts: int = 3, delay: float = 1.0):
    """Retry a function if it raises an exception."""
    
    def decorator(func: Callable) -> Callable:
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"⚠️ Attempt {attempt} failed: {e}")
                    if attempt == max_attempts:
                        raise
                    time.sleep(delay)
            return None
        
        return wrapper
    
    return decorator


@retry(max_attempts=3, delay=0.5)
def unstable_api():
    """Simulate an API that sometimes fails."""
    import random
    if random.random() < 0.7:  # 70% chance of failure
        raise Exception("API timeout")
    return "Success!"

# ============================================
# DECORATOR 3: Logger (Log function calls)
# ============================================

def logger(func: Callable) -> Callable:
    """Log when a function is called and what it returns."""
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        print(f"📞 Calling {func.__name__} with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"✅ {func.__name__} returned: {result}")
        return result
    
    return wrapper


@logger
def add_numbers(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

# ============================================
# DECORATOR 4: Cache (Memoization)
# ============================================

def cache(func: Callable) -> Callable:
    """Cache results to avoid recomputing."""
    stored_results = {}
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        # Create a key from arguments
        key = str(args) + str(sorted(kwargs.items()))
        
        if key in stored_results:
            print(f"💾 Cache hit for {func.__name__}{args}")
            return stored_results[key]
        
        result = func(*args, **kwargs)
        stored_results[key] = result
        print(f"💾 Cache miss - stored result for {func.__name__}{args}")
        return result
    
    return wrapper


@cache
def expensive_computation(n: int) -> int:
    """Simulate an expensive calculation."""
    print(f"🔢 Computing for {n}...")
    time.sleep(1)  # Simulate heavy work
    return n * n

# ============================================
# DECORATOR 5: Require Login (Authentication)
# ============================================

def require_login(func: Callable) -> Callable:
    """Check if user is logged in before executing."""
    
    # This would normally check a session or token
    user_logged_in = False  # Simulate logged out
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        if not user_logged_in:
            raise PermissionError("You must log in first")
        return func(*args, **kwargs)
    
    return wrapper


@require_login
def view_dashboard():
    """User dashboard - requires login."""
    return "Welcome to your dashboard"

# ============================================
# DECORATOR 6: Multiple decorators together
# ============================================

@timer
@logger
def process_data(data: list) -> list:
    """Process data with multiple decorators."""
    return [x * 2 for x in data]


# ============================================
# TEST ALL DECORATORS
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("TESTING DECORATORS")
    print("=" * 60)
    
    # Test 1: Timer
    print("\n[TEST 1] Timer Decorator")
    slow_function()
    
    # Test 2: Retry
    print("\n[TEST 2] Retry Decorator")
    try:
        result = unstable_api()
        print(f"Final result: {result}")
    except Exception as e:
        print(f"All attempts failed: {e}")
    
    # Test 3: Logger
    print("\n[TEST 3] Logger Decorator")
    add_numbers(5, 3)
    
    # Test 4: Cache
    print("\n[TEST 4] Cache Decorator")
    expensive_computation(10)
    expensive_computation(10)  # This should be cached
    expensive_computation(20)  # New computation
    
    # Test 5: Require Login
    print("\n[TEST 5] Require Login Decorator")
    try:
        view_dashboard()
    except PermissionError as e:
        print(f"❌ Correctly blocked: {e}")
    
    # Test 6: Multiple decorators
    print("\n[TEST 6] Multiple Decorators")
    result = process_data([1, 2, 3, 4, 5])
    print(f"Result: {result}")
    
    print("\n" + "=" * 60)
    print("ALL DECORATOR TESTS COMPLETE")
    print("=" * 60)