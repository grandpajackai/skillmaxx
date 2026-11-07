# Sourced by testing/nightly.sh. Production sync is unchanged.
# SKILLMAXX_TRIAL=1 stays on the current branch and never fetches, checks out, pulls, or pushes.
skillmaxx_sync() {
  if [ "${SKILLMAXX_TRIAL:-}" = "1" ]; then
    branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown)
    case "$branch" in
      master|main)
        echo "TRIAL refuses branch $branch. No fetch, checkout, commit, or push."
        return 1
        ;;
      HEAD|unknown|"")
        echo "TRIAL refuses detached HEAD. No fetch, checkout, commit, or push."
        return 1
        ;;
    esac
    if [ -n "$(git status --porcelain)" ]; then
      echo "TRIAL refuses a dirty worktree on $branch. No fetch, checkout, commit, or push."
      return 1
    fi
    NOPUSH=1
    export NOPUSH
    echo "TRIAL: staying on $branch. No fetch, checkout, or pull. Push disabled."
    return 0
  fi
  git fetch -q origin && git checkout -q master && git pull -q --ff-only origin master
}

skillmaxx_trial_commit_ok() {
  [ "${SKILLMAXX_TRIAL:-}" = "1" ] || return 0
  branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown)
  case "$branch" in
    master|main|HEAD|unknown|"")
      echo "TRIAL refuses to commit on $branch."
      return 1
      ;;
  esac
  NOPUSH=1
  export NOPUSH
  return 0
}
