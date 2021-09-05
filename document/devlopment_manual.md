### 1. image 一覧表示
    docker images
### 2. container 一覧表示
    docker ps -a
### 3. 使用したい image が up かどうか status 確認
    # up でない場合は下記のコマンド実行
    docker restart < container名 >
### 4. image がなければ Docker image から container を起動
    docker run -v ~/Dropbox/udemy/Python_data_science:/work -p 8888:8888 --name kame-env < images ID >
### 5. container を止める
    dockre stop < container名・ID >
### 6. container 削除
    docker rm < container名・ID >
