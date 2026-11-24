#!/usr/bin/env bash
# Commit the changes under COMMIT_PATHS and push them to the current branch.
# Used by the generation jobs in .github/workflows/aws-news-summary.yml.
#
# Environment variables:
#   COMMIT_PATHS    Paths to commit, separated by spaces (for example "reports/")
#   COMMIT_MESSAGE  Commit subject. " for YYYY-MM-DD" (UTC) is appended
#   ARTIFACT_DIR    Directory that receives a copy of the added and updated files
#                   (uploaded as a workflow artifact)
#   ARTIFACT_FLAT   "1" to copy the files without their directories
#   GITHUB_REF_NAME Branch to push to (set by GitHub Actions)
set -euo pipefail

: "${COMMIT_PATHS:?COMMIT_PATHS is required}"
: "${COMMIT_MESSAGE:?COMMIT_MESSAGE is required}"
: "${ARTIFACT_DIR:?ARTIFACT_DIR is required}"
branch="${GITHUB_REF_NAME:?GITHUB_REF_NAME is required}"

# COMMIT_PATHS is a space-separated list, so it is not quoted.
read -r -a paths <<< "${COMMIT_PATHS}"

git add -- "${paths[@]}"

if git diff --cached --quiet -- "${paths[@]}"; then
  echo "No changes to commit in ${COMMIT_PATHS}."
  exit 0
fi

# Copy the added and updated files for the workflow artifacts
mkdir -p "${ARTIFACT_DIR}"
git -c core.quotePath=false diff --cached --name-only --diff-filter=AM -- "${paths[@]}" |
  while IFS= read -r file; do
    [ -f "${file}" ] || continue
    if [ "${ARTIFACT_FLAT:-0}" = "1" ]; then
      cp "${file}" "${ARTIFACT_DIR}/"
    else
      mkdir -p "${ARTIFACT_DIR}/$(dirname "${file}")"
      cp "${file}" "${ARTIFACT_DIR}/${file}"
    fi
  done
echo "Files added or updated: $(find "${ARTIFACT_DIR}" -type f | wc -l)"

git commit -q -m "${COMMIT_MESSAGE} for $(date -u +%Y-%m-%d)" -m "[skip ci]"
echo "Committed: $(git log --oneline -1)"

# Another job or run may have pushed in the meantime, so rebase before each attempt
for attempt in 1 2 3; do
  if git fetch -q origin "${branch}" && git rebase -q FETCH_HEAD; then
    if git push origin "HEAD:${branch}"; then
      echo "Pushed to ${branch}: $(git log --oneline -1)"
      exit 0
    fi
  else
    git rebase --abort || true
  fi
  echo "Push attempt ${attempt} failed."
  sleep $((attempt * 10))
done

echo "::error::Could not push the changes in ${COMMIT_PATHS} to ${branch}. The files are kept in the workflow artifact."
exit 1
