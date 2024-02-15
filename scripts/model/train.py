#!/usr/bin/env python
import os
from pathlib import Path
from ultralytics import YOLO
import torch

while ".git" not in os.listdir(os.getcwd()): os.chdir(Path(os.getcwd())/"..")

# Config
learn_dataset = "svd_vedai_dota"
base_model = 'yolov8n.pt' # svd_vedai-last.pt yolov8n.pt
batch_size = 4
epochs = 50

name = f"{learn_dataset}"


# Load the base model
model = YOLO(f'./data/model/{base_model}')

# Train the model
model.train(
    data=f'{os.getcwd()}/data/unified/yolo-sets/{learn_dataset}/data.yaml', 
    batch=batch_size, epochs=epochs, imgsz=640, name=name, cache=True
)
