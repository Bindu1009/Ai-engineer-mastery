"""
DAY 2: GENERATORS MASTERY

Learn why generators are memory-efficient
"""

import sys
import time

# ============================================
# PROBLEM: Processing large data with lists
# ============================================

def process_with_list(n: int):
    """
    This creates a list with n numbers in memory.
    For n=10,000,000, this uses ~800MB of RAM
    """
    numbers = [i for i in range(n)]  # ALL numbers in memory at once
    result = 0
    for num in numbers:
        result += num
    return result

def process_with_generator(n: int):
    """
    This creates ONE number at a time.
    Uses almost no memory regardless of n
    """
    def number_generator():
        for i in range(n):
            yield i  # yield = return but remember position
    
    result = 0
    for num in number_generator():  # One number at a time
        result += num
    return result


# ============================================
# BASIC GENERATOR PATTERNS
# ============================================

# Pattern 1: Generator function using yield
def countdown(n: int):
    """Count down from n to 1."""
    print(f"Starting countdown from {n}")
    while n > 0:
        yield n
        n -= 1
    print("Blast off! 🚀")

# Pattern 2: Infinite generator
def fibonacci():
    """Generate Fibonacci numbers forever."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# Pattern 3: Generator with send() (advanced)
def accumulator():
    """Accumulate values sent to the generator."""
    total = 0
    while True:
        value = yield total  # yield returns the current total
        if value is not None:
            total += value

# Pattern 4: Generator expression (like list comprehension)
# List comprehension: [x*2 for x in range(10)]  # Creates list in memory
# Generator expression: (x*2 for x in range(10))  # Creates generator

# ============================================
# PRACTICAL REAL-WORLD GENERATOR EXAMPLES
# ============================================

# Example 1: Read large file line by line
def read_large_file(filepath: str):
    """
    Reads a file without loading entire file into memory.
    Perfect for 10GB log files.
    """
    with open(filepath, 'r') as file:
        for line in file:
            yield line.strip()

# Example 2: Paginate through API results
def paginated_api_calls(base_url: str, page_size: int = 100):
    """
    Simulates fetching paginated API data.
    Yields one page at a time.
    """
    page = 1
    while True:
        # Simulate API call
        print(f"Fetching page {page}...")
        data = [f"Item {i}" for i in range(page * page_size, (page + 1) * page_size)]
        
        if not data:  # No more data
            break
        
        yield data
        page += 1
        
        # Stop after 3 pages for demo
        if page > 3:
            break

# Example 3: Data pipeline with multiple generators
def data_pipeline():
    """Chain generators together for efficient processing."""
    
    # Generator 1: Raw data
    def raw_data():
        for i in range(10):
            yield i
    
    # Generator 2: Clean data
    def clean_data(source):
        for item in source:
            if item % 2 == 0:  # Keep only even numbers
                yield item
    
    # Generator 3: Transform data
    def transform_data(source):
        for item in source:
            yield item * 10
    
    # Chain them
    raw = raw_data()
    cleaned = clean_data(raw)
    transformed = transform_data(cleaned)
    
    return transformed


# ============================================
# DEMONSTRATE MEMORY EFFICIENCY
# ============================================

def demonstrate_memory_usage():
    """Show the memory difference between lists and generators."""
    
    n = 10_000_000  # 10 million numbers
    
    print("\n" + "=" * 60)
    print("MEMORY COMPARISON: List vs Generator")
    print("=" * 60)
    
    # Generator memory
    def gen():
        for i in range(n):
            yield i
    
    gen_obj = gen()
    gen_size = sys.getsizeof(gen_obj)
    print(f"Generator object size: {gen_size} bytes")
    print(f"Generator uses ~{gen_size / 1024:.2f} KB regardless of n={n}")
    
    # List memory (CAUTION: This will use a lot of RAM)
    print(f"\n⚠️ Warning: Creating list of {n} numbers will use ~{n * 28 / 1024 / 1024:.0f} MB")
    answer = input("Run list memory test? (yes/no): ")
    
    if answer.lower() == 'yes':
        list_obj = list(range(n))
        list_size = sys.getsizeof(list_obj)
        print(f"List object size: {list_size / 1024 / 1024:.2f} MB")
    else:
        print("Skipped list test (would use too much memory)")


# ============================================
# TEST ALL GENERATORS
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("TESTING GENERATORS")
    print("=" * 60)
    
    # Test 1: Countdown
    print("\n[TEST 1] Countdown Generator")
    for num in countdown(5):
        print(f"  {num}")
    
    # Test 2: Fibonacci (first 10 numbers)
    print("\n[TEST 2] Fibonacci Generator")
    fib = fibonacci()
    for _ in range(10):
        print(f"  {next(fib)}", end=" ")
    print()
    
    # Test 3: Accumulator with send()
    print("\n[TEST 3] Accumulator with send()")
    acc = accumulator()
    next(acc)  # Initialize generator
    print(f"Send 10: {acc.send(10)}")
    print(f"Send 20: {acc.send(20)}")
    print(f"Send 30: {acc.send(30)}")
    
    # Test 4: Generator expression vs list comprehension
    print("\n[TEST 4] List vs Generator Expression")
    
    # List comprehension (eager)
    list_comp = [x * 2 for x in range(5)]
    print(f"List comprehension: {list_comp}")
    print(f"Type: {type(list_comp)}")
    
    # Generator expression (lazy)
    gen_expr = (x * 2 for x in range(5))
    print(f"Generator expression: {gen_expr}")
    print(f"Type: {type(gen_expr)}")
    print(f"Convert to list: {list(gen_expr)}")
    
    # Test 5: Read large file simulation
    print("\n[TEST 5] Read Large File (Simulated)")
    # Create a test file
    with open("test_large_file.txt", "w") as f:
        for i in range(100):
            f.write(f"Line {i}: This is some sample data\n")
    
    for line in read_large_file("test_large_file.txt"):
        if "50" in line:
            print(f"  Found: {line}")
            break  # We can stop early without reading entire file
    
    # Test 6: Paginated API
    print("\n[TEST 6] Paginated API")
    for page_data in paginated_api_calls("https://api.example.com"):
        print(f"  Got page with {len(page_data)} items")
        print(f"  First item: {page_data[0]}")
    
    # Test 7: Data pipeline
    print("\n[TEST 7] Data Pipeline (Chained Generators)")
    pipeline = data_pipeline()
    results = list(pipeline)
    print(f"Pipeline results: {results}")
    
    # Test 8: Performance comparison
    print("\n[TEST 8] Performance: Process with List vs Generator")
    
    # List version
    start = time.time()
    list_result = process_with_list(10_000_000)
    list_time = time.time() - start
    
    # Generator version
    start = time.time()
    gen_result = process_with_generator(10_000_000)
    gen_time = time.time() - start
    
    print(f"List version: {list_time:.4f} seconds")
    print(f"Generator version: {gen_time:.4f} seconds")
    print(f"Both produce same result: {list_result == gen_result}")
    
    # Clean up
    import os
    os.remove("test_large_file.txt")
    
    # Memory demonstration (optional)
    demonstrate_memory_usage()
    
    print("\n" + "=" * 60)
    print("ALL GENERATOR TESTS COMPLETE")
    print("=" * 60)