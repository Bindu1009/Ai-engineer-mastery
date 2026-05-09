"""
DAY 2 CHALLENGE: Build a Log File Analyzer

Use decorators AND generators together
"""

import time
import functools
from typing import Generator, Dict, List
from datetime import datetime

# ============================================
# STEP 1: Create decorators for logging and timing
# ============================================

def log_execution(func):
    """Log when a function starts and ends."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[START] {func.__name__}")
        result = func(*args, **kwargs)
        print(f"[END] {func.__name__}")
        return result
    return wrapper

def time_execution(func):
    """Time how long function takes."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"[TIME] {func.__name__} took {time.time() - start:.4f}s")
        return result
    return wrapper

# ============================================
# STEP 2: Create a generator that yields log lines
# ============================================

def generate_log_lines(n: int) -> Generator[str, None, None]:
    """Generate n simulated log lines."""
    log_levels = ["INFO", "WARNING", "ERROR", "DEBUG"]
    
    for i in range(n):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        level = log_levels[i % len(log_levels)]
        
        if level == "ERROR":
            message = f"Database connection failed"
        elif level == "WARNING":
            message = f"High memory usage: 85%"
        else:
            message = f"Processing batch {i}"
        
        yield f"{timestamp} [{level}] {message}"

# ============================================
# STEP 3: Create processing pipeline with generators
# ============================================

def filter_by_level(logs: Generator, target_level: str) -> Generator:
    """Filter logs to only show specific level."""
    for log in logs:
        if f"[{target_level}]" in log:
            yield log

def extract_errors(logs: Generator) -> Generator:
    """Extract only error messages."""
    for log in logs:
        if "[ERROR]" in log:
            # Extract just the message part
            parts = log.split("]")
            yield parts[-1].strip()

def count_by_level(logs: Generator) -> Dict[str, int]:
    """Count how many logs per level."""
    counts = {"INFO": 0, "WARNING": 0, "ERROR": 0, "DEBUG": 0}
    
    for log in logs:
        for level in counts.keys():
            if f"[{level}]" in log:
                counts[level] += 1
                break
    
    return counts

# ============================================
# STEP 4: Apply decorators to the analysis
# ============================================

@log_execution
@time_execution
def analyze_logs(n_lines: int = 100):
    """Complete log analysis pipeline."""
    
    print(f"\nAnalyzing {n_lines} log lines...\n")
    
    # Pipeline: Generate -> Filter -> Count
    logs = generate_log_lines(n_lines)
    counts = count_by_level(logs)
    
    print("Log Level Counts:")
    for level, count in counts.items():
        bar = "█" * (count // 5)  # Simple visual bar
        print(f"  {level:7}: {count:3} {bar}")
    
    # Pipeline: Generate -> Filter -> Extract errors
    print("\nSample Errors:")
    errors = extract_errors(filter_by_level(generate_log_lines(n_lines), "ERROR"))
    
    error_count = 0
    for error in errors:
        if error_count < 5:  # Only show first 5
            print(f"  ⚠️ {error}")
        error_count += 1
    
    print(f"\nTotal errors found: {error_count}")
    
    return counts

# ============================================
# RUN THE CHALLENGE
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("DAY 2 CHALLENGE: Log File Analyzer")
    print("=" * 60)
    
    # Run with different sizes
    analyze_logs(50)
    print("\n" + "-" * 40)
    analyze_logs(200)
    
    print("\n" + "=" * 60)
    print("✅ CHALLENGE COMPLETE!")
    print("You've used decorators AND generators together")
    print("=" * 60)