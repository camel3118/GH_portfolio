# GH_portfolio

1. 실시간 지능형 Smart CCTV 솔루션
-개요
주관: 한양대학교 산학협력단(K-digital Training)
기간: 2022.4.04~2022.6.15
참여인원: 서근하, 최성경, 이규동, 김동민, 노인재 등 6인
역할: 팀 리더
활동 내역:
     ㅇ System Architecture 구상/제작
     ㅇ Product Backlog/Splint Plan 계획/작성
     ㅇ Prototype 가정/기능 수준 설정
     ㅇ 스크럼 미팅 진행
     ㅇ 멘토 미팅 진행
     ㅇ Linux PC1(Ubuntu local PC) 시스템 구축/제공/관리
     ㅇ Linux PC2(Ubuntu local PC) 제공/관리
     ㅇ CUDA/cuDNN 환경 구축
     ㅇ Azure VM 관리
     ㅇ YOLOv5/Deepsort 사전학습 모델적용 코드 작성
     ㅇ YOLOv5 사전학습 모델 전이 학습
     ㅇ ‘쓰러짐’ 이상행동 탐지 기초기능 구현
     ㅇ ‘배회’ 이상행동 탐지 기능 구현
     ㅇ spark(분산 처리) / Kafka(분산 저장) 시스템 구축
     ㅇ M-JPEG 영상 재생 기능 구현
     ㅇ Linux 장비 원격 접속 기능 구축


2. 시계열 모델을 이용한 intel 주식 종가 예측(미니 프로젝트)
-개요
기간: 2022.3.28~2022.4.01
참여인원: 서근하, 이지은, 김민지, 박지연, 정다은 등 5인
역할: 팀원
활동 내역:
      ㅇ 프로젝트 운영 및 관리 지원
      ㅇ 시계열 머신러닝 알고리즘 조사 및 모델제작
      ㅇ 머신러닝 학습 환경 구축
      
# :pushpin: 실시간 지능형 Smart CCTV 시스템 구축
>실시간 영상분석 이용한 이상행동 탐지 시스템  

</br>

## 1. 제작 기간 & 참여 인원 및 역할
- 2022년 4월 4일 ~ 6월 15일
- 한양대학교 산학협력단(K-digital training)
- 총 인원 6인
- 역할: 팀 리더

#### `활동내역`
- System Architecture 구상/제작
- Product Backlog/Splint Plan 계획/작성
- Prototype 가정/기능 수준 설정
- 스크럼 미팅 진행
- 멘토 미팅 진행
- Linux PC1(Ubuntu local PC) 시스템 구축/제공/관리
- Linux PC2(Ubuntu local PC) 제공/관리
- CUDA/cuDNN 환경 구축
- Azure VM 관리
- YOLOv5/Deepsort 사전학습 모델적용 코드 작성
- YOLOv5 사전학습 모델 전이 학습
- ‘쓰러짐’ 이상행동 탐지 기초기능 구현
- ‘배회’ 이상행동 탐지 기능 구현
- spark(분산 처리) / Kafka(분산 저장) 시스템 구축
- M-JPEG 영상 재생 기능 구현
- Linux 장비 원격 접속 기능 구축

</br>

## 2. 사용 기술
#### `시스템`
  - Spark 3.0.2
  - Hadoop Yarn 2.7.7
  - Kafka 2.8.0
  - Zookeeper 3.8.0
  - MongoDB 4.4.13
  - MariaDB 10.3.34
  - Ubuntu 18.04
  - Azure Cloud
  - CUDA 11.3
  - cuDNN 8.2.1
#### `영상 처리`
  - Python 3.8.10
  - Pytorch 1.11.0
  - OpenCV 4.5.3
  - YOLOv5
  - DeepSORT
#### `웹 배포`
  - Django 4.0.5

</br>

