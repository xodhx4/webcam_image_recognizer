"""Label video file and save image.

You could load video with label.
Then you could save frame as image at './train/{label}'.
And this dataset is used to train your own model

USAGE:
    python labeling.py labeling --label LABEL --videoname VIDEO_PATH
"""
import cv2
import os
import fire
from util import makepath
from copy import deepcopy
from datetime import datetime


class Labeler(object):
    def __init__(self, label, videoname):
        """Init label, and video and make label dir if not exist.

        Args:
            label (string): The name of class you wanted to train your classifier 
            videoname (string): The path for video to labeling 
        """
        # Set label and video name
        self.label = label
        self.videoname = os.path.join(os.getcwd(), "record", videoname)

        # Set path for dataset
        trainpath = os.path.join(os.getcwd(), "train")
        self.labelpath = os.path.join(trainpath, label)

        # Create dir if not exist
        makepath(trainpath)
        makepath(self.labelpath)
        self._check_video()

    def _check_video(self):
        """Check if video is not exist
        """
        if not os.path.exists(self.videoname):
            raise FileNotFoundError()

    def labeling(self):
        """Load video and labeling.

        There exist 2 mode seperately
        'playmode' : Automatically play the video. If not, you could pass frame by press any key except reserved key.
        'capturemode' : Save frame that shown in monitor. So this should be turn on when object you what to train is on frame.
        You could watch which mode you are at video left top.
        The default mode is not playmode, not capturemode.

        RESERVED KEY:
            'q' : stop labeling
            's' : change playmode
            'c' : change capturemode
            ':{number}f' : You could pass the frame you want.
                For example, if you press ':500f', then it will pass 500 frames.
        """
        # Open webcam and set defualt mode
        cap = cv2.VideoCapture(self.videoname)
        playmode = False
        capturemode = False

        count = 0
        framelist = list()
        namelist = list()

        # Start labeling
        while(cap.isOpened()):
            name = os.path.join(
                self.labelpath, f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}-{count}.jpg")
            ret, frame = cap.read()

            # If can't read video, end program
            if not ret:
                break

            # If capture mode is on, append frame to savelist
            if capturemode:
                # cv2.imwrite(name, frame)
                framelist.append(deepcopy(frame))
                namelist.append(name)
                count += 1

            # Show frame with info about mode
            info = f"Playmode : {playmode} | Capturemode : {capturemode}"
            cv2.putText(frame, info, (5, 20),
                        cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0))
            cv2.imshow('frame', frame)

            # If playmode, wait key about fps time. Else wait until key pressed
            if playmode:
                key = cv2.waitKey(int(1000/30)) & 0xFF
            else:
                key = cv2.waitKey(0) & 0xFF

            # Change playmode
            if key == ord('s'):
                playmode = not playmode
            # Stop video
            elif key == ord('q'):
                break
            # Chagne capturemode
            elif key == ord('c'):
                capturemode = not capturemode
            # Pass frame
            elif key == ord(':'):
                order = ":"
                cv2.putText(frame, order, (5, 400),
                            cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0))
                cv2.imshow('frame', frame)
                key = cv2.waitKey(0) & 0xFF
                try:
                    while(key != ord('f')):
                        order += chr(key)
                        cv2.putText(frame, order, (5, 400),
                                    cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0))
                        cv2.imshow('frame', frame)
                        key = cv2.waitKey(0) & 0xFF
                    moveframe = int(order[1:-1])
                    for i in range(moveframe):
                        cap.read()
                except:
                    print(f"Input is something wrong {order}")

        cap.release()
        cv2.destroyAllWindows()

        # Save frame in savelist
        for i in range(count):
            cv2.imwrite(namelist[i], framelist[i])


if __name__ == '__main__':
    fire.Fire(Labeler)
