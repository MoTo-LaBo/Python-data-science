# Python data sience
- Docker を使用した環境構築
  - ANACONDA, Jupyterlab, ubuntu, docker
- Python の基本
- data sience 関連ライブラリ
  - NumPy, Pandas, Matplotlib, OpenCV, etc...
- coding の考え方
- 今回の code はなるべく PEP8 に準拠
> https://www.python.org/dev/peps/pep-0008/
##  環境構築
### 1. docker に login
    docker login
- Login Succeeded  (login 成功)
### 2. docker hub から docker image 取得
    docker pull datascientistus/ds-python-env
- docker pull < image 名>
### 3. docker image 一覧表示
    docker images
### 4. container を立てる
    docker run -v ~/Dropbox/udemy/Python_data_science:/work -p 3333:8888 --name kame-env datascientistus/ds-python-env
- -v option を付けると、container の file system を Host に mount する事ができる
- -p option : port (ポート) Jupyterlab は web のアプリケーション。ネットワークを介してアクセスするものなので、指定した port の上で動かす必要がある
- 今回は *3333*:8888 という port の上で動くようにしてある default の Jupyter の port の番号
- container の port を Host に繋げてあげないと動かない。なので host 側の localhost.8888 に接続すると container 8888 に届くようになっている
-   -- name で container に名前を付ける事ができる
    -   名前を付けないと container の方で default で変な名前が付けられてしまう
### 5.  Lab App 一覧が表示されて Jupyter lab 起動 -> browser に移動
-  ブラウザで **localhost:8888** アクセス
   -  Firefox, chrome が良い
-  Jupyter lab が表示される
-  Docker を使用する事で簡単に data sience の環境構築ができる
   -  docker login -> docker pull < image 名 > -> docker run
   -  ３つのコマンドで完了
### 実は docker の pull は必要がない
  - run をした時に docker image が local host にない場合は自動で pull をして来てくれる
  - 事実上はコマンド 1行で完了できる！！
## Docker の基本操作
#### コンテナ一覧表示
    docker ps -a
### docker image 一覧表示
    docker images
### docker image から container 起動
    docker run -v ~/Desktop/work:/work -p 8888:8888 --name my-env < image名 >
### コンテナを止める
    docker stop < container >
### コンテナを削除
    docker rm < container >
### コンテナを restart
    docker restart < container >
## Jupyterlab
    pip install --upgrade jupyterlab
- まずは upgrade しておく
- version up する事でおかしな挙動の改善ができる
## Docker container とは？
### <u>container は localhost とは独立した環境</u>
- *hostがどういう環境であろうとcontainerを作れば同じ環境になる*
