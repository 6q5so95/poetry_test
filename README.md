# poetry_test

## pyenvでlocalのPythonバージョンを指定する
- pyenv install で必要となる複数のpythonを導入する
```
pyenv install --list
pyenv install 3.11.4
pyenv install 3.11.x
```

## 使用するpythonバージョンを指定する
globalはシステム全体で使うバージョンを変えたいときに使用。localはプロジェクトごとで違うバージョンを使いたいときに使用。
```
mkdir sandbox1; cd $_
cat .python-version
3.11.4
pyenv local or pyenv global
```

```
$ pyenv local; python -V
3.11.4
Python 3.11.4
```
---

## poetry初期設定
対話式で導入
pythonのバージョンはpyenvで設定したものを示すこと
```
petory init
```
## poetoryでインストール
```
poetry install

$ poetry install
The currently activated Python version 3.8.11 is not supported by the project (3.11.4).
Trying to find and use a compatible version. 
Using python3 (3.11.4)
Creating virtualenv poetry-test-82y1yN3c-py3.11 in /home/satoshi/.cache/pypoetry/virtualenvs
Updating dependencies
Resolving dependencies... (0.1s)

Writing lock file

/developer/poetry_sandbox/test_package1/poetry_test/poetry_test does not contain any element
```
生成ファイル確認
```
$ ls -altr
合計 28
drwxrwxr-x 3 satoshi satoshi 4096 12月  9 12:49 ..
drwxrwxr-x 8 satoshi satoshi 4096 12月  9 12:49 .git
-rw-rw-r-- 1 satoshi satoshi    7 12月  9 13:05 .python-version
-rw-rw-r-- 1 satoshi satoshi  309 12月  9 13:13 pyproject.toml
-rw-rw-r-- 1 satoshi satoshi  173 12月  9 13:14 poetry.lock
drwxrwxr-x 3 satoshi satoshi 4096 12月  9 13:14 .
-rw-rw-r-- 1 satoshi satoshi 1206 12月  9 13:15 README.md
```
---

## 追加でパッケージを追加する
```
poetry add requests

The currently activated Python version 3.8.11 is not supported by the project (3.11.4).
Trying to find and use a compatible version. 
Using python3 (3.11.4)
Using version ^2.31.0 for requests

Updating dependencies
Resolving dependencies... (0.1s)

Writing lock file

Package operations: 5 installs, 0 updates, 0 removals

  • Installing certifi (2023.11.17)
  • Installing charset-normalizer (3.3.2)
  • Installing idna (3.6)
  • Installing urllib3 (2.1.0)
  • Installing requests (2.31.0)
```
## 追加パッケージの確認
いくつか方法があります

### インストール済みの依存パッケージの一覧を表示
これでrequestsがリストに含まれていることを確認
```
$ poetry show -t
The currently activated Python version 3.8.11 is not supported by the project (3.11.4).
Trying to find and use a compatible version. 
Using python3 (3.11.4)
requests 2.31.0 Python HTTP for Humans.
├── certifi >=2017.4.17
├── charset-normalizer >=2,<4
├── idna >=2.5,<4
└── urllib3 >=1.21.1,<3
```

### Pythonのpipが見ているインストール済みパッケージを確認
pip listのリストにrequestsが存在すればOK
```
$ poetry run pip list
The currently activated Python version 3.8.11 is not supported by the project (3.11.4).
Trying to find and use a compatible version. 
Using python3 (3.11.4)
Package            Version
------------------ ----------
certifi            2023.11.17
charset-normalizer 3.3.2
idna               3.6
pip                22.2.2
requests           2.31.0
setuptools         65.3.0
urllib3            2.1.0
wheel              0.37.1

[notice] A new release of pip available: 22.2.2 -> 23.3.1
[notice] To update, run: pip install --upgrade pip
```
### 仮想環境に入りPythonインタプリタからimportしエラーが出なければ導入済みを意味します
```
$ poetry shell
The currently activated Python version 3.8.11 is not supported by the project (3.11.4).
Trying to find and use a compatible version. 
Using python3 (3.11.4)
Spawning shell within /home/satoshi/.cache/pypoetry/virtualenvs/poetry-test-82y1yN3c-py3.11
. /home/satoshi/.cache/pypoetry/virtualenvs/poetry-test-82y1yN3c-py3.11/bin/activate
satoshi@server:/developer/poetry_sandbox/test_package1/poetry_test$ . /home/satoshi/.cache/pypoetry/virtualenvs/poetry-test-82y1yN3c-py3.11/bin/activate
(poetry-test-py3.11) satoshi@server:/developer/poetry_sandbox/test_package1/poetry_test$ python -c 'import requests'
(poetry-test-py3.11) satoshi@server:/developer/poetry_sandbox/test_package1/poetry_test$ 
```

### pyproject.tomlファイルを確認し、dependenciesセクションにrequestsが追加されているかどうかを確認
```
$ cat pyproject.toml 
[tool.poetry]
name = "poetry-test"
version = "0.1.0"
description = ""
authors = ["satoshi <satoshi@kawagucchi.net>"]
readme = "README.md"
packages = [{include = "poetry_test"}]

[tool.poetry.dependencies]
python = "3.11.4"
requests = "^2.31.0"


[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```
