# :pushpin: 시계열 예측 모델을 이용한 intel 주식 종가 예측
>시계열 예측 모델을 이용하여 intel의 주식 종가를 예측(미니 프로젝트)

</br>

## 1. 제작 기간 & 참여 인원 및 역할
- 2022년 3월 28일 ~ 4월 1일
- 한양대학교 산학협력단(K-digital training)/미니 프로젝트
- 총 인원 5인
- 역할: 팀원

#### `활동내역`
- 프로젝트 운영 및 관리 지원
- 시계열 머신러닝 알고리즘 조사 및 모델제작
- 머신러닝 학습 환경 구축
- BiLSTM, GRU 알고리즘 논문 조사 및 모델제작
- Tensorflow, CUDA/cuDNN 환경 구축


</br>

## 2. 사용 기술
#### `시스템`
  - Windows 10 SP2
  - CUDA 11.3
  - cuDNN 8.2.1
  - Anaconda
#### `예측 모델`
  - Python 3.8.10
  - Tensorflow 2.8.0
  - Pandas 1.4.0
  - Keras
  - Numpy


</br>

## 3. 모델 별 결과치
### 3.1. 13개 변수/window size: 50/Patience: 15/Epoch: 200
![](https://user-images.githubusercontent.com/81274469/175939431-d1e19dd6-bede-49b4-bbd8-d173c9fab85a.png)
### 3.2. 17개 변수/window size: 50/Patience: 15/Epoch: 200
![](https://user-images.githubusercontent.com/81274469/175939438-61992f5d-2a4e-4a7f-bdbb-e7d5cd317862.png)


## 4. 핵심 기능
CNN 1차원 레이어를 통해 분석 데이터를 3차원화 한 후 양방향 LSTM을 이용하여 시계열 예측 진행함.

- Yahoo finance api를 이용하여 주가지수/원자재/국채 금리/경쟁사 주가 등의 데이터를 수집함.
- 2017년 1월 1일 부터 2020년 12월 31일 까지를 Train Set으로, 2021년 1월 1일부터 2021년 12월 31일 까지를 Test Set으로 설정하였음.


### 4.1. 양방향 LSTM 선정 배경
![](https://user-images.githubusercontent.com/81274469/175882621-a02b7389-6570-4580-a45e-21749adbdac6.JPG)
- **시스템 동작 흐름**
     1. CCTV 영상이 Spark 안에서 Python을 기반으로 OpenCV를 통해 Frame단위로 쪼개어짐.
     2. OpenCV를 이용하여 MariaDB에 카메라 ID, 탐지된 이상행동의 종류, 금지구역 좌푯값을 저장.
     3. OpenCV에서 Frame 단위로 쪼개어준 영상 이미지를 바탕으로 YOLOv5와 DeepSORT 모델이 적용되어 Bbox를 검출함. 이를 바탕으로 설정하는 경계선에 다시 OpenCV가 색을 입혀 도형화함. Bbox는 객체를 인지한 후 인식된 객체의 중간 점으로 예상되는 픽셀값을 지칭하는 값으로, 우리 모델에서는 이를 기반으로 객체를 추적하고, 도형화함.
     4. 분석된 Frame을 JPG 형태로 인코딩하여 Byte 데이터로 변환하고 MongoDB와 Kafka에 실시간으로 처리되는 데이터를 저장함.
     5. 이상행동 탐지 과정에서 생성되는 Meta Data에 따라 카카오톡 API를 통한 사용자 경고 메시지가 발송됨. 
     6. Django 에서 구동되는 웹 서버에 사용자가 접속하면 MariaDB에 저장된 사용자 계정정보와 요청정보가 일치할 때 웹 대시보드에 접속할 수 있음.
     7. Django 에서 구동되는 웹 서버에서 Kafka로부터 수신하는 JPG 형식의 Byte 데이터를 M-JPEG 압축 방식으로 웹 대시보드에 영상 형태로 출력함.
     8. Django 메인 페이지에 내장되어있는 Grafana 대시보드가 MariaDB 안의 MetaData를 시각화하고 이를 이용하여 패턴이나 시계열 분석을 할 수 있음.




- **다중객체 탐지(MOT) 기반의 이상행동 탐지 기능 구현**
  - 기존의 YOLOv5 기반 알고리즘은 다중객체가 탐지될 때 인원이 특정되지 않아서 지속해서 오류가 발생하였음.
  - 다중으로 객체가 탐지될 때 이를 특정하는 값이 필요하였음.
  - 객체를 특정하는 ID 값을 부여하기 위하여 DeepSORT와 YOLOv5를 통합하였음.
  - DeepSORT는 다중객체 탐지(MOT) 알고리즘의 일종으로 정확성은 조금 떨어져도 처리 속도가 빨라 실시간성을 확보하기 쉬웠음.
  - DeepSORT를 통해 산출되는 ID 값을 이용하여 객체를 특정하는 것으로 알고리즘을 수정하였고 이를 통해 많은 객체를 동시에 탐지하는 기능과 객체 탐지 수에 따라 발생하던 오류를 해결할 수 있었음.
</div>
</details>
