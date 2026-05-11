"""
DAY 3: CONTEXT MANAGERS MASTERY

Learn to manage resources automatically
"""

import time
import sqlite3
from contextlib import contextmanager
from typing import Any, Generator

# ============================================
# METHOD 1: Class-based Context Manager
# ============================================

class Timer:
    """Context manager that measures execution time."""
    
    def __enter__(self):
        self.start = time.time()
        return self  # Return value available via 'as timer'
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = time.time()
        self.duration = self.end - self.start
        print(f"⏱️ Operation took {self.duration:.4f} seconds")
        
        # Return False to propagate exceptions, True to suppress them
        return False  # Don't suppress exceptions
    
    def get_duration(self) -> float:
        return self.duration


class DatabaseConnection:
    """Context manager for database connections."""
    
    def __init__(self, db_name: str = ":memory:"):
        self.db_name = db_name
        self.connection = None
    
    def __enter__(self):
        print(f"📁 Opening database connection to {self.db_name}")
        self.connection = sqlite3.connect(self.db_name)
        return self.connection
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(f"⚠️ Exception occurred: {exc_val}")
            self.connection.rollback()
        else:
            print("✅ No errors, committing changes")
            self.connection.commit()
        
        print("🔒 Closing database connection")
        self.connection.close()
        return False  # Don't suppress exceptions


class FileHandler:
    """Context manager for file operations with automatic backup."""
    
    def __init__(self, filename: str, mode: str = 'r'):
        self.filename = filename
        self.mode = mode
        self.file = None
    
    def __enter__(self):
        print(f"📂 Opening file: {self.filename}")
        self.file = open(self.filename, self.mode)
        return self.file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"📂 Closing file: {self.filename}")
        if self.file:
            self.file.close()
        
        # Create backup if no errors occurred
        if exc_type is None and self.mode == 'w':
            backup_name = f"{self.filename}.backup"
            import shutil
            shutil.copy(self.filename, backup_name)
            print(f"💾 Created backup: {backup_name}")
        
        return False  # Don't suppress exceptions


class SuppressErrors:
    """Context manager that suppresses specific exceptions."""
    
    def __init__(self, *exceptions):
        self.exceptions = exceptions
    
    def __enter__(self):
        pass
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type and issubclass(exc_type, self.exceptions):
            print(f"🚫 Suppressed error: {exc_val}")
            return True  # Suppress the exception
        return False


# ============================================
# METHOD 2: Generator-based Context Manager (Simpler!)
# ============================================

@contextmanager
def timed_section(name: str):
    """Simpler context manager using @contextmanager decorator."""
    print(f"🟢 Starting: {name}")
    start = time.time()
    try:
        yield  # This is where the 'with' block runs
    finally:
        end = time.time()
        print(f"🔴 Finished: {name} took {end - start:.4f} seconds")


@contextmanager
def managed_resource(resource_name: str):
    """Generic resource manager."""
    print(f"🔧 Acquiring {resource_name}")
    try:
        yield f"Resource: {resource_name}"
    finally:
        print(f"🔧 Releasing {resource_name}")


@contextmanager
def retry_on_error(max_attempts: int = 3, delay: float = 1.0):
    """Retry a block of code if it fails."""
    last_exception = None
    for attempt in range(1, max_attempts + 1):
        try:
            print(f"🔄 Attempt {attempt} of {max_attempts}")
            yield  # Execute the 'with' block
            break  # Success, exit the loop
        except Exception as e:
            last_exception = e
            print(f"❌ Attempt {attempt} failed: {e}")
            if attempt < max_attempts:
                time.sleep(delay)
            else:
                raise last_exception


# ============================================
# PRACTICAL EXAMPLES
# ============================================

