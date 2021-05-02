#! /bin/sh

function recommends_push() {
    echo "Recommend \"git push\", since all of files are committed, but not pushed."
    exit 1
}

# count not committed, and not staged files.
fileCount=$(git status -s | grep -v \?\? | wc -l)

if [[ $fileCount -ne 0 ]]; then
    # not recommends push, since non-committed files exist.
    exit 0
fi

# get the current branch name.
currentBranch=$(git rev-parse --abbrev-ref HEAD)

# get remote branch name
remoteBranch=$(git branch -a | grep remotes | grep $currentBranch | xargs)
if [[ remoteBranch == "" ]]; then
    # the user does not push the current branch, yet.
    recommends_push
fi

# find the commit count of not pushed.
commitCount=$(git log --oneline $remoteBranch..$currentBranch | wc -l | xargs)

if [[ commitCount -ne 0 ]]; then
    # this repository has not pushed commits.
    recommends_push
fi

exit 0
