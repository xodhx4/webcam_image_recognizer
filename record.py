"""Record your video from webcam.

Record video by using your webcam.
You could pause recording by press key 's'.
And quit record by pressing key 'q'.
Basic folder for saving video is './record'.
You could change saving folder by option '--path'.

USAGE:
    python record.py record [--path PATH]
    
"""
import os
import cv2
import fire
from datetime import datetime
from util import makepath


class Recoder(object):
    """Class for recoring
    """

    def __init__(self, path=os.path.join(os.getcwd(), "record")):
        """Set saving path and if path not exist, make directory.

        Args:
            path (string): Defaults to os.path.join(os.getcwd(), "record"). Path for saving record.
        """
        self.path = path
        makepath(self.path)

    def record(self):
        """Start recording and save.
        """
        cap = cv2.VideoCapture(0)
        # https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_video_display/py_video_display.html
        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        name = os.path.join(
            self.path, f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.avi")
        out = cv2.VideoWriter(name, fourcc, 30.0, (640, 480))

        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:

                out.write(frame)

                cv2.imshow('frame', frame)
                key = cv2.waitKey(1)
                if key & 0xFF == ord('q'):
                    break
                elif key & 0xFF == ord('s'):
                    if (cv2.waitKey(0) & 0xFF == ord('s')):
                        pass
            else:
                break

        # Release everything if job is finished
        cap.release()
        out.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    fire.Fire(Recoder)
