# Engineering execution

Backlog.md is the only writable engineering work record. Product objects, canonical
contracts and product decisions remain requirements authorities. The frozen
S-042 prohibition on introducing task management governs the Product application;
this user-authorized repository tooling does not add task objects or Product features.

Use an existing Backlog.md 1.53.0 installation, or run the pinned official package:

```powershell
npx backlog.md@1.53.0 instructions overview
npx backlog.md@1.53.0 task list --plain
npx backlog.md@1.53.0 search 'your subject' --plain
npx backlog.md@1.53.0 task view TASK-5 --plain
```

No MCP, daemon, sync service, callback or custom state engine is required. The local
ignored `.tools/backlog` install is an optional convenience, not another backlog.
Do not reinitialize the project. Config and tasks are versioned; auto-commit, remote
operations and cross-branch task discovery are disabled. Work in the current bound
worktree; do not edit task state simultaneously from multiple worktrees.

Statuses are Backlog (not yet committed to start), Ready (startable), Doing (active),
Blocked (exact blocker in notes), and Done (acceptance verified). Native dependencies
remain authoritative even when a Doing task has independent work it can continue.
Backlog's derived readiness does not replace a task's explicit status. Unassigned
migrated work stays unassigned until a worker takes responsibility.

Read the CLI's required task-creation, task-execution and task-finalization guides.
Typical lifecycle, using IDs returned by the CLI:

```powershell
npx backlog.md@1.53.0 task create 'Requirement implementation' --doc spec/OWNER/contract.md --ac 'Observable result'
npx backlog.md@1.53.0 task edit TASK-N -s Ready
npx backlog.md@1.53.0 task edit TASK-N -s Doing -a @worker --plan 'Current researched plan'
npx backlog.md@1.53.0 task edit TASK-N --append-notes 'Implemented slice; command and result'
npx backlog.md@1.53.0 task edit TASK-N -s Blocked --append-notes 'Exact blocker; evidence; unblock condition'
npx backlog.md@1.53.0 task edit TASK-N --check-ac 1 --final-summary 'Verified result and evidence'
npx backlog.md@1.53.0 task edit TASK-N -s Done
```

Do not set Done merely because implementation exists. Acceptance requiring a merged
PR remains open until the legitimate gate integrates it. Commit task updates with
their implementation/evidence. Product requirements are linked, never rewritten as
new normative Backlog decisions.

## Migration boundary

The migration inventoried all Issues, open PRs, local plans, dirty runtime/spec files
and implementation readiness. TASK-2 references the existing distribution Issue #9
and PR #10; it does not duplicate their implementation. TASK-3 retains the original
Meaning Closure plan and local work inventory; TASK-4 records its missing protocol.
Closed Issues #1 and #7 and historical Stage 1/readiness/acceptance records remain
historical evidence, not actionable tasks. The completed frozen execution sequence
is not recreated as twenty new tasks. `docs/plans/` now routes to the migrated task;
future plans/progress live in task records. No runtime or product changes belonging
to the existing Meaning Closure work are included in this migration.

## Protected integration compatibility

Run `.harness/AGENT.md` entry/doctor and retain bound workspaces, native protected
PRs, trusted checks, exact-head owner approval for control changes, integration and
release. Existing GitHub Issues serve only as required gate-binding identities;
do not mirror Backlog statuses, owners, dependencies, checklists or progress there.
Existing open bindings must remain open while their PR gates require them.

**Remaining enforced-authority gap:** installed OpenHarness `github-pr-v1`
hard-codes `work: github-issues` in `model.AUTHORITIES`, rejects any other map in
`validate_config`, and requires an open Issue in `ci.candidate_context`. Its installed
entry also requires the generated `.harness/AGENT.md` bytes unchanged. Changing the
config alone or rewriting the generated entry would break closure without supporting
Backlog. Agent guidance therefore uses Backlog today, but OpenHarness cannot yet
attest that Backlog is the sole work authority. TASK-1 records this blocker. A native
upstream-supported profile must resolve it; no local bypass or custom sync is added.

The migration changes AGENTS.md, which is a protected control surface. Its PR needs
native repository-owner approval bound to the exact head and base before trusted
candidate acceptance/integration. Do not fabricate that approval on the owner's behalf.
