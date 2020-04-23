from flask import Flask, render_template, url_for, request, redirect, Response, stream_with_context
import time
from imageai.Detection import ObjectDetection
import requests as r
import cv2
import numpy as np
import random
from gtts import gTTS 
import os

import playsound
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


# def audio_response():
# #     l=["dog"]
#     for x in range(2):
# #         s="static/audio/{}.mp3".format(l[x])
#         with open("static/audio/bark.mp3", "rb") as aud:
#             data = aud.read(1024)
#             while data:
#                 yield data
#                 data = aud.read(1024)
            
#         time.sleep(5.0)
# #     return redirect('/index.html')


# @app.route('/audio')
# def audio():
#     return Response(audio_response(), mimetype='audio/x-mp3')

class main():
    def __init__(self):
        
        self.detector = ObjectDetection()
        self.model_path = "static/yolo.h5"      #actual path

        self.detector.setModelTypeAsYOLOv3()
        self.detector.setModelPath(self.model_path)
        self.detector.loadModel()
        
url="http://192.168.43.225:8080/shot.jpg" #ip webcam url        
    
        
@app.route('/index', methods=['POST'])
def index_func():
    try:

        s=main()
        z=0
        while True:

            res= r.get(url)
            arr=np.array(bytearray(res.content), dtype=np.uint8)
            img=cv2.imdecode(arr,-1)
#             gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cv2.imwrite("static/detectionimage/a{}.jpeg".format(z),img)


            input_path = "static/detectionimage/a{}.jpeg".format(z)
            output_path = "static/output/a{}.jpeg".format(z)
            detection = s.detector.detectObjectsFromImage(input_image=input_path, output_image_path=output_path)
            a=""
            obj=set()
            for d in detection:
                obj.add(d['name'])
            language = 'en'
            if len(obj)==0:
                sss="It seems to be nothing on your way"
                speech = gTTS(text = sss, lang = language, slow = False)
            else:

                fin='and'.join(obj)

                ss1="Hey!! Their is {} on your way.".format(fin)
                ss2="Hey!! I found {} their.".format(fin)
                ss3="Their is {} in front of you.".format(fin)
                x=random.randrange(1,4)
                if x==1:
                    speech = gTTS(text = ss1, lang = language, slow = False)
                elif x==2:
                    speech = gTTS(text = ss2, lang = language, slow = False)
                elif x==3:
                    speech = gTTS(text = ss3, lang = language, slow = False)

            speech.save("static/audio/a{}.mp3".format(z))
            playsound.playsound("static/audio/a{}.mp3".format(z),True)
    #         time.sleep(5)
    #         os.remove("static/audio/a{}.mp3".format(z))
            z+=1
    except:
            return render_template('output.html')


if __name__ == '__main__':
    app.run(debug=True)
