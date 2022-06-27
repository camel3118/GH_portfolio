import os 
import requests
import json
#카카오톡 무료 메시지 전송기능 사용 관계로 토큰 재발급 받아야 함.
#https://kauth.kakao.com/oauth/authorize?response_type=code&client_id=b9c7ed4d6ad2545d1a5430733d9e79ad&redirect_uri=http://14.7.128.55:40000/View/Dashboard
# url = "https://kauth.kakao.com/oauth/token"

# data = {
#     "grant_type" : "authorization_code",
#     "client_id" : "b9c7ed4d6ad2545d1a5430733d9e79ad",
#     "redirect_uri" : "http://14.7.128.55:40000/View/Dashboard",
#     "code" : "-GWNbMxfGpyYfPuIbwMAGQaEcxk-dh0oAk1eUUn3n4K8nvGp7vh1T_wQCMM-r7lqyaMkTAo9dRsAAAGBW37Ebw"
# }
# response = requests.post(url, data=data)

# tokens = response.json()

# print(tokens)
# # import mysql.connector
import os
from datetime import datetime
import requests
import json
#https://kauth.kakao.com/oauth/authorize?response_type=code&client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}
def sendToMeMessage(text):
    header = {"Authorization": 'Bearer ' + '_eu0z2CcufYxeVCyUl_5RBxBHPX_nea2LF8pm1N6CinJXwAAAYFbf3yB'}
    
    url1 = "https://kapi.kakao.com/v2/api/talk/memo/default/send" #나에게 보내기 주소

    post = {
        "object_type": "text",
        "text": text,
        "link": {
            "web_url": "http://14.7.128.55:40000/View/Dashboard"},
            "button_title": "HOT6 홈페이지"
    }    
    data5 = {"template_object": json.dumps(post)}
    
    return requests.post(url1, headers=header, data=data5)
text = '성공입니다.'
print(sendToMeMessage(text).text)


