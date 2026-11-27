---
name: finishing-a-development-branch
description: Finish implemented work on a git branch or worktree: verify the full test suite, then let the user choose merge, pull request or keep, and clean up safely. Use when implementation is done and tests are passing. "จบงาน branch", "ควร merge ยังไง".
---

# Finishing a branch
1. **Verify.** Run the project's full test suite on the tree you are about to integrate. Failing: report the failures and stop; no menu until green. (Projects that forbid local runs: verify through their CI.)
2. **Detect.** `git rev-parse --git-dir`, `--git-common-dir`, `--show-toplevel`. Same git dir = normal repo; different = linked worktree. Save the worktree path now. Detached HEAD in a worktree = externally managed.
3. **Base branch.** Use the one named in the plan or upstream; if unknown ask "this split from <guess>, correct?" Merging into the wrong base is hard to undo.
4. **Offer exactly these options and wait** (the integration decision is the user's; nothing here runs without their pick):
   1. Merge back to the base locally
   2. Push and open a pull request
   3. Keep the branch as is
   Detached HEAD: only "push as a new branch and open a PR" or "keep".
5. **Execute.**
   - Merge: from the main repo root `git checkout <base>`, `git pull`, `git merge <branch>`, run the tests on the merged result. If they fail, stop and leave branch and worktree in place. If green, remove the worktree (step 6), then `git branch -d <branch>`.
   - PR: `git push -u origin <branch>` (detached: `git push origin HEAD:refs/heads/<new-branch>`), then create the PR with `gh pr create` following the repo's template; report the URL. Keep the worktree for review fixes.
   - Keep: report the branch name and worktree path.
6. **Clean up the worktree** (merge or confirmed discard only), from outside it: only if its path is under `.worktrees/` or `worktrees/` (made by `worktree-isolation`): `git worktree remove "<path>"`, `git worktree prune`. If removal is refused because of uncommitted files, never use `--force`: show `git -C "<path>" status --porcelain -uall` and ask whether to commit them, move them, or delete them. Other worktrees belong to the host: leave them.
7. **Discard** exists only when the user explicitly asks to throw the work away. List the branch, commits and worktree, and require the user to type `discard`; only then `git branch -D`.
8. Never force-push on your own; a rejected push means the remote moved, so investigate.
