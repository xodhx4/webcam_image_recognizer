"""Inference real time video from webcam

Load model you choose and turn on vwebcam.
For each frame, classify by model and show on frame

USAGE :
    python inference.py inference --model MODEL_PATH [--path PATH]

TODO :
    [] Save result on json or image
"""
import os
import cv2
import fire
import numpy as np
from keras.models import load_model
from datetime import datetime
from util import makepath

class Inferencer(object):
    def __init__(self, model, path=os.path.join(os.getcwd(), "result")):
        """Init option and make result directory
        
        Args:
            model (string): Path of model for classification
            path (string): Defaults to os.path.join(os.getcwd(), "result"). 
        """
        self.path = path
        makepath(self.path)
        self.model = os.path.join(os.getcwd(), "model", model)

    def _get_label(self):
        """Load label data
        """
        with open(self.model+".txt") as f:
            label = f.readline()
            labellist = label.split(",")

        return labellist

    def inference(self):
        """Inference video from webcam

        Load deep learning model, and classify on real time from webcam video.
        You could quit with press 'q'
        """
        cap = cv2.VideoCapture(0)

        # Load model and label data
        try:
            model = load_model(self.model)
            labellist = self._get_label()
        except Exception:
            print(f"The model {model} may not exist in {self.model}")
            
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret==True:
                # Change frame size to put model
                size = model.layers[0].input_shape[1:3]
                resized_frame = np.expand_dims(cv2.resize(frame, size), axis=0)

                # Predict frame
                result = model.predict(resized_frame)[0]

                start_y = 20

                # Put text of result on frame
                for index, i in enumerate(result):
                    per = int(i*100)
                    info = f"{labellist[index]} : {per}%"
                    cv2.putText(frame, info, (5, start_y), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0))
                    start_y += 20

                # Show frame
                cv2.imshow('frame',frame)
                key = cv2.waitKey(1)

                # Quit program
                if key & 0xFF == ord('q'):
                    break
            else:
                break

        # Release everything if job is finished
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    fire.Fire(Inferencer)

