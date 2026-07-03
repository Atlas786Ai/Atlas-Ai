# Repository Transfer Audit

Use `scripts/repository_transfer_audit.sh` before and after every coding stage to confirm that local work is committed and ready to be transferred to GitHub.

## What it checks

- The command is running inside a git repository.
- The current branch and local `HEAD` are detectable.
- The working tree has no uncommitted or untracked files.
- The GitHub remote named `origin` is configured.
- When the remote is available, local and GitHub branch states are compared.
- The audit reports whether local commits are ahead of GitHub, behind GitHub, or already present on GitHub.

## Recommended workflow

Run the audit after each implementation step:

```bash
scripts/repository_transfer_audit.sh
```

If the audit says local commits are ahead of GitHub, push with:

```bash
scripts/github_sync_check.sh --push
```

If the audit says `origin` is missing, provide the GitHub repository URL and configure it once:

```bash
git remote add origin <github-url>
```

or set it for the sync helper:

```bash
export GITHUB_REPOSITORY_URL="https://github.com/<owner>/<repo>.git"
scripts/github_sync_check.sh --check
```

## Human input still required

This repository can automate checks and pushes, but it cannot safely invent these values:

1. The GitHub repository URL.
2. Authentication credentials, preferably via SSH keys or a Git credential manager.

Never commit tokens, passwords, or private keys into the repository.
