#!/usr/bin/env bash
set -euo pipefail

REMOTE_NAME="${REMOTE_NAME:-origin}"
BRANCH="${BRANCH:-$(git branch --show-current)}"

print_section() {
  printf '\n== %s ==\n' "$1"
}

failures=0
warn() {
  printf 'WARN: %s\n' "$1" >&2
}

fail() {
  printf 'FAIL: %s\n' "$1" >&2
  failures=$((failures + 1))
}

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "FAIL: not inside a git repository" >&2
  exit 2
fi

print_section "Local repository"
echo "Branch: ${BRANCH:-unknown}"
echo "HEAD: $(git rev-parse --short HEAD)"

print_section "Working tree"
STATUS_OUTPUT="$(git status --short)"
if [[ -z "${STATUS_OUTPUT}" ]]; then
  echo "OK: working tree is clean"
else
  fail "working tree has uncommitted or untracked files"
  echo "${STATUS_OUTPUT}"
fi

print_section "Remote configuration"
if git remote get-url "${REMOTE_NAME}" >/dev/null 2>&1; then
  REMOTE_URL="$(git remote get-url "${REMOTE_NAME}")"
  echo "OK: ${REMOTE_NAME} -> ${REMOTE_URL}"
else
  fail "remote '${REMOTE_NAME}' is not configured"
  echo "Set it with: git remote add ${REMOTE_NAME} <github-url>"
fi

if [[ -z "${BRANCH}" ]]; then
  fail "current branch could not be detected"
fi

if [[ ${failures} -eq 0 ]]; then
  print_section "GitHub comparison"
  git fetch "${REMOTE_NAME}" --prune
  if git rev-parse --verify "${REMOTE_NAME}/${BRANCH}" >/dev/null 2>&1; then
    AHEAD_COUNT="$(git rev-list --count "${REMOTE_NAME}/${BRANCH}..HEAD")"
    BEHIND_COUNT="$(git rev-list --count "HEAD..${REMOTE_NAME}/${BRANCH}")"
    echo "Ahead of ${REMOTE_NAME}/${BRANCH}: ${AHEAD_COUNT}"
    echo "Behind ${REMOTE_NAME}/${BRANCH}: ${BEHIND_COUNT}"
    if [[ "${BEHIND_COUNT}" != "0" ]]; then
      warn "local branch is behind GitHub; pull/rebase before pushing"
    fi
    if [[ "${AHEAD_COUNT}" != "0" ]]; then
      warn "local commits are not on GitHub yet; run scripts/github_sync_check.sh --push after review"
    else
      echo "OK: local HEAD is present on ${REMOTE_NAME}/${BRANCH}"
    fi
  else
    warn "remote branch ${REMOTE_NAME}/${BRANCH} does not exist yet; first push will create it"
  fi
fi

print_section "Result"
if [[ ${failures} -eq 0 ]]; then
  echo "OK: repository is ready for GitHub sync checks"
else
  echo "FAIL: resolve ${failures} blocking issue(s) before GitHub sync"
fi

exit "${failures}"
