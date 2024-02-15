#!/usr/bin/env python
import os
from pathlib import Path
from ultralytics import YOLO

while ".git" not in os.listdir(os.getcwd()): os.chdir(Path(os.getcwd())/"..")

# Config
learn_dataset = "svd_vedai_dota"
base_model = 'svd_vedai_dota-best.pt' # yolov8n.pt
batch_size = 8
epochs = 1000

name = f"{learn_dataset}-further"

# Load the base model
model = YOLO(f'./data/model/{base_model}')

# Train the model
model.train(
    data=f'{os.getcwd()}/data/unified/yolo-sets/{learn_dataset}/data.yaml', 
    batch=batch_size, epochs=epochs, imgsz=1280, name=name
)
