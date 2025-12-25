---
description: Data engineering PR review (diff vs origin/main)
allowed-tools: Bash(git diff:*), Bash(git status:*), Bash(git branch:*)
---

Branch: !`git branch --show-current`
Status: !`git status --porcelain`

Diff:
!`git diff origin/main...HEAD`

Review ONLY the diff. Output:
1) Summary
2) Must-fix (idempotency, dedupe logic, schema changes, late/duplicate data, performance)
3) Tests to add (re-run safety, duplicates, bad types)
4) Operational notes (backfills, monitoring)
