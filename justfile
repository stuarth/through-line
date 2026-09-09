# List available recipes
default:
    @just --list

# Cut a release: tag the current main commit and publish a GitHub release.
# Usage: just release 1.3.0
release version:
    #!/usr/bin/env bash
    set -euo pipefail
    version="{{version}}"
    tag="v${version#v}"

    if [[ -n "$(git status --porcelain)" ]]; then
        echo "error: working tree is not clean" >&2; exit 1
    fi
    branch="$(git branch --show-current)"
    if [[ "$branch" != "main" ]]; then
        echo "error: on branch '$branch', releases are cut from main" >&2; exit 1
    fi
    git fetch origin main
    if [[ "$(git rev-parse HEAD)" != "$(git rev-parse origin/main)" ]]; then
        echo "error: local main is not in sync with origin/main" >&2; exit 1
    fi
    if git rev-parse "$tag" >/dev/null 2>&1; then
        echo "error: tag $tag already exists" >&2; exit 1
    fi

    git tag -a "$tag" -m "through-line $tag"
    git push origin "$tag"
    gh release create "$tag" --title "through-line $tag" --generate-notes
