import os
import cv2
import fire
import numpy as np
from keras.models import load_model
from datetime import datetime
from util import makepath

class Inferencer(object):
    def __init__(self, model, path=os.path.join(os.getcwd(), "result")):
        self.path = path
        makepath(self.path)
        self.model = os.path.join(os.getcwd(), "model", model)

    def _get_label(self):
        with open(self.model+".txt") as f:
            label = f.readline()
            labellist = label.split(",")

        return labellist

    def inference(self):
        cap = cv2.VideoCapture(0)
        # https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_video_display/py_video_display.html
        # Define the codec and create VideoWriter object
        try:
            model = load_model(self.model)
            labellist = self._get_label()
        except Exception:
            print(f"The model {model} may not exist in {self.model}")
            
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret==True:
                
                resized_frame = np.expand_dims(cv2.resize(frame, (64, 64)), axis=0)

                result = model.predict(resized_frame)[0]

                start_y = 20
                for index, i in enumerate(result):
                    per = int(i*100)
                    info = f"{labellist[index]} : {per}%"
                    cv2.putText(frame, info, (5, start_y), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0))
                    start_y += 10


                cv2.imshow('frame',frame)
                key = cv2.waitKey(1)
                if key & 0xFF == ord('q'):
                    break
            else:
                break

        # Release everything if job is finished
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    fire.Fire(Inferencer)

