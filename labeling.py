import cv2
import os
import fire
from util import makepath
from copy import deepcopy
from datetime import datetime

class Labeler(object):
    def __init__(self, label, videoname):
        self.label = label
        self.videoname = os.path.join(os.getcwd(), "record", videoname)
        trainpath = os.path.join(os.getcwd(), "train")
        self.labelpath = os.path.join(trainpath, label)
        makepath(trainpath)
        makepath(self.labelpath)
        self._check_video()

        
    def _check_video(self):
        if not os.path.exists(self.videoname):
            raise FileNotFoundError()

    def labeling(self):
        cap = cv2.VideoCapture(self.videoname)
        playmode = False 
        capturemode = False 
        count = 0
        framelist = list()
        namelist = list()
        while(cap.isOpened()):
            name = os.path.join(self.labelpath, f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}-{count}.jpg")
            ret, frame = cap.read()
            if not ret:
                break
            if capturemode:
                # cv2.imwrite(name, frame)
                framelist.append(deepcopy(frame))
                namelist.append(name)
                count += 1
            info = f"Playmode : {playmode} | Capturemode : {capturemode}"
            cv2.putText(frame, info, (5, 20), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0))
            cv2.imshow('frame', frame)


            if playmode:
                key = cv2.waitKey(int(1000/30)) & 0xFF
            else:
                key = cv2.waitKey(0) & 0xFF

            if key == ord('s'):
                playmode = not playmode 
            elif key == ord('q'):
                break
            elif key == ord('c'): 
                capturemode = not capturemode
            elif key == ord(':'):
                order = ":"
                cv2.putText(frame, order, (5, 400), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0))
                cv2.imshow('frame', frame)
                key = cv2.waitKey(0) & 0xFF
                try:
                    while(key != ord('f')):
                        order += chr(key)
                        cv2.putText(frame, order, (5, 400), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0))
                        cv2.imshow('frame', frame)
                        key = cv2.waitKey(0) & 0xFF
                    moveframe = int(order[1:-1])
                    for i in range(moveframe):
                        cap.read()
                except:
                    print(f"Input is something wrong {order}")



                        
        
        cap.release()
        cv2.destroyAllWindows()

        for i in range(count):
            cv2.imwrite(namelist[i], framelist[i])
        
        
if __name__ == '__main__':
    fire.Fire(Labeler)