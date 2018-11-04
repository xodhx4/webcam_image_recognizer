# Smiple Webcam Recognizer

[TOC]

## Pre-requirement

```shell
pip install opencv-python
pip install fire
pip install tensorflow=1.5
pip install keras
pip install pillow
```

Or you could easily build environment using `conda` with `env.yml` file

```노
conda env create -f env.yml
```

After that, activate environment using `activate wb-02`

## Caution

It is only tested on window10



## 1. Video Recording

### parameter

- -p, --path: The path where save the video

### How to stop

Press 'q'

### How to pause

press 's'



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

## 5. Analysis

- shap

## TODO

[] The training parameter record, tensorboard

[] Object Detection

[] Inference result save

[] Analysis

[] Test on other os