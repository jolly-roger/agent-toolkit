# Development Rules

## SCSS Rules

- The main class in a component SCSS file must use the component name in kebab case.
- All child classes must be nested according to the component hierarchy and usage.
- Avoid flat, loosely named selectors when the styles belong to a specific component.
- Always use `rem` units in SCSS, with `1rem = 16px`.

## JSX Rules

- JSX markup ternary operators must not contain nested ternary operators.

## TypeScript Rules

- Avoid using `Omit` when creating interfaces or types.
- Use `Omit` only as a last resort when there is no practical alternative.
- Prefer flat interfaces over deeply composed ones.
- Split interfaces into smaller reusable interfaces when that improves clarity or reuse.
- Use `type` only for plain combinations of interfaces that do not rely on helper types or advanced type composition.

## Git Safety

  - Git read operations against remotes are allowed when useful, including `git fetch`, `git ls-remote`, and reading remote refs.
  - Git write operations must be local-only unless I explicitly request a remote write.
  - Do not run remote-mutating commands by default, including:
    - `git push`
    - `git push --force`
    - `git push --delete`
    - `git tag` followed by pushing tags
    - `git remote set-url`
    - `git remote add`
    - `git remote remove`
    - `git remote rename`
  - Before any remote git write operation, ask for confirmation and state the exact command.
  - Local write operations are allowed, including:
    - `git checkout -b`
    - `git switch -c`
    - `git branch`
    - `git add`
    - `git commit`
    - `git stash`
    - `git tag` when not pushed
  - Branches should be created locally first and not pushed unless I explicitly ask.

## Jira Safety

  - Treat Jira as assigned-to-me only by default.
  - Every Jira search must include `assignee = currentUser()` unless I explicitly request a broader query.
  - Before reading or mutating a specific Jira issue, verify its assignee is `currentUser()`.
  - If assignee verification is unavailable or the issue is not assigned to me, ask before proceeding.
  - Never mutate Jira issues not assigned to me unless I explicitly name the issue and request the mutation.

## MongoDB Safety

  - Treat `db` as the workspace-local MongoDB alias for the active project.
  - All MongoDB operations must target only the local database referenced by `db`.
  - Do not read, query, aggregate, export, mutate, or inspect any other MongoDB database, including `admin`, `config`, and `local`, unless I explicitly request it.
  - Before any MongoDB write operation, state the exact target database and collection.

## README Guidance

  - README files should stay high-level and summarize the broader information.
  - Do not duplicate detailed content that already exists in other markdown files.
  - When details are needed, link or refer to the source markdown file instead of repeating the information.
  - README files should describe the repository content and purpose, not explain why or how the README was written.
  - README files should not refer to themselves or explain the README content as content.
