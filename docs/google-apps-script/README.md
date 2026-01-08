Google Apps Script — Auto-push sheet to GitHub

Overview

This example shows how to push the active sheet content as JSON into the repository at `data/concerts.json` using a GitHub Personal Access Token (PAT).

Setup steps

1. Create a GitHub Personal Access Token with `repo` scope (or `public_repo` for public repos). Keep the token secret.
2. Open your Google Sheet, go to Extensions → Apps Script and create a new project.
3. Copy the script `update_concerts.gs` into the project.
4. In Apps Script: Project Settings → Script Properties, add:
   - `GITHUB_TOKEN` = your PAT
   - `REPO_OWNER` = your GitHub username or org
   - `REPO_NAME` = pedroalcacer-com
   - `FILE_PATH` = data/concerts.json
   - (optional) `COMMITTER_NAME` and `COMMITTER_EMAIL`
5. Run `pushSheetToGit()` once to authorize the script and perform the commit. Approve required scopes.
6. (Optional) In Apps Script, create a trigger: Edit → Current project's triggers → add time-driven trigger (e.g., daily) or install an onEdit trigger.

Security notes

- The PAT needs `repo` scope if the repo is private. Treat it as a secret — store only in Script Properties.
- Commits will show up in the repository with the committer you configured.

If you prefer the repository not to contain secrets, an alternative is to have Apps Script call a small serverless endpoint you control which holds the PAT and performs the commit.
