import requests
import pandas as pd
from math import sqrt
import time 


def distance(x1,x2,y1,y2):
    return sqrt((x1-x2)**2 + (y1 - y2)**2)




KEY = "f3a0082fd7354815bae4cf2f8ddeee19"
#KEY = "aa330cf999c54aefaec1382cfc1bf007"

face_api_url = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'

headers = { 
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': KEY }

params = {
    'returnFaceId': 'false',
    'returnFaceLandmarks': 'true',
    'returnFaceAttributes': 'gender,smile'
}

index_of_windows=['pupilLeft', 'pupilRight', 'noseTip', 'mouthLeft', 'mouthRight', \
'eyebrowLeftOuter', 'eyebrowLeftInner', 'eyeLeftOuter', 'eyeLeftTop', 'eyeLeftBottom', \
'eyeLeftInner', 'eyebrowRightInner', 'eyebrowRightOuter', 'eyeRightInner', 'eyeRightTop',\
 'eyeRightBottom', 'eyeRightOuter', 'noseRootLeft', 'noseRootRight', 'noseLeftAlarTop', \
 'noseRightAlarTop', 'noseLeftAlarOutTip', 'noseRightAlarOutTip', 'upperLipTop', \
 'upperLipBottom', 'underLipTop', 'underLipBottom']

col = ["%s - %s" % (i,j) for i in index_of_windows for j in index_of_windows 
    if index_of_windows.index(i) < index_of_windows.index(j) ]
col.append('smile')
col.append('sex')
col.append('target')

dataFrame = pd.DataFrame(columns = col)
file = open("way.txt",'r')

for ways in file.readlines():
    time.sleep(2.5)
    values = []
    way = ways.split('/')
    target = 'extra'
    name_index = way [2].rstrip()
    

    with open(ways.rstrip()[2:],'rb') as f:
        img_data = f.read()

    try:
        # Execute the api call as a POST request. 
        # What's happening?: You're sending the data, headers and
        # parameter to the api route & saving the
        # mcs server's response to a variable.
        # Note: mcs face api only returns 1 analysis at time
        response = requests.post(face_api_url,
                                data=img_data, 
                                headers=headers,
                                params=params)
        
        # json() is a method from the request library that converts 
        # the json reponse to a python friendly data structure
        parsed = response.json()

        dict_landamarks =  parsed[0].get("faceLandmarks")   
        values = [ distance( dict_landamarks.get(i).get("x"), dict_landamarks.get(j).get("x"),\
        dict_landamarks.get(i).get("y"), dict_landamarks.get(j).get("y") ) \
        for i in index_of_windows for j in index_of_windows 
            if index_of_windows.index(i) < index_of_windows.index(j) ]

        
        
        values.append(parsed[0].get('faceAttributes').get('smile'))
        values.append(0 if parsed[0].get('faceAttributes').get('gender') != 'male' else 1)
        values.append(target)

        temp = pd.Series(values,index=col)
        dataFrame = dataFrame.append(temp,ignore_index=True)

    except Exception as e:
        print('Error - ',e ,' in :',ways.rstrip()[2:])
    
dataFrame.to_csv('matrix_extra.csv', sep=';', encoding='utf-8')