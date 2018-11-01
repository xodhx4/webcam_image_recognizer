import os

def makepath(path):
    if not os.path.exists(path):
        os.mkdir(path)
        print(f"Make folder :  {path}")