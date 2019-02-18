import hashlib  
import time  
import random  
import string
import requests  
import base64  
import requests
import cv2
import numpy as np
from urllib.parse import urlencode
import json #用于post后得到的字符串到字典的转换
import matplotlib.pyplot as plt
from io import BytesIO
import numpy as np
import urllib.request
import cv2

app_id = '2107872408' 
app_key = 'DvMF4dRYHQccBoiI'

# METHOD #1: OpenCV, NumPy, and urllib
def url_to_image(url):
	# download the image, convert it to a NumPy array, and then read
	# it into OpenCV format
	resp = urllib.request.urlopen(url)
	image = np.asarray(bytearray(resp.read()), dtype="uint8")
	image = cv2.imdecode(image, cv2.IMREAD_COLOR)
	return image

def get_params(img):                         #鉴权计算并返回请求参数
    #请求时间戳（秒级），用于防止请求重放（保证签名5分钟有效
    time_stamp=str(int(time.time())) 
    #请求随机字符串，用于保证签名不可预测,16代表16位
    nonce_str = ''.join(random.sample(string.ascii_letters + string.digits, 16))

    params = {'app_id':app_id,                #请求包，需要根据不同的任务修改，基本相同
              'image':img,                    #文字类的任务可能是‘text’，由主函数传递进来
              'time_stamp':time_stamp,        #时间戳，都一样
              'nonce_str':nonce_str,          #随机字符串，都一样
              #'sign':''                      #签名不参与鉴权计算，只是列出来示意
             }

    sort_dict= sorted(params.items(), key=lambda item:item[0], reverse = False)  #字典排序
    sort_dict.append(('app_key',app_key))   #尾部添加appkey
    rawtext= urlencode(sort_dict).encode()  #urlencod编码
    sha = hashlib.md5()    
    sha.update(rawtext)
    md5text= sha.hexdigest().upper()        #MD5加密计算
    params['sign']=md5text                  #将签名赋值到sign
    return  params                          #返回请求包


def url_ocr(): 
    '''
    #用python系统读取方法
    f = open('c:/girl.jpg','rb')
    img = base64.b64encode(f.read())   #得到API可以识别的字符串
     '''
    #用opencv读入图片
    frame = url_to_image('http://www.tianjin-air.com/captcha/sphinx?timestamp=95')
    #frame=cv2.imread('C:/Users/jtian/Python/out.png')
    plt.imshow(frame)
    plt.show()
    nparry_encode = cv2.imencode('.png', frame)[1]
    data_encode = np.array(nparry_encode)
    img = base64.b64encode(data_encode)    #得到API可以识别的字符串
    #print('img--------->', img)
    params = get_params(img)    #获取鉴权签名并获取请求参数

    url = "https://api.ai.qq.com/fcgi-bin/ocr/ocr_handwritingocr"  # 人脸分析
    #检测给定图片（Image）中的所有人脸（Face）的位置和相应的面部属性。位置包括（x, y, w, h），面部属性包括性别（gender）, 年龄（age）, 表情（expression）, 魅力（beauty）, 眼镜（glass）和姿态（pitch，roll，yaw）   
    res = requests.post(url,params).json()
    print('res--------->', res)



    
def pil_ocr(pil_img): 
    buffered = BytesIO()
    pil_img = pil_img.convert('RGB')
    pil_img.save(buffered, format="JPEG")
    img = base64.b64encode(buffered.getvalue())
    params = get_params(img)    #获取鉴权签名并获取请求参数

    url = "https://api.ai.qq.com/fcgi-bin/ocr/ocr_handwritingocr"  # 人脸分析
    #检测给定图片（Image）中的所有人脸（Face）的位置和相应的面部属性。位置包括（x, y, w, h），面部属性包括性别（gender）, 年龄（age）, 表情（expression）, 魅力（beauty）, 眼镜（glass）和姿态（pitch，roll，yaw）   
    res = requests.post(url,params, timeout=20).json()
    print('res--------->', res)
    return res
    