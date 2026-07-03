# GitHub Sync Procedure

This repository keeps all Atlas implementation work in local git commits first. To verify and push those commits to GitHub, use `scripts/github_sync_check.sh`.

## What the script does

- Verifies the working tree is clean.
- Detects the current branch.
- Verifies or configures the GitHub remote named `origin`.
- Fetches GitHub state.
- Reports whether local commits are ahead of or behind GitHub.
- Pushes only when explicitly run with `--push`.

## First-time setup

If `origin` is not configured, set the GitHub repository URL for this shell session:

```bash
export GITHUB_REPOSITORY_URL="https://github.com/<owner>/<repo>.git"
```

Then run:

```bash
scripts/github_sync_check.sh --check
```

If the output is correct, push with:

```bash
scripts/github_sync_check.sh --push
```

## Ongoing check

After every coding stage, run:

```bash
scripts/github_sync_check.sh --check
```

Then push when ready:

```bash
scripts/github_sync_check.sh --push
```

## What the user may need to provide

The automation cannot invent GitHub access. A human must provide one of these:

1. A GitHub repository URL, such as `https://github.com/<owner>/<repo>.git`.
2. Authentication already configured for git, for example SSH keys or a Git credential manager/token.

Prefer SSH or a Git credential manager for authentication. Do not paste access tokens into files or commit secrets into this repository.
