# agent-toolkit

`agent-toolkit` is a small instruction repository for shared Codex working rules.

At the moment it contains one source of truth:

- [`AGENTS.md`](./AGENTS.md) for development, Git, Jira, and MongoDB safety rules

## What this repo is for

- Keep shared agent instructions in one place.
- Provide a lightweight reference for the conventions used across the workspace.
- Avoid duplicating policy in individual project repos when the same rule applies broadly.

## Current rules covered

- SCSS structure and formatting
- JSX ternary usage
- Git safety and remote-write restrictions
- Jira access and mutation safety
- MongoDB database restrictions

## Notes

- This repository currently has no application code.
- If new tooling or templates are added later, document them here and keep `AGENTS.md` as the authoritative rule file.
