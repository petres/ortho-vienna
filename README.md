## Car Detection on Orthophotos of Vienna

> [!CAUTION]  
> Work in progress!

We train YOLO8 models on various datasets to infer cars on orthophotos.

It's still very inaccurate, but have a look:

<https://vienna.abteil.org>

Note that it is trained only on images of areas somewhere in the range of zoom level 19 and 20.
Zoom to some location and select a model.

Thats the output for example of the model `self-svd-after-best` (clicking link `IMG S`):

![with](https://github.com/petres/ortho-vienna/assets/3594062/88c24bdd-d6cd-4d99-9f71-d14c58014395)

Starting annotating some original tiles/img from Vienna could improve the accuracy.

### Trainings Data

Used trainingsdata is listed under [`data`](https://github.com/petres/ortho-vienna/tree/main/data).

Preparation scripts are still under [`scripts/playground/prepareTraining`](https://github.com/petres/ortho-vienna/tree/main/scripts/playground/prepareTraining)

Model weights 

