from flask import Flask, jsonify, render_template
import pandas as pd
import os
from flask import send_from_directory

import keras
from keras.preprocessing import image
from keras import backend as K

# initialize flask app
app = Flask(__name__)

# Loading a keras model with flask
# https://blog.keras.io/building-a-simple-keras-deep-learning-rest-api.html
def load_model():
    global model
    global graph
    model = keras.models.load_model("mnist_trained.h5")
    graph = K.get_session().graph

def prepare_image(img):
    # Convert the image to a numpy array
    img = image.img_to_array(img)
    # Scale from 0 to 255
    img /= 255
    # Invert the pixels
    img = 1 - img
    # Flatten the image to an array of pixels
    image_array = img.flatten().reshape(-1, 28 * 28)
    # Return the processed feature array
    return image_array



