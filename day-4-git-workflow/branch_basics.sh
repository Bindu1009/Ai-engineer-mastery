#!/bin/bash
# Day 4: Git Branching Basics
# Run this script to learn branching commands

echo "=========================================="
echo "GIT BRANCHING BASICS"
echo "=========================================="

# Show current branch
echo ""
echo "1. Check current branch:"
git branch
echo "  (* means you are on that branch)"

# Create a new branch
echo ""
echo "2. Create a new branch called 'feature-multiply':"
git branch feature-multiply

# List all branches
echo ""
echo "3. List all branches:"
git branch

# Switch to new branch
echo ""
echo "4. Switch to feature-multiply branch:"
git checkout feature-multiply

# Alternative: create and switch in one command
echo ""
echo "5. Create and switch in one command (git checkout -b):"
echo "   git checkout -b new-branch-name"

# Add content on new branch
echo ""
echo "6. Add multiply function on feature branch:"
cat >> calculator.py << 'EOF'

def multiply(a, b):
    """Return the product of a and b."""
    return a * b
EOF

# Show changes
git diff

# Commit the change
git add calculator.py
git commit -m "Add multiply function"

# Show branch history
echo ""
echo "7. View commit history on feature branch:"
git log --oneline -3

# Switch back to main
echo ""
echo "8. Switch back to main branch:"
git checkout main

# Show calculator.py on main (multiply function is missing)
echo ""
echo "9. View calculator.py on main branch:"
cat calculator.py
echo "  Note: multiply function is NOT here (it's only on feature branch)"

echo ""
echo "=========================================="
echo "KEY CONCEPTS:"
echo "  - Branches are independent lines of development"
echo "  - Changes on one branch don't affect others"
echo "  - git branch: list branches"
echo "  - git branch <name>: create branch"
echo "  - git checkout <name>: switch branch"
echo "  - git checkout -b <name>: create and switch"
echo "=========================================="