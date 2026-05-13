"""
DAY 4 CHALLENGE: Git Workflow Simulation

Write the git commands for each scenario below.
"""

# Scenario 1: Starting a new feature
print("=" * 60)
print("SCENARIO 1: Start a new feature")
print("=" * 60)

print("""
You need to add a 'power' function (exponentiation) to the calculator.
Current branch: main (with add, subtract, multiply, divide)

Commands:
1. ___________________________________  # Create and switch to feature branch
2. ___________________________________  # Write code (not a git command)
3. ___________________________________  # Stage changes
4. ___________________________________  # Commit with message
""")

# Scenario 2: Updating feature branch with main
print("\n" + "=" * 60)
print("SCENARIO 2: Update feature branch with latest main")
print("=" * 60)

print("""
While you were working on 'feature/power', your teammate merged 
'feature/square-root' into main. You need these changes.

Current branch: feature/power

Commands:
1. ___________________________________  # Switch to main
2. ___________________________________  # Get latest changes
3. ___________________________________  # Switch back to feature branch
4. ___________________________________  # Update feature branch with main changes
""")

# Scenario 3: Fix a bug in production
print("\n" + "=" * 60)
print("SCENARIO 3: Emergency bug fix on main")
print("=" * 60)

print("""
A critical bug was found in production. The divide function crashes 
when b is None (not just zero). You need to fix it immediately.

Current branch: main (but you're working on feature/power)

Commands:
1. ___________________________________  # Save current work temporarily
2. ___________________________________  # Switch to main
3. ___________________________________  # Create hotfix branch
4. ___________________________________  # Fix the bug (not a git command)
5. ___________________________________  # Stage the fix
6. ___________________________________  # Commit the fix
7. ___________________________________  # Switch to main
8. ___________________________________  # Merge hotfix into main
9. ___________________________________  # Delete hotfix branch
10. __________________________________  # Go back to feature branch
11. __________________________________  # Restore saved work
""")

# Scenario 4: Pull Request review feedback
print("\n" + "=" * 60)
print("SCENARIO 4: Address PR feedback")
print("=" * 60)

print("""
Your PR for 'feature/power' was reviewed. The reviewer wants:
- Better docstring for power function
- Add test for negative exponent

Current branch: feature/power (PR is open on GitHub)

Commands:
1. ___________________________________  # Make changes (not a git command)
2. ___________________________________  # Stage changes
3. ___________________________________  # Commit changes
4. ___________________________________  # Push to update PR
""")

# Answer Key
print("\n" + "=" * 60)
print("ANSWER KEY")
print("=" * 60)

print("""
Scenario 1:
1. git checkout -b feature/power
2. # Write the power function in calculator.py
3. git add calculator.py
4. git commit -m "feat: Add power function"

Scenario 2:
1. git checkout main
2. git pull origin main
3. git checkout feature/power
4. git rebase main  (or git merge main)

Scenario 3:
1. git stash
2. git checkout main
3. git checkout -b hotfix/divide-none
4. # Fix the divide function
5. git add calculator.py
6. git commit -m "fix: Handle None in divide function"
7. git checkout main
8. git merge hotfix/divide-none
9. git branch -d hotfix/divide-none
10. git checkout feature/power
11. git stash pop

Scenario 4:
1. # Update docstring and add test
2. git add calculator.py tests/test_calculator.py
3. git commit -m "fix: Address PR feedback on power function"
4. git push origin feature/power
""")

print("\n" + "=" * 60)
print("✅ CHALLENGE COMPLETE")
print("=" * 60)