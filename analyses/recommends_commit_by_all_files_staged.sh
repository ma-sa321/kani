#! /bin/sh

function recommends_commit_ja() {
    echo "全てのファイルがステージングエリアに移されたので，\"git commit\"を実行しましょう．"
    exit 1
}

function recommends_commit() {
    echo "Recommend \"git commit\", since all of editted files are on stage."
    exit 1
}

status=$(git status -s)

# count not staged files.
notStagedFileCount=$(echo "$status" | grep '^.[AMDUCR] .*' | wc -l)
# count staged file.
stagedFileCount=$(echo "$status" | grep '^[AMDUCR]  .*' | wc -l)

if [[ $stagedFileCount -ne 0 && $notStagedFileCount -eq 0 ]]; then
    recommends_commit_ja
fi
