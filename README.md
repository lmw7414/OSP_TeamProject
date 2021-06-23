# OSP_TeamProject

about Corona
1. 리눅스 환경에 맞도록 그리고 원활히 작동하도록 하기 위해 설치가 필요한 요소들이 있습니다.
2. 우선 리눅스의 shell 창에 엘라스틱서치 파일이 다운될 수 있도록 아래의 명령어를 입력해주세요. 
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.6.2-linux-x86_64.tar.gz
3. 엘라스틱 서치 파일의 압축을 바탕화면에다가 푼 후 쉘창을 통해서 해당 디렉토리로 들어가 줍니다. 그리고 아래의 코드처럼 입력 후 elasticsearch를 구동시켜주세요.

 ![사용설명서1](https://user-images.githubusercontent.com/18253618/123070172-7cb97a80-d44e-11eb-9b70-b91a7cc3035f.jpg)

4. main 브랜치에 있는 전체파일을 다운받은 후 바탕화면에서 압축을 풀어줍니다.
5. 실행환경을 setup하고 자동으로 실행하기 위해서 자동 실행 쉘 스크립트 파일인 setting.sh를 실행시켜줘야 합니다.(이미 elasticsearch가 구동되어 있는 경우에는 다른 쉘 창을 띄워서 진행해주세요.) 만약 자신의 환경에서 pip3 version을 이용한다면 setting.sh를 그냥 pip version을 이용한다면 setting2.sh 파일을 실행시켜주세요. 설치는 한번으로 충분하니 이후에 flask를 구동할 경우에는 해당 디렉토리의 app.py(./app.py)를 실행시켜주세요. 그리고 추가적으로 python3 version을 이용한다면 app.py의 상단 코드를 python -> python3로 변경해주어야 합니다.
6. shell창에 나오는 링크 (http://127.0.0.1:5000) 로 접속해주세요.
