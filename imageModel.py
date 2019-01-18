import os
import io
import numpy as np

import keras
from keras.preprocessing import image
from keras.preprocessing.image import img_to_array
from keras.applications.xception import (
    Xception, preprocess_input, decode_predictions)
from keras import backend as K

from flask import Flask, request, redirect, url_for, jsonify
import h5py
from keras.utils.io_utils import HDF5Matrix
from keras.models import load_model
# import cv2

# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = 'Uploads'

# model = None
# graph = None

label_names = ['apple_pie', 'baby_back_ribs', 'baklava', 'beef_carpaccio', 'beef_tartare', 'beet_salad', 'beignets', 'bibimbap', 'bread_pudding', 'breakfast_burrito', 'bruschetta', 'caesar_salad', 'cannoli', 'caprese_salad', 'carrot_cake', 'ceviche', 'cheese_plate', 'cheesecake', 'chicken_curry', 'chicken_quesadilla', 'chicken_wings', 'chocolate_cake', 'chocolate_mousse', 'churros', 'clam_chowder', 'club_sandwich', 'crab_cakes', 'creme_brulee', 'croque_madame', 'cup_cakes', 'deviled_eggs', 'donuts', 'dumplings', 'edamame', 'eggs_benedict', 'escargots', 'falafel', 'filet_mignon', 'fish_and_chips', 'foie_gras', 'french_fries', 'french_onion_soup', 'french_toast', 'fried_calamari', 'fried_rice', 'frozen_yogurt', 'garlic_bread', 'gnocchi', 'greek_salad', 'grilled_cheese_sandwich', 'grilled_salmon', 'guacamole', 'gyoza', 'hamburger', 'hot_and_sour_soup', 'hot_dog', 'huevos_rancheros', 'hummus', 'ice_cream', 'lasagna', 'lobster_bisque', 'lobster_roll_sandwich', 'macaroni_and_cheese', 'macarons', 'miso_soup', 'mussels', 'nachos', 'omelette', 'onion_rings', 'oysters', 'pad_thai', 'paella', 'pancakes', 'panna_cotta', 'peking_duck', 'pho', 'pizza', 'pork_chop', 'poutine', 'prime_rib', 'pulled_pork_sandwich', 'ramen', 'ravioli', 'red_velvet_cake', 'risotto', 'samosa', 'sashimi', 'scallops', 'seaweed_salad', 'shrimp_and_grits', 'spaghetti_bolognese', 'spaghetti_carbonara', 'spring_rolls', 'steak', 'strawberry_shortcake', 'sushi', 'tacos', 'takoyaki', 'tiramisu', 'tuna_tartare', 'waffles']

def load_model():
    global model
    global graph
    model = keras.models.load_model('food_class_model.h5')
    graph = K.get_session().graph


# load_model()


def prepare_image(img):
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    #img = preprocess_input(img)
    # return the processed image
    images = np.vstack([img])
    return images


### Commenting out the code and inserting the same in app.py
"""
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    data = {"success": False}
    if request.method == 'POST':
        if request.files.get('file'):
            # read the file
            file = request.files['file']

            # read the filename
            filename = file.filename

            # create a path to the uploads folder
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            file.save(filepath)

            # Load the saved image using Keras and resize it to the Xception
            # format of 299x299 pixels
            image_size = (32, 32)
            im = keras.preprocessing.image.load_img(filepath,
                                                    target_size=image_size,
                                                    grayscale=True)

            # preprocess the image and prepare it for classification
            image = prepare_image(im)

            global graph
            with graph.as_default():
                preds = model.predict(image, batch_size=10)
                results = label_names[np.argmax(preds)]
                # print the results
                print(results)

                #data["predictions"] = []

                # loop over the results and add them to the list of
                # returned predictions
                # for (imagenetID, label, prob) in results[0]:
                #     r = {"label": label, "probability": float(prob)}
                #     data["predictions"].append(r)

                # # indicate that the request was a success
                # data["success"] = True

        return jsonify(data)

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

"""
# if __name__ == "__main__":
#     app.run(debug=True)
