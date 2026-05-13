
# Day 4: Pull Request Workflow Simulation

echo "=========================================="
echo "PULL REQUEST WORKFLOW"
echo "=========================================="

cd ~/Desktop/ai-engineer-mastery/day-4-git-workflow/git-practice

echo ""
echo "PROFESSIONAL WORKFLOW:"

echo ""
echo "1. Always start from updated main:"
echo "   git checkout main"
echo "   git pull origin main  (if remote exists)"
echo "   git checkout -b feature/new-feature"

echo ""
echo "2. Make changes and commit:"
echo "   # Write code"
echo "   git add ."
echo "   git commit -m 'feat: Add new feature'"
echo "   git commit -m 'test: Add tests for feature'"
echo "   git commit -m 'docs: Update documentation'"

echo ""
echo "3. Push branch to GitHub:"
echo "   git push origin feature/new-feature"

echo ""
echo "4. Create Pull Request on GitHub:"
echo "   - Go to repository on GitHub"
echo "   - Click 'Pull requests' → 'New pull request'"
echo "   - Base: main, Compare: feature/new-feature"
echo "   - Add title and description"
echo "   - Request reviewers"
echo "   - Create pull request"

echo ""
echo "5. Address review feedback:"
echo "   # Make requested changes"
echo "   git add ."
echo "   git commit -m 'fix: Address PR feedback'"
echo "   git push origin feature/new-feature"
echo "   (PR updates automatically)"

echo ""
echo "6. Merge after approval:"
echo "   Options:"
echo "   - Merge commit: Preserves all commits"
echo "   - Squash merge: Combine all commits into one"
echo "   - Rebase merge: Linear history"

echo ""
echo "7. Clean up:"
echo "   git checkout main"
echo "   git pull origin main"
echo "   git branch -d feature/new-feature"
echo "   git push origin --delete feature/new-feature"

echo ""
echo "=========================================="
echo "BEST PRACTICES:"
echo "  ✅ Keep PRs small (<400 lines)"
echo "  ✅ Write descriptive PR titles"
echo "  ✅ Link to issue: 'Closes #123'"
echo "  ✅ Add screenshots for UI changes"
echo "  ✅ Use PR templates"
echo "  ✅ Request specific reviewers"
echo "  ✅ Respond to all comments"
echo "=========================================="