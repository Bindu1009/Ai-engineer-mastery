#!/bin/bash
# Day 4: Git Rebasing

# Create a fresh repository for rebasing demo
cd ~/Desktop/ai-engineer-mastery/day-4-git-workflow
mkdir rebasing-practice
cd rebasing-practice

git init

echo "# Rebasing Practice" > README.md
git add README.md
git commit -m "Initial commit"

# Create feature branch
git checkout -b feature-logging

# Add logging feature
cat > logger.py << 'EOF'
import datetime

def log_info(message):
    print(f"[INFO] {datetime.datetime.now()}: {message}")

def log_error(message):
    print(f"[ERROR] {datetime.datetime.now()}: {message}")
EOF

git add logger.py
git commit -m "Add logging module"

# Go back to main and add commits
git checkout main

cat > utils.py << 'EOF'
def greet(name):
    return f"Hello, {name}!"
EOF

git add utils.py
git commit -m "Add utils module with greet function"

# Now rebase feature branch onto updated main
echo ""
echo "=========================================="
echo "REBASING DEMO"
echo "=========================================="

echo ""
echo "Before rebase, commit history looks like:"
echo "  main: A <- B (utils.py)"
echo "  feature-logging: A <- C (logger.py)"
echo "  (A is initial commit)"

echo ""
echo "Rebasing makes it look like:"
echo "  main: A <- B"
echo "  feature-logging: A <- B <- C"
echo "  (feature branch now starts from latest main)"

# Perform the rebase
git checkout feature-logging
git rebase main

echo ""
echo "Rebase complete! History is now linear."

echo ""
echo "VS MERGE (creates merge commit):"
echo "  main: A <- B <- M"
echo "  feature: A <- C -/"

echo ""
echo "KEY DIFFERENCES:"
echo "  Merge: Preserves history as it happened, creates merge commit"
echo "  Rebase: Creates linear history, rewrites commit hashes"
echo ""
echo "WHEN TO USE:"
echo "  Merge: Public branches, when you want to preserve context"
echo "  Rebase: Private feature branches, before opening PR"