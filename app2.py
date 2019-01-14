from flask import Flask, request, jsonify, render_template, send_from_directory
# import imagePrediction
import scrape_news
from flask_pymongo import PyMongo
from pymongo import MongoClient
import keras
from keras.preprocessing import image
from keras import backend as K
import pandas as pd
import os

# initialize flask app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'

model = None
graph = None

def load_model():
    global model
    global graph
    model = keras.models.load_model("mnist_trained.h5")
    graph = K.get_session().graph

load_model()

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
        print(request)

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
            # format of 28x28 pixels
            image_size = (28, 28)
            im = image.load_img(filepath, target_size=image_size,
                                grayscale=True)

            # Convert the 2D image to an array of pixel values
            image_array = prepare_image(im)
            print(image_array)

            # Get the tensorflow default graph and use it to make predictions
            global graph
            with graph.as_default():

                # Use the model to make a prediction
                predicted_digit = model.predict_classes(image_array)[0]
                data["prediction"] = str(predicted_digit)

                # indicate that the request was a success
                data["success"] = True

            return jsonify(data)
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