## 3. 논리적 시스템 구성도
![](https://zuminternet.github.io/images/portal/post/2019-04-22-ZUM-Pilot-integer/final_erd.png)


## 4. 핵심 기능
본 시스템의 핵심 기능은 크게 3가지로 나뉩니다.
1. 실시간 CCTV 영상에서 이상행동을 탐지한다.
2. 탐지된 이상행동(침입,배회,쓰러짐,화재감지)을 사용자에게 경고한다.
3. 객체 탐지 및 이상행동 탐지 후처리가 완료된 CCTV 영상을 웹을 통해 실시간으로 송출한다.
MVP(최소기능제품) 제작을 위해 애자일 방법에 따라 개발을 진행하였습니다.
이상행동의 정의는 KISA 지능형 CCTV 인증기준을 참고 하였습니다.

<details>
<summary><b>핵심 기능 설명 펼치기</b></summary>
<div markdown="1">

### 4.1. 물리적 시스템 구성도
![](https://zuminternet.github.io/images/portal/post/2019-04-22-ZUM-Pilot-integer/flow1.png)
- **시스템 동작 흐름**
     1. CCTV 영상이 Spark 안에서 Python을 기반으로 OpenCV를 통해 Frame단위로 쪼개어짐.
     2. OpenCV를 이용하여 MariaDB에 카메라 ID, 탐지된 이상행동의 종류, 금지구역 좌푯값을 저장.
     3. OpenCV에서 Frame 단위로 쪼개어준 영상 이미지를 바탕으로 YOLOv5와 DeepSORT 모델이 적용되어 Bbox를 검출함. 이를 바탕으로 설정하는 경계선에 다시 OpenCV가 색을 입혀 도형화함. Bbox는 객체를 인지한 후 인식된 객체의 중간 점으로 예상되는 픽셀값을 지칭하는 값으로, 우리 모델에서는 이를 기반으로 객체를 추적하고, 도형화함.
     4. 분석된 Frame을 JPG 형태로 인코딩하여 Byte 데이터로 변환하고 MongoDB와 Kafka에 실시간으로 처리되는 데이터를 저장함.
     5. 이상행동 탐지 과정에서 생성되는 Meta Data에 따라 카카오톡 API를 통한 사용자 경고 메시지가 발송됨. 
     6. Django 에서 구동되는 웹 서버에 사용자가 접속하면 MariaDB에 저장된 사용자 계정정보와 요청정보가 일치할 때 웹 대시보드에 접속할 수 있음.
     7. Django 에서 구동되는 웹 서버에서 Kafka로부터 수신하는 JPG 형식의 Byte 데이터를 M-JPEG 압축 방식으로 웹 대시보드에 영상 형태로 출력함.
     8. Django 메인 페이지에 내장되어있는 Grafana 대시보드가 MariaDB 안의 MetaData를 시각화하고 이를 이용하여 패턴이나 시계열 분석을 할 수 있음.


### 4.2. Software/Hardware 배치도


- **Software 배치도**
     ![](https://zuminternet.github.io/images/portal/post/2019-04-22-ZUM-Pilot-integer/flow_vue.png)
  - 각 Server는 Linux 기반의 Ubuntu 18.04 버전 OS를 바탕으로 구성됨.
  - CUDA / cuDNN은 머신러닝 구동 시 GPU를 사용하여 처리 속도를 올리기 위한 라이브러리 임.
  - RDBMS로 MariaDB를 채택하여 구축하였고, Nosql로 MongoDB를 구축하였음.
  - 분산 저장소로 Zookeeper 기반의 Kafka를 Cluster 구성하였음.
  - Hadoop Yarn을 이용하여 Spark Master와 Worker node들을 Cluster로 구성함.
  - 각 Spark node 안에는 모델 구동에 필요한 Pytorch, OpenCV, YOLOv5, DeepSORT 등이 구축됨.
     
 - **Hardware 배치도**
     ![](https://zuminternet.github.io/images/portal/post/2019-04-22-ZUM-Pilot-integer/flow_vue.png)
  - 각 Server는 IP 주소로 통신하며 여기에 기반하는 Port 주소를 각 Cluster 마다 할당함.
  - 개인 PC를 기반으로 하는 On-premise Server 1개와 Azure Cloud를 기반으로 하는 VM Server 2개가 엮여 총 3개를 Cluster로 구성함.

### 4.3. 이상행동 탐지 알고리즘


- **침입 탐지 알고리즘**
     ![](https://zuminternet.github.io/images/portal/post/2019-04-22-ZUM-Pilot-integer/flow_vue.png)
  - 침입은 사용자 설정 구역에 객체의 몸 전체가 들어가야 한다는 기준을 가지고 탐지함.
  - 객체를 탐지할 때 생기는 Bbox의 꼭지점을 포인트로 지칭하고 사용자 설정구역을 다각형으로 지칭할 때, 다각형 내부에 포인트가 있는지 판별하는 것이 기능 구현의 핵심임.
  - 포인트에서 오른쪽으로 직선을 그었을 때 직선의 접점 개수가 홀수면 다각형의 내부, 짝수면 외부로 판별함.
  - Bbox는 총 4개의 포인트가 있고 포인트 모두 내부로 판별되었을 때 침입으로 탐지함.

     
- **배회 탐지 알고리즘**
     ![](https://zuminternet.github.io/images/portal/post/2019-04-22-ZUM-Pilot-integer/flow_vue.png)
  - 배회는 객체의 몸 전체가 사용자 설정구역에서 10초 이상 머무는 것을 기준으로 탐지함.
  - 침입 탐지 알고리즘을 기본 조건으로 하여 작동함.
  - 위 사진과 같이 객체별로 등장한 프레임 수를 세어서 시간 개념으로 변환함.
  - 30fps의 영상에서 특정 객체가 등장한 프레임 수가 300이면 10초의 시간으로 인식되어 배회를 탐지함.
 
- **쓰러짐 탐지 알고리즘**
     ![](https://zuminternet.github.io/images/portal/post/2019-04-22-ZUM-Pilot-integer/flow_vue.png)
  - 쓰러짐은 사람이 주저앉거나 실신한 상태를 기준을 탐지함.
  - 객체가 쓰러졌을 때 Bbox의 가로와 세로 비율이 반전됨.
  - Bbox 대각선 위치의 꼭짓점을 서로 연결했을 때 교차점의 각도를 연산하여 기능을 구현함.
  - 객체가 잠깐 주저앉았을 때 쓰러짐으로 탐지하는 것을 보완하고자 쓰러진 상태가 일정 시간 유지되었을 때만 사용자에게 알람이 발송됨.
  - 객체가 화면 가장자리에서 등장할 때 몸의 일부만 탐지되면 Bbox의 비율이 반전되기 때문에 Bbox의 y값과 화면의 가장자리가 겹치는 경우를 배제함.
     
- **화재 탐지 모델**
     ![](https://zuminternet.github.io/images/portal/post/2019-04-22-ZUM-Pilot-integer/flow_vue.png)
  - 화재 탐지 모델은 이상행동 탐지 모델과는 별개로 YOLOv5 가중치 값에 전이 학습을 하여 구축함.
  - 화재 이미지 데이터 약 400장을 labeling하고 훈련데이터와 검증데이터를 8:2로 학습을 진행함.
  - 0.5 이상의 예측 정확도를 가진 Bbox가 화면에 출력됨.



### 4.3. 모델 성능 평가
- **모델 성능 평가**
     ![](https://zuminternet.github.io/images/portal/post/2019-04-22-ZUM-Pilot-integer/flow_vue.png)
  - KISA 지능형 CCTV 인증기준 기반 모델 성능 테스트를 진행함.
  - KISA에서 제공하는 테스트 프로그램 사용하여 결과값 측정함.
  - 침입/쓰러짐/배회/화재탐지 등 4가지 이상행동에 대해 실시함. 
  - 1차 성능테스트 결과 종합 평균 50점을 획득함.
  - 모델 성능개선 후 2차 성능테스트 결과 종합 평균 93.8점 획득함.



### 4.4. Django 이용 웹 배포
- **Django 템플릿** 
![](https://zuminternet.github.io/images/portal/post/2019-04-22-ZUM-Pilot-integer/flow_repo.png)
![](https://zuminternet.github.io/images/portal/post/2019-04-22-ZUM-Pilot-integer/flow_repo.png)
![](https://zuminternet.github.io/images/portal/post/2019-04-22-ZUM-Pilot-integer/flow_repo.png)
     
  - URL 유효성 체크와 이미지, 제목 파싱이 끝난 컨텐츠는 DB에 저장합니다.
  - 저장된 컨텐츠는 다시 Repository - Service - Controller를 거쳐 화면단에 송출됩니다.

</div>
</details>

</br>

## 5. 문제점 및 해결방안
### 5.1. 프로젝트 운영 
- **업무 분담 효율성 재고**
  - 업무 분담의 효율성을 높이고자 시스템/모델 개발팀으로 양분하여 진행함.
  - 개발 과정에서 오류 해결이나 난이도가 높은 분야는 조장이 지원하여 진행함.
  - 소요 예정 시간 측정은 데일리 스크럼을 확인하며 수정하여 반영함.
  - 데일리 스크럼 링크(https://docs.google.com/spreadsheets/d/1aB71318qFPvctYozDlna_jfL3CwMJ9wt6Jw-sxy3WIU/edit?usp=sharing)

- **User story 선정 및 개발 수준 설정**
  - 계획 및 분석 초기에 지능형 CCTV에 대한 파악이 덜 되어 User story 선정 및 개발 수준 설정이 불가하였음.
  - 계획 및 분석 단계에서 많은 시간을 소모할 때 2개월의 한정된 기간 안에 결과물을 만들기 위해서는 개발 일정이 부족할 것으로 판단하였음.
  - 이에 최소기능제품 프로토타입 제작으로 목표를 설정하고 User story 기반의 Agile 방식으로 개발을 진행하였음.
  - 이상행동 탐지를 최우선 목표로 User story를 선정하여 Sprint #1과 #2를 진행 하였음.
  - Sprint #1과 #2 진행 과정에서 습득한 지식과 멘토, 담임 강사 등 외부 인원의 피드백 및 자체 피드백을 기반으로 웹 배포, 데이터/시스템 아키텍처 등을 개발하고 테스트를 통해 파악된 기존 이상 탐지 알고리즘의 개선을 목표로 Sprint #3과 #4를 계획하여 진행하였음.
  - Sprint #5 에서는 개선된 이상 탐지 알고리즘의 검증을 위하여 KISA 인증기준을 기반으로 한 검증 기준을 설정하여 정량적인 모델 성능 측정을 하였음.
 
- **팀원 간 의사소통**
  - 개발 초기 생소한 기술의 이해 부족 및 의사소통의 부재 때문에 원활한 개발 진행이 어려웠음.
  - 원활한 업무 진행을 위하여 매일 오전 스크럼 회의 진행을 통해 시스템/모델 팀 간의 의사를 교환하고 관련 지식 전파를 추진함.
  - 개발 속도를 높이기 위하여 팀원들의 스스로 결정할 수 있는 자율성을 강조함.
  - User story 선정 및 업무 분배 등 개발과 관련된 사안은 모두 조원 각자가 스크럼 회의를 통하여 자율적으로 결정하여 진행함.
  - 최종 개발 방향 및 중요 사안의 경우 팀원들과 스크럼 회의를 통해 팀장이 결정함.



### 5.2. 프로토타입 개발 측면
- **Cluster 구축**
  - 분산 처리/저장을 위하여 Spark와 Kafka를 Cluster로 구축함.
  - Cluster 구축 시에 각 장비는 IP 주소와 Port 번호로 통신함.
  - on-premise Server는 공인 IP 하나만 존재하지만, Azure의 경우 외부, 내부 IP가 각각 존재함.
  - Azure 외부 IP로만 설정하여 Azure VM간의 연결이 안 되어 지속적 오류가 발생하였음.
  - 이에 설정값에 Azure 외부, 내부 IP를 병기 하여 두 IP 주소 모두 통신할 수 있게끔 설정하여 오류를 해결하였음.

- **이상행동 알람 기능 구현**
  - 이상행동 발생 여부를 알리는 알람을 이메일로 제공하고자 하였음.
  - 이메일의 경우 관리자가 제대로 확인하지 않을 수 있다는 점이 스크럼 회의에서 피드백으로 제안됨.
  - 이메일을 대체할 다른 알람 방법으로 소리, 앱 알람 등이 제안되었으나 개발 기간을 고려하면 현실성이 떨어진다는 피드백이 나옴.
  - 이에 카카오톡 API를 이용한 카카오톡 알람 기능이 제안되어 무료 버전을 기반으로 이상행동 알람 기능을 구현함.

- **이상행동 중 배회의 시간 개념 설정**
  - 배회의 경우 지정구역 안에서 객체가 10초 이상 탐지될 때 발생함.
  - 10초라는 시간의 개념이 현실과 영상 안에서 다를 수 있기 때문에 이를 모두 포함할 수 있는 개념이 필요하였음.
  - 이에 영상의 프레임 단위를 이용하여 역산하여 시간으로 환산하는 공식을 알고리즘에 포함했음.
  - 예를 들어 초당 30프레임인 영상의 경우 300프레임이 영상에서의 10초이므로 300프레임 이상 배회 행위가 탐지될 때 경고가 발생함.

- **다중객체 탐지(MOT) 기반의 이상행동 탐지 기능 구현**
  - 기존의 YOLOv5 기반 알고리즘은 다중객체가 탐지될 때 인원이 특정되지 않아서 지속해서 오류가 발생하였음.
  - 다중으로 객체가 탐지될 때 이를 특정하는 값이 필요하였음.
  - 객체를 특정하는 ID 값을 부여하기 위하여 DeepSORT와 YOLOv5를 통합하였음.
  - DeepSORT는 다중객체 탐지(MOT) 알고리즘의 일종으로 정확성은 조금 떨어져도 처리 속도가 빨라 실시간성을 확보하기 쉬웠음.
  - DeepSORT를 통해 산출되는 ID 값을 이용하여 객체를 특정하는 것으로 알고리즘을 수정하였고 이를 통해 많은 객체를 동시에 탐지하는 기능과 객체 탐지 수에 따라 발생하던 오류를 해결할 수 있었음.
</div>
</details>
