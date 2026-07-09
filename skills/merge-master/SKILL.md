---
name: merge-master
description: Pull the latest base branch and latest work branch, stay on the work branch, and merge the updated base branch into it. Never resolve merge conflicts automatically.
---

# Merge base branch into work branch

When the user asks to merge an updated base branch into a work branch, extract:

- project/repository name, if provided
- work branch identifier, if provided
- base branch, if provided

Workflow:

1. If a project/repository name is provided, move to that repository.

2. Fetch all latest remote changes:

   ```bash
   git fetch --all --prune
   ```

3. Determine the base branch.
   - Prefer the base branch explicitly named by the user.
   - Otherwise use the repository's standard integration branch, usually `master` or `main`.

4. Checkout the local base branch:

   ```bash
   git checkout <base-branch>
   ```

5. Pull latest changes for the base branch:

   ```bash
   git pull --ff-only origin <base-branch>
   ```

6. Determine the work branch to update.
   - Prefer the branch explicitly named by the user.
   - Otherwise use the current branch.
   - Check both local and remote branches when discovery is needed.
   - If multiple branches match, select the most likely candidate and explain the choice.

7. Checkout the work branch:

   ```bash
   git checkout <work-branch>
   ```

8. Pull latest changes for the work branch:

   ```bash
   git pull --ff-only
   ```

9. Confirm that the current branch is the work branch:

   ```bash
   git branch --show-current
   ```

10. Merge the updated local base branch into the work branch:

   ```bash
   git merge <base-branch>
   ```

Conflict rules:

- If merge conflicts occur, leave the repository in the conflicted merge state.
- Stay on the work branch.
- Do not abort the merge.
- Do not run `git merge --abort`.
- Do not revert the merge attempt.
- Do not reset the branch.
- Do not resolve conflicts automatically.
- Do not edit conflicting files.
- Do not create conflict resolution commits.
- Report:
  - conflicting files
  - current git status
  - current branch
  - suggested next steps for manual conflict resolution
- Stop after reporting the conflict state.

Successful merge rules:

- If the merge succeeds, stay on the work branch.
- Leave the merge result in the working tree.
- Report the merge result.
- Show the current branch.
- Show `git status`.
- Do not push changes.

Safety rules:

- Do not push unless the user explicitly asks.
- Do not delete branches.
- Do not rebase branches.
- Do not create additional commits unless required by the merge itself.
- Never execute:
  - `git merge --abort`
  - `git reset --hard`
  - `git restore`
  - `git checkout -- .`
  - `git clean -fd`
  unless explicitly requested by the user.
