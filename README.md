# 2023ESWContest_free_1029
# 생동감 있는 미술관 관람을 위한새로운 초지향성 스피커
:mag_right: 개요1.   
현대 시대의 미술관, 박물관은 단순히 관람객만 수용하는 것이 아니라 적극적으로 관람의수요를 창출하는 시대로 접어들었다. 나아가 국가 및 지역의 이미지를 창출하여 경제 영역에서도 차츰 중요한 부분을 차지하고 있다.
  
:mag_right: 개요2.  
이러한 맥락에서 현재 많은 미술관, 박물관들은 관람객이 더 작품에 몰입할 수 있도록 기반을 조성하고 있지만 조용한 미술관, 박물관 특성상 작품의 설명을 글로 읽는 것 말고는 작품에 더 몰입할 수 있는 요소가 제한된다.
  
:mag_right: 개요3.  
관람객의 작품 이해를 돕고 생동감 있는 관람을 위해 영상분석 기반으로 관람객을 인식하고, 특정 구역에서만 소리를 들을 수 있는 초지향성 스피커 개발을 목표로 하였다.
  

## 서비스모델
![image](https://raw.githubusercontent.com/Const4nt0228/2023ESWContest_free_1029/main/img/servicemodel.png?token=GHSAT0AAAAAACG5SIJV5HOLHOTT36IOX4EMZHOZWIA)

## 개발환경
![image](https://github.com/Const4nt0228/2023ESWContest_free_1029/blob/main/img/enviroment.png)

## 파일구성
![image](https://github.com/Const4nt0228/2023ESWContest_free_1029/blob/main/img/folder_2.png)  

:page_with_curl: class_faceDetector   
라즈베리파이 구동 코드, 영상처리 Rest API 송신   

:page_with_curl: servoModule (currently version deprecated!)    
Servo motor 제어  

:page_with_curl: [haarcasecade_frontalface_default.xml, apache 2.0 license](https://github.com/opencv/opencv).  
얼굴인식 라이브러리  

:page_with_curl: app    
flask API Server, Rest API, Video Frame    

:page_with_curl: main_client_face    
클라이언트 GUI Software with opencv, Rest API, Control   

:page_with_curl: def_api_request    
for Client's API Request module    

:page_with_curl: ui_client    
for Client's ui file    


## 흐름도
![image](https://github.com/Const4nt0228/2023ESWContest_free_1029/blob/main/img/flow.png)
