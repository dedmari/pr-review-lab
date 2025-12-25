---
description: Backend PR review (diff vs origin/main)
allowed-tools: Bash(git diff:*), Bash(git status:*), Bash(git branch:*)
---

Branch: !`git branch --show-current`
Status: !`git status --porcelain`

Diff:
!`git diff origin/main...HEAD`

Review ONLY the diff. Output:
1) Summary (max 6 bullets)
2) Must-fix (correctness, security, data loss, concurrency). Include file and exact fix.
3) Tests to add (concrete)
4) Risks and rollout notes