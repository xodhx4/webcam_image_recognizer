"""Util functions for this package
"""
import os


def makepath(path):
    """Make dir if  not exit.

    Args:
            path (string): The path to check 
    """
    if not os.path.exists(path):
        os.mkdir(path)
        print(f"Make folder :  {path}")
