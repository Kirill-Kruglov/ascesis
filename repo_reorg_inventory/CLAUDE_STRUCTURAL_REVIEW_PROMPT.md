# Claude Structural Review Prompt

You are reviewing the local repository `ascesis` after reorganization passes 1-4.

Scope: review repository structure and navigation only. Do not evaluate or rewrite the underlying research theory. Do not move, delete, rename, stage, or commit files during review unless explicitly asked in a later pass.

Inspect these files first:

- `README.md`
- `research/README.md`
- `experiments/INDEX.md`
- `experiments/BA/INDEX.md`
- `experiments/FA/INDEX.md`
- `experiments/JB/INDEX.md`
- `research/playbook/README.md`
- `research/playbook/02_source_artifact_map.md`
- `repo_reorg_inventory/post_reorg_inventory.md`
- `repo_reorg_inventory/reorg_pass_4_commit_prep_report.md`
- `repo_reorg_inventory/commit_plan.md`

Then answer these questions:

1. Is navigation coherent for a new researcher?
2. Are research docs and experiments separated cleanly?
3. Are BA/FA/JB/JB0 evidence chains discoverable?
4. Are any active docs still misplaced?
5. Are there stale references caused by reorg?
6. Is playbook clearly marked as skeleton rather than finished method?
7. What should be fixed before the first reorg commit?
8. What should not be changed?

Review constraints:

- Do not suggest deleting evidence outputs, `results/`, `outputs/`, or `raw/` directories.
- Do not treat old reports/specs as live navigation unless they are explicitly index/readme files.
- Distinguish historical references from broken live links.
- Do not claim safety or theory success.
- Do not propose a new theory architecture; this is a repository structure review.

Expected output:

- Findings first, ordered by severity.
- File/path references for every finding.
- A short section titled `Before First Commit` with concrete fixes, if any.
- A short section titled `Do Not Change` listing historical/evidence areas that should remain intact.
- Final recommendation: `ready_for_commit`, `ready_after_minor_fixes`, or `needs_reorg_fix`.
