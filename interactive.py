import cmd
import os
from pyfiglet import Figlet

f = Figlet(font='slant')
print(f.renderText('WEBCAM RECOGNIZER'))


class Recognizer(cmd.Cmd):
    intro = """
    Hello this is interactive shell for webcam recognizer
    You could choose which tool to use
    1 : test
    2 : record
    3 : labeling
    4 : train
    5 : inferace
    6 : analysis
    
    You could read help by type `help <topic>`    
    """
    prompt = "(Recog)"

    def wrong(self, args):
        print(f"Wrong argument number\nYou enter Check help")
        if len(args) == 0:
            print("NO ARG")
        else:
            for i, arg in enumerate(args):
                print(f"{i} : {arg}")

    def parse_arg(self, arg):
        if len(arg) == 0:
            return arg
        else:
            args = arg.split(" ")
            return args

    def do_test(self, arg):
        'Test Webcam with simple code'
        from test import main
        main()

    def do_record(self, arg):
        """
        Test Webcam with simple code

        You could choose directory to save

        USAGE:
            record
            record PATH
        """
        arg = self.parse_arg(arg)
        if len(arg) > 1:
            self.wrong(arg)
        else:
            self.record(arg)

    def do_labeling(self, arg):
        """
        Label video file and save image

        You could choose label and video path by args
        USAGE:
            labeling
            labeling LABEL VIDEO_NAME
        """
        arg = self.parse_arg(arg)
        if len(arg) == 0 or len(arg) == 2:
            self.labeling(arg)
        else:
            self.wrong(arg)

    def do_train(self, arg):
        """
        Make CNN model with your dataset

        If you want to change defualt option,
        try
            train.py
        not interactive.py

        USAGE:
            train
        """
        arg = self.parse_arg(arg)
        if len(arg) == 0:
            self.train()
        else:
            self.wrong(arg)

    def do_inference(self, arg):
        """
        Inference real time video from webcam

        USAGE:
            inference
            inference MODEL_NAME
            inference MODEL_NAME PATH

        """
        arg = self.parse_arg(arg)
        if len(arg) > 2:
            self.wrong(arg)
        else:
            self.inference(arg)
    
    def do_analysis(self, arg):
        print("Sorry, this function is not working now")

    def record(self, arg):
        import record
        if len(arg) == 0:
            rec = record.Recoder()

        else:
            rec = record.Recoder(arg[0])
        rec.record()

    def labeling(self, arg):
        if len(arg) == 0:
            label = input("Enter label name : ")
            video_list = os.listdir(os.path.join(os.getcwd(), "record"))
            print("LIST OF VIDEO\n")
            for index, video in enumerate(video_list):
                print(f"{index} : {video}")
            videopath = input("Enter video path (or Index) : ")
            try:
                videopath=video_list[int(videopath)]
            except:
                pass
        else:
            label = arg[0]
            videopath = arg[1]

        import labeling
        lab = labeling.Labeler(label, videopath)
        lab.labeling()

    def train(self):
        import train
        tra = train.Trainer()
        tra.train()

    def inference(self, arg):
        import inference
        if len(arg) == 0:
            model_list = list(filter(lambda x: x[-2:]=="h5", os.listdir(os.path.join(os.getcwd(), "model"))))
            print("LIST OF MODEL\n")
            for index, m in enumerate(model_list):
                print(f"{index} : {m}")
            model = input("Enter model name (or Index) : ")
            try:
                model=model_list[int(model)]
            except:
                pass
            infe = inference.Inferencer(model=model)
        elif len(arg) == 1:
            infe = inference.Inferencer(model=arg[0])
        else:
            infe = inference.Inferencer(model=arg[0], path=arg[1])

        infe.inference()


if __name__ == "__main__":
    Recognizer().cmdloop()
