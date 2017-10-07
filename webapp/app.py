import utils
import numpy as np
import io, traceback
import tensorflow as tf

from flask import jsonify
from flask import Flask, request, g
from flask_mako import MakoTemplates, render_template
from plim import preprocessor

from keras.models import load_model

app = Flask(__name__, instance_relative_config=True)

# For Plim templates
mako = MakoTemplates(app)
app.config['MAKO_PREPROCESSOR'] = preprocessor
app.config.from_object('config.DevelopmentConfig')

@app.route('/')
def homepage():
    return render_template('index.html.slim', name='mako')

@app.route('/predict', methods=['POST'])
def predict():
    # Get input text and convert to lower case
    text = request.form.get('text', type=str)
    text = text.lower()

    # Get predictions
    prob, pred = utils.predict(text)
    print("Prediction Probability:", prob)
    print("Prediction Class:", pred)

    if prob is not None:
        return jsonify('{"prob": "%s", "pred": "%s"}' %(prob, pred))
    else:
        return jsonify('{"error": true}')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
