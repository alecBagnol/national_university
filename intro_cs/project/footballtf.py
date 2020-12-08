import os
import keras

from keras_retinanet import models
from keras_retinanet.utils.image import read_image_bgr, preprocess_image, resize_image
from keras_retinanet.utils.visualization import draw_box, draw_caption
from keras_retinanet.utils.colors import label_color

import matplotlib.pyplot as plt
import cv2
import numpy as np
import time

import tensorflow as tf

def get_session():
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    return tf.Sessions(config=config)

os.environ["CUDA_VISIBLE_DEVICES"] = "1"

keras.backend.tensorflow_backend.set_session(get_session())

def view_annotations(image_path, csv_file):
    filename = os.path.basename(image_path)
    image = read_image_bgr(image_path)
    annotations = [a for a in [i.split(",") for i in open(csv_file).read().split("\n")] if filename in a[0]]
    boxes = np.vstack([i[1:-1] for i in annotations]).astype("i")
    draw = image.copy()
    draw = cv2.cvtColor(draw, cv2.COLOR_BGR2RGB)
    for box in boxes: 
        color = label_color(1)
        b = box.astype(int)
        draw_box(draw, b, color=color)
    plt.figure(figsize=(15, 15))
    plt.axis('off')
    plt.imshow(draw)
    plt.show()

    view_annotations("soccer/images/frame_0033.jpg", "soccer/data.csv")
