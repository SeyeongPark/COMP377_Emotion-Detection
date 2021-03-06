from pyexpat import model
from flask import Flask, request
import os
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.densenet import preprocess_input as preprocess_fun
from tensorflow.keras.models import load_model
from flask_cors import CORS

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './UploadedImages/'
CORS(app)

@app.route("/")
def index():
    return {"Group 2": "Group Project"}

@app.route("/predict", methods= ["POST"])
def predict():
    # Load Image
    try:
        image = request.files['image']
        filePath = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        print('path', filePath)
        image.save(filePath)
        my_image = load_img(filePath, target_size=(IMG_HEIGHT, IMG_WIDTH))
    except:
        return f"Image not found or corrupted", 400

    # Preproces Image
    my_image = img_to_array(my_image)
    my_image = my_image.reshape((1, my_image.shape[0], my_image.shape[1], my_image.shape[2]))
    my_image = preprocess_fun(my_image)
    my_image /= 255

    # Create Prediction using Model
    prediction = model.predict(my_image)
    prediction = np.argmax(prediction , axis = 1 )
    print('prediction', prediction[0])
    return emotions[prediction[0]]

if __name__ == "__main__":
    # Initialize Constants and Model
    emotions = ['Angry', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']
    IMG_HEIGHT = 48
    IMG_WIDTH = 48
    model = load_model('../emotion-detection/emotion_model')
    
    app.run(debug=True)