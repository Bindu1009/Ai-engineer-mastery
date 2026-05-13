#!/bin/bash
# Day 4: Git Merging

echo "=========================================="
echo "GIT MERGING DEMO"
echo "=========================================="

# Make sure we're on main branch
git checkout main

# Create another feature branch
echo ""
echo "1. Create 'feature-divide' branch:"
git checkout -b feature-divide

# Add divide function
echo ""
echo "2. Add divide function:"
cat >> calculator.py << 'EOF'

def divide(a, b):
    """Return the quotient of a and b."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
EOF

# Commit the change
git add calculator.py
git commit -m "Add divide function with zero division check"

# Switch back to main
git checkout main

# Merge feature-divide into main
echo ""
echo "3. Merge feature-divide into main:"
git merge feature-divide

# Show the result
echo ""
echo "4. Calculator.py after merge:"
tail -10 calculator.py

# Create a conflicting scenario
echo ""
echo "=========================================="
echo "CREATING A MERGE CONFLICT"
echo "=========================================="

# Create second branch from main
git checkout main
git checkout -b feature-power

# Modify same line on feature branch
sed -i '' 's/def add(a, b):/def add(a, b):\n    \"\"\"Add two numbers together.\"\"\"\n    # Using simple addition/' calculator.py 2>/dev/null || \
sed -i 's/def add(a, b):/def add(a, b):\n    \"\"\"Add two numbers together.\"\"\"\n    # Using simple addition/' calculator.py

git add calculator.py
git commit -m "Add documentation to add function on feature branch"

# Switch to main and modify SAME line
git checkout main

# Modify same line on main
sed -i '' 's/def add(a, b):/def add(a, b):\n    \"\"\"Return sum of two numbers.\"\"\"\n    # Simple addition implementation/' calculator.py 2>/dev/null || \
sed -i 's/def add(a, b):/def add(a, b):\n    \"\"\"Return sum of two numbers.\"\"\"\n    # Simple addition implementation/' calculator.py

git add calculator.py
git commit -m "Improve add function documentation on main"

echo ""
echo "Now try to merge feature-power into main:"
git merge feature-power

echo ""
echo "CONFLICT! Git doesn't know which version to keep."
echo ""
echo "Run: git status"
echo "Run: cat calculator.py (look for <<<<<<< markers)"
echo ""
echo "To resolve:"
echo "  1. Open calculator.py"
echo "  2. Remove <<<<<<<, =======, >>>>>>> markers"
echo "  3. Keep the code you want"
echo "  4. git add calculator.py"
echo "  5. git commit -m 'Resolve merge conflict'"# View the conflicted file
