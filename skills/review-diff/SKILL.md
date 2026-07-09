---
name: review-diff
description: Fetch the latest base branch, update the work branch, compare the work branch against the base branch, and review the changes.
---

# Review work branch against base branch

Extract from the user request:

- repository/project name, if provided
- work branch identifier, if provided
- base branch, if provided

Workflow:

1. Move to the specified repository.
2. Determine the base branch.
   - Prefer the base branch explicitly named by the user.
   - Otherwise use the repository's standard integration branch, usually `master` or `main`.
3. Fetch the latest base branch:

   ```bash
   git fetch origin <base-branch> --prune
   ```

4. Determine the work branch to review.
   - Prefer the branch explicitly named by the user.
   - Otherwise use the current branch.
5. Checkout the work branch if necessary.
6. Pull latest changes for the work branch:

   ```bash
   git pull --ff-only
   ```

7. Review the work branch against latest `origin/<base-branch>`.

Recommended comparison commands:

```bash
git status
git branch --show-current
git log --oneline origin/<base-branch>..HEAD
git diff --stat origin/<base-branch>...HEAD
git diff origin/<base-branch>...HEAD
```
