# Git操作補助ツールkani
## 本ツールは2020年度特別研究IIで作成
https://github.com/tamadalab/2020bthesis_masuda
### 実装機能概要
- コンパイル時にcommit差分を比較し，規定値以上の変更があった場合commitを促す．
- 連続したエラーが解消された時点で，commitを促す．
- commitを促す際，add commit pushの簡易にhelp表示する．

### 未修正点
- エラー情報を蓄積するDBが1つに集約されているため，ファイルAのエラーが修正されないまま別ファイルを実行すると，ファイルAのエラー情報の影響を受ける．
- コンパイルはgccとclangの場合と手動で制限している[該当ファイル](https://github.com/tamadalab/kani/blob/master/scripts/precmd_hook.sh)．
- .gitフォルダが上位ディレクトリにない場合，.git無いよとエラー出る(操作には影響ない)．
- 正直スパゲッティになってるファイルがある．



## 評価実験用
#### テンプレートリポジトリ
https://github.com/tmdlab2020TestTeam/testTemplate
#### GitHubClassroom[GitHub Classroomとは](http://takehiroman.hatenablog.com/entry/2016/03/31/135736)
https://classroom.github.com/classrooms/73564814-tmdlab2020testteam-githubclassroom/assignments/tmdlab-test-team


# kaniの機能詳細
### 分析の一時停止/再開

```sh
$ git kani disable/enable
```

* `disable` で `PROJECT_ROOT/.kani/disable` ファイルが作成される．
* `enable` を実行すると，`PROJECT_ROOT/.kani/disable` ファイルが削除される．

### 分析対象から外す

```sh
$ git kani deinit
```

* `$HOME/.config/kani/projects`からプロジェクトのパスが削除される．


## 導入方法
### Homebrewからkaniをインストールする
```sh
$ brew tap tamadalab/brew
$ brew install kani
```

上記コマンドにて，以下のようなディレクトリが作成される．

```sh
/usr/local/Celler/kani
├── README.md
├── analyses
│   ├── recommend.py (どういった条件でcommitを促すか決める所)
│   └── commit_guide.txt (commitを促す際の文)
├── bin
│   └── git-kani
└── scripts # ユーティリティスクリプト(hook関数)
    ├── chpwd_hook.sh
    ├── periodic_hook.sh
    ├── precmd_hook.sh
    ├── preexec_hook.sh
    ├── find-project-dir.sh (現在のディレクトリからプロジェクトのルートを取得するスクリプト)
    └── is-target-project.sh (現在のディレクトリのプロジェクトがkaniの分析対象かどうかを判定するスクリプト)
```

`zshrc.txt` に書かれていた内容は，`git kani init -` で出力するようにしました．
そのため，`~/.zshrc` の最後に，次の1行を追加すればOKにするようにしました．

```sh
eval "$(git kani init -)"
```

hook関数については[この資料](https://qiita.com/mollifier/items/558712f1a93ee07e22e2)を参照してください．

### 利用したいディレクトリにkaniを適応させる

```sh
$ git kani init
```

* 上記のコマンドで `.git` と同じディレクトリに `.kani` ディレクトリが作成される．
    * `.kani` ディレクトリには，`analyses`ディレクトリにあるスクリプトがコピーされる．
* `$HOME/.config/kani/projects` にプロジェクトのパスが追記される．

* `PROJECT_ROOT/.kani` には，分析結果のデータを格納している．

## Requirements

* [rcaloras/bash-preexec](https://github.com/rcaloras/bash-preexec)