def demo_class_based():
    """Demonstrate class-based context managers."""
    print("\n" + "=" * 60)
    print("CLASS-BASED CONTEXT MANAGERS")
    print("=" * 60)
    
    # Example 1: Timer
    print("\n[1] Timer Context Manager")
    with Timer() as timer:
        time.sleep(0.5)
        print("  Doing some work...")
    print(f"  Actually took: {timer.get_duration():.4f}s")
    
    # Example 2: Database connection
    print("\n[2] Database Connection")
    with DatabaseConnection("test.db") as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE users (id INTEGER, name TEXT)")
        cursor.execute("INSERT INTO users VALUES (1, 'Alice')")
        print("  ✅ Database operations completed")
    
    # Example 3: File with backup
    print("\n[3] File Handler with Backup")
    with FileHandler("test_data.txt", "w") as f:
        f.write("Hello, World!")
        print("  ✅ Wrote to file")
    
    # Example 4: Error suppression
    print("\n[4] Error Suppression")
    with SuppressErrors(ZeroDivisionError, ValueError):
        print("  Trying to divide by zero...")
        result = 10 / 0
        print(f"  Result: {result}")  # This won't execute
    print("  ✅ Code continued after suppressed error")


def demo_generator_based():
    """Demonstrate @contextmanager decorator."""
    print("\n" + "=" * 60)
    print("GENERATOR-BASED CONTEXT MANAGERS")
    print("=" * 60)
    
    # Example 1: Timed section
    print("\n[1] Timed Section")
    with timed_section("Database backup"):
        time.sleep(0.5)
        print("  📀 Backing up database...")
    
    # Example 2: Resource management
    print("\n[2] Resource Manager")
    with managed_resource("Network Connection") as resource:
        print(f"  Using {resource}")
    
    # Example 3: Retry on error
    print("\n[3] Retry on Error")
    attempt_counter = 0
    
    with retry_on_error(max_attempts=3, delay=0.5):
        attempt_counter += 1
        if attempt_counter < 2:
            raise ConnectionError("Network timeout")
        print(f"  ✅ Succeeded on attempt {attempt_counter}")


# ============================================
# ADVANCED: Chaining Context Managers
# ============================================

def demo_chaining():
    """Chain multiple context managers."""
    print("\n" + "=" * 60)
    print("CHAINING CONTEXT MANAGERS")
    print("=" * 60)
    
    # Method A: Multiple 'with' statements
    print("\n[1] Multiple with statements (Python 3.9+)")
    with open("file1.txt", "w") as f1, open("file2.txt", "w") as f2:
        f1.write("Content 1")
        f2.write("Content 2")
        print("  ✅ Wrote to both files")
    
    # Method B: Nested context managers
    print("\n[2] Nested context managers")
    with Timer():
        with DatabaseConnection("test.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            results = cursor.fetchall()
            print(f"  Users: {results}")


# ============================================
# REAL-WORLD: API Client with Rate Limiting
# ============================================

class RateLimiter:
    """Context manager that enforces rate limits."""
    
    def __init__(self, max_calls: int, time_window: float):
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = []
    
    def __enter__(self):
        now = time.time()
        # Remove calls older than time window
        self.calls = [t for t in self.calls if t > now - self.time_window]
        
        if len(self.calls) >= self.max_calls:
            wait_time = self.time_window - (now - self.calls[0])
            print(f"⏰ Rate limit hit. Waiting {wait_time:.2f} seconds")
            time.sleep(wait_time)
        
        self.calls.append(time.time())
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def make_api_call(api_name: str):
    """Simulate making an API call."""
    print(f"📡 Calling {api_name}...")
    time.sleep(0.1)  # Simulate network delay
    print(f"✅ {api_name} responded")


def demo_real_world():
    """Real-world example: Rate-limited API client."""
    print("\n" + "=" * 60)
    print("REAL-WORLD: RATE-LIMITED API CLIENT")
    print("=" * 60)
    
    # Allow only 2 calls per second
    with RateLimiter(max_calls=2, time_window=1.0):
        for i in range(5):
            with RateLimiter(max_calls=2, time_window=1.0):
                make_api_call(f"API {i+1}")


# ============================================
# CLEANUP & RUN
# ============================================

if __name__ == "__main__":
    demo_class_based()
    demo_generator_based()
    demo_chaining()
    demo_real_world()
    
    # Cleanup
    import os
    for file in ["test.db", "test_data.txt", "file1.txt", "file2.txt", "test_data.txt.backup"]:
        if os.path.exists(file):
            os.remove(file)
    
    print("\n" + "=" * 60)
    print("✅ ALL CONTEXT MANAGER TESTS COMPLETE")
    print("=" * 60)