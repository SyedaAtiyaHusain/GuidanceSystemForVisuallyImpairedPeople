"""
Title: Guidance System For Visually Impaired People
Developed  by: Syeda Atiya Husain, Ashish Kore and Nupur Kshatri.
Language: Python
Requirement:
            Python version: Python 3 or later
            Libraries:1) flask
                      2) imageai
                      3) requests 
                      4) cv2
                      5) numpy
                      6) random
                      7) gtts
                      8) playsound
            Additional files: Yolov3.h5
"""

from flask import Flask, render_template                                                    #Importing necessary libraries
from imageai.Detection import ObjectDetection
import requests as r
import cv2
import numpy as np
import random
from gtts import gTTS 
import playsound
                
                                                        #Initializing flask based app.
app = Flask(__name__)

@app.route('/')      
                                                        #This function will be called on landing up to the above end point.                                                                    
def home():
    
    """
    This function returns a template named "home.html". 
    """
    
    return render_template('home.html')

class main():
    
    """
    This class is defined to create the instantiate objectdetection class and load Yolov3 model.
    """
    
    def __init__(self):
        
        self.detector = ObjectDetection()                          #Creating object of objectdetection class. 
        self.model_path = "static/yolo.h5"                         #Specifying path of yolo model.                                                                  
        self.detector.setModelTypeAsYOLOv3()                       #Selecting model type.
        self.detector.setModelPath(self.model_path)                #Setting path of yolo model.
        self.detector.loadModel()                                  #Loading yolo model.
        
url="http://192.168.43.225:8080/shot.jpg"                          #url for IP Web Camera App Server      
           
@app.route('/index', methods=['POST'])
                                        #This function will be called on landing up to the above end point.
def index_func():
    
    """
    This function upon calling performs object detection task on image obtained from IP web camera.
    Thereafter it generates audio instruction containing names of the object classes.
    This process gets continued on lives images until the user shuts down the IP web camera app.
    """
    
    try:
        s=main()                                                    #Initializing main class object.
        z=0
        while True:
            res= r.get(url)                                         #Hits the IP web camera server url for image response.
            arr=np.array(bytearray(res.content), dtype=np.uint8)
            img=cv2.imdecode(arr,-1)
            cv2.imwrite("static/detectionimage/a{}.jpeg".format(z),img) #saving the response image in JPEG format.
            input_path = "static/detectionimage/a{}.jpeg".format(z)
            output_path = "static/output/a{}.jpeg".format(z)
            detection = s.detector.detectObjectsFromImage(input_image=input_path, output_image_path=output_path) #calling detection
                                                 #function for object detection and storing the object names in list.
            a=""
            obj=set()
            for d in detection:
                obj.add(d['name'])
                                              #generating audio instructions according to objects name list. 
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
            speech.save("static/audio/a{}.mp3".format(z))                   #saving generated audio
            playsound.playsound("static/audio/a{}.mp3".format(z),True)      #playing generated audio
            z+=1
    except:
            return render_template('output.html')                           #returns output.html template when the app is closed.

if __name__ == '__main__':
    app.run(debug=True)
