#!/usr/bin/env python
import os
from pathlib import Path
from ultralytics import YOLO

while ".git" not in os.listdir(os.getcwd()): os.chdir(Path(os.getcwd())/"..")

# Config
learn_dataset = "self-svd"
base_model = 'svd_vedai_dota-further-best' # svd-last.pt yolov8n.pt
epochs = 250

name = f"{learn_dataset}-after"

# Load the base model
model = YOLO(f'./data/model/{base_model}.pt')

# Train the model
model.train(
    data=f'{os.getcwd()}/data/unified/yolo-sets/{learn_dataset}/data.yaml', 
    epochs=epochs, imgsz=1280, name=name
)
