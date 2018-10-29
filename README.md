# Smiple Webcam Recognizer

[TOC]

## Pre-requirement

```shell
pip install opencv-contrib-python
pip install opencv-python
pip install fire
```



## 1. Video Recording

### parameter

- -p, --path: The path where save the video

### How to stop

ctrl + c

### How to pause

ctrl + z



## 2. Labeling the video frame

### parameter

- -l, --label : The label name
  - It will make a new folder with that name, and save the all the frame image  
- -a, --augumentation : Y/N

### How to use

- Start duration and end duration by key



## 3. Train model

### Parameter

- -m, --model : You could choose which pretrained model to use. You could choose it by considering your computer. Or you could write a path what saved model
- -n, --num : how much layer will be trained
- -s, --save : save path
- -l, --label :  The path where train

## 4. Inference

### Parameter

- -m, --model : Choose model to Inference
- -s, --save : Will you save picture or just json

## 5. Analsis

- shap

## TODO

[] The training parameter record, tensorboard

[] Docker

## Reference

- How to install opencv on window and test
  - https://www.codingforentrepreneurs.com/blog/install-opencv-3-for-python-on-windows/
  - https://www.codingforentrepreneurs.com/blog/opencv-python-web-camera-quick-test/