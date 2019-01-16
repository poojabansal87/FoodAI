from flask import Flask, request, jsonify, render_template, send_from_directory, redirect, url_for
import numpy as np
# import imagePrediction
import scrape_news
from flask_pymongo import PyMongo
# import imageModel
from pymongo import MongoClient
import keras
from keras.preprocessing import image
from keras.preprocessing.image import img_to_array
from keras.applications.xception import (
    Xception, preprocess_input, decode_predictions)
import h5py
from keras import backend as K
import pandas as pd
import os
import io
import tensorflow as tf
from keras.utils.io_utils import HDF5Matrix
from keras.models import load_model
# import cv2


# initialize flask app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'

model = None
graph = None

label_names = ['apple_pie', 'baby_back_ribs', 'baklava', 'beef_carpaccio', 'beef_tartare', 'beet_salad', 'beignets', 'bibimbap', 'bread_pudding', 'breakfast_burrito', 'bruschetta', 'caesar_salad', 'cannoli', 'caprese_salad', 'carrot_cake', 'ceviche', 'cheese_plate', 'cheesecake', 'chicken_curry', 'chicken_quesadilla', 'chicken_wings', 'chocolate_cake', 'chocolate_mousse', 'churros', 'clam_chowder', 'club_sandwich', 'crab_cakes', 'creme_brulee', 'croque_madame', 'cup_cakes', 'deviled_eggs', 'donuts', 'dumplings', 'edamame', 'eggs_benedict', 'escargots', 'falafel', 'filet_mignon', 'fish_and_chips', 'foie_gras', 'french_fries', 'french_onion_soup', 'french_toast', 'fried_calamari', 'fried_rice', 'frozen_yogurt', 'garlic_bread', 'gnocchi', 'greek_salad', 'grilled_cheese_sandwich', 'grilled_salmon', 'guacamole', 'gyoza', 'hamburger', 'hot_and_sour_soup', 'hot_dog', 'huevos_rancheros', 'hummus', 'ice_cream', 'lasagna', 'lobster_bisque', 'lobster_roll_sandwich', 'macaroni_and_cheese', 'macarons', 'miso_soup', 'mussels', 'nachos', 'omelette', 'onion_rings', 'oysters', 'pad_thai', 'paella', 'pancakes', 'panna_cotta', 'peking_duck', 'pho', 'pizza', 'pork_chop', 'poutine', 'prime_rib', 'pulled_pork_sandwich', 'ramen', 'ravioli', 'red_velvet_cake', 'risotto', 'samosa', 'sashimi', 'scallops', 'seaweed_salad', 'shrimp_and_grits', 'spaghetti_bolognese', 'spaghetti_carbonara', 'spring_rolls', 'steak', 'strawberry_shortcake', 'sushi', 'tacos', 'takoyaki', 'tiramisu', 'tuna_tartare', 'waffles']

def load_model():
    global model
    global graph
    model = keras.models.load_model("my_model.h5")
    graph = K.get_session().graph

load_model()

def prepare_image(img):
    # Convert the image to a numpy array
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    # Scale from 0 to 255
    # img /= 255
    # Invert the pixels
    # img = 1 - img
    # Flatten the image to an array of pixels
    # image_array = img.flatten().reshape(-1, 28 * 28)
    # Return the processed feature array
    images = np.vstack([img])
    return images

# read the data and merge it 

####Possible Code to Use for connecting to MongoDB###
conn = os.environ.get('MONGODB_URI')
if not conn:
    conn = 'mongodb://localhost:27017/'
# client = MongoClient(conn)
# db = client.heart_data
# collection = db.train_values
# listt = []
# for obj in collection.find():
#     obj.pop("_id")
#     listt.append(obj)

# # Use flask_pymongo to set up mongo connection
# app.config["MONGO_URI"] = "mongodb://localhost:27017/allergyNews"
# mongo = PyMongo(app)


##########################################################
# Begin: build out the main page routes
##########################################################
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/remodel')
def analysis():
    return render_template('remodel.html')

@app.route('/inspector')
def predict():
    return render_template('inspector.html')

@app.route('/news')
def data():
    return render_template('news.html', listings = scrape_news.scrape())

##########################################################
# End: build out the main page routes
##########################################################

@app.route('/remodel_code')
def tab_content():      
    return jsonify(listt)

# Jsonify the output of prediction to be used on Inspector Page
@app.route('/predict', methods=['GET', 'POST'])
def predictImage():
    data = {"success": False}
    if request.method == 'POST':
        # print(request)

        if request.files.get('file'):
            # read the file
            file = request.files['file']

            # read the filename
            filename = file.filename

            # create a path to the uploads folder
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            # Save the file to the uploads folder
            file.save(filepath)

            # Load the saved image using Keras and resize it to the mnist
            # format of 32x32 pixels
            image_size = (32, 32)
            im = keras.preprocessing.image.load_img(filepath, 
                                target_size=image_size,
                                grayscale=True)

            # Convert the 2D image to an array of pixel values
            image = prepare_image(im)
            # print(image_array)
            # results = []
            
            # Get the tensorflow default graph and use it to make predictions
            global graph
            with graph.as_default():
                preds = model.predict(image, batch_size=10)
                print(np.argmax(preds))
                results = label_names[np.argmax(preds)]
                # print the results
                print(results)


                # # Use the model to make a prediction
                # predicted_digit = model.predict_classes(image_array)[0]
                # data["prediction"] = str(predicted_digit)

                # # indicate that the request was a success
                # data["success"] = True

            return jsonify(results)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <a href="/inspector">Inspector</a>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)
