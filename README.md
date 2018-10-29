# Smiple Webcam Recognizer

[TOC]

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



