#!/usr/bin/env bash
set -euo pipefail

REMOTE_NAME="${REMOTE_NAME:-origin}"
REMOTE_URL="${GITHUB_REPOSITORY_URL:-}"
BRANCH="${BRANCH:-$(git branch --show-current)}"
MODE="${1:---check}"

usage() {
  cat <<USAGE
Usage: $0 [--check|--push|--help]

Environment variables:
  REMOTE_NAME              Remote name to verify or configure. Defaults to origin.
  GITHUB_REPOSITORY_URL    GitHub remote URL used when REMOTE_NAME is missing.
  BRANCH                   Branch to compare or push. Defaults to current branch.
USAGE
}

case "${MODE}" in
  --check|--push)
    ;;
  --help|-h)
    usage
    exit 0
    ;;
  *)
    usage >&2
    echo "ERROR: unknown mode '${MODE}'" >&2
    exit 2
    ;;
esac

if [[ -z "${BRANCH}" ]]; then
  echo "ERROR: unable to determine current git branch" >&2
  exit 2
fi

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "ERROR: not inside a git repository" >&2
  exit 2
fi

if [[ -n "$(git status --short)" ]]; then
  echo "ERROR: working tree is not clean; commit or stash changes before syncing" >&2
  git status --short >&2
  exit 1
fi

if ! git remote get-url "${REMOTE_NAME}" >/dev/null 2>&1; then
  if [[ -z "${REMOTE_URL}" ]]; then
    echo "ERROR: remote '${REMOTE_NAME}' is not configured. Set GITHUB_REPOSITORY_URL or run git remote add ${REMOTE_NAME} <url>." >&2
    exit 3
  fi
  git remote add "${REMOTE_NAME}" "${REMOTE_URL}"
  echo "Configured ${REMOTE_NAME} -> ${REMOTE_URL}"
fi

REMOTE_URL_ACTUAL="$(git remote get-url "${REMOTE_NAME}")"
echo "Remote: ${REMOTE_NAME} -> ${REMOTE_URL_ACTUAL}"
echo "Branch: ${BRANCH}"
echo "Local HEAD: $(git rev-parse --short HEAD)"

git fetch "${REMOTE_NAME}" --prune

if git rev-parse --verify "${REMOTE_NAME}/${BRANCH}" >/dev/null 2>&1; then
  AHEAD_COUNT="$(git rev-list --count "${REMOTE_NAME}/${BRANCH}..HEAD")"
  BEHIND_COUNT="$(git rev-list --count "HEAD..${REMOTE_NAME}/${BRANCH}")"
  echo "Ahead of ${REMOTE_NAME}/${BRANCH}: ${AHEAD_COUNT}"
  echo "Behind ${REMOTE_NAME}/${BRANCH}: ${BEHIND_COUNT}"
else
  AHEAD_COUNT="new-branch"
  BEHIND_COUNT="0"
  echo "Remote branch ${REMOTE_NAME}/${BRANCH} does not exist yet."
fi

if [[ "${MODE}" == "--push" ]]; then
  git push --set-upstream "${REMOTE_NAME}" "${BRANCH}"
  echo "Pushed ${BRANCH} to ${REMOTE_NAME}."
else
  echo "Check complete. Use '$0 --push' to push after reviewing the output."
fi
