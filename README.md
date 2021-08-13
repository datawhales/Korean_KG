# Korean_KG
## Introduction
Korean Knowledge Graph Construction.
## Data
한국어-위키피디아 corpus에 대해 Entity Recognition + Relation Extraction을 기반으로 구축된 triple data.
## 데이터 준비
먼저 triple data를 https://github.com/usgnob/KBN-Dataset 에서 다운로드합니다.  
다운로드받은 zip file(`KBN-KO-v1.0.zip`)을 `./data`(`mkdir data`) directory에 위치시키고 `unzip KBN-KO-v1.0.zip`을 통해 압축을 풀어줍니다.  
`data` directory에 생성된 `KBN-KO-v1.0` directory의 이름을 `KBN_data`로 변경합니다(`mv KBN-KO-v1.0 KBN_data`).  
마지막으로 `cd code`를 통해 `code` directory로 이동 후에 `prepare_data.py`를 실행하면 데이터 준비가 완료됩니다.  
코드 실행이 완료되면 `data` directory에 `modified_KBN_data` 폴더와 `rel2id.json`, `train.txt`, `dev.txt`, `test.txt`가 생성된 것을 확인할 수 있습니다.