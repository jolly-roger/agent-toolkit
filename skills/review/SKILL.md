---
name: review
description: Fetch the latest base branch, update the work branch, compare the work branch against the base branch, and review the changes together with their implementation context. Use when the review should cover not only exact diff hunks, but also the surrounding function, method, component, helper, or related call sites touched by the change, including clear redundant logic or unnecessary repeated work introduced by the change.
---

# Review work branch against base branch with implementation context

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
8. Expand the review beyond raw diff hunks:
   - If a function or method changed, review the whole function or method.
   - If a component changed, review the whole component.
   - If a helper changed, review its main callers and the values passed in and out.
   - If a type, interface, or schema changed, review the main consumers affected by that contract.
   - If a condition, calculation, or data transformation changed, verify the surrounding flow that produces and consumes that value.
9. Look explicitly for implementation waste introduced by the change:
   - redundant second passes over the same data
   - duplicate aggregation or recomputation of a value already available
   - dead assignments or fields that are structurally present but never meaningfully populated
   - helper splits that preserve behavior but leave unnecessary work behind
10. Focus findings on bugs, regressions, inconsistent behavior, missing propagation, unnecessary repeated work, misleading types, and missing tests.

Recommended comparison commands:

```bash
git status
git branch --show-current
git log --oneline origin/<base-branch>..HEAD
git diff --stat origin/<base-branch>...HEAD
git diff origin/<base-branch>...HEAD
```

Recommended context-gathering commands:

```bash
git diff origin/<base-branch>...HEAD -- <path>
sed -n '<start>,<end>p' <path>
rg "<symbol-name>" <path-or-dir>
```
