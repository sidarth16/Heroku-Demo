import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle


import pickle
from pickle import load
from pickle import dump

from tensorflow import keras
import numpy as np
from flask import Flask, request, jsonify, render_template,redirect,flash,send_file

import os
import urllib.request


from flask import Flask , render_template , request , redirect, url_for,flash
from werkzeug.utils import secure_filename
from sudoku_main import sudoku_crop_solve_save


import cv2





app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    int_features = [int(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)

    output = round(prediction[0], 2)

    return render_template('index.html', prediction_text='Employee Salary should be $ {}'.format(output))


if __name__ == "__main__":
    app.run(debug=True)
