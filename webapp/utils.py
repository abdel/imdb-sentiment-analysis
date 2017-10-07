import nltk
import numpy as np
import tensorflow as tf

from nltk.corpus import stopwords
from keras.models import load_model
from keras.preprocessing import sequence, text

# Download NLTK stopwords
nltk.download('stopwords')

# Params
maxlen = 400
max_features = 5000

# Load model
print("Loading model")
model = load_model('./model/cnn_model.h5', compile=False)
graph = tf.get_default_graph()

def preprocess(data):
    # Prepare the stopwords
    stopwords_nltk = set(stopwords.words('english'))
    relevant_words = set(['not', 'nor', 'no', 'wasn', 'ain', 'aren', 'very',
                          'only', 'but', 'don', 'isn', 'weren'])
    stopwords_filtered = list(stopwords_nltk.difference(relevant_words))

    # Remove the stop words from input text
    data = ' '.join([word for word in data.split() if word not in stopwords_filtered])

    # One-hot the input text
    data = text.one_hot(data, max_features)
    data = np.array(data)

    # Pad the sequences
    data = sequence.pad_sequences([data], maxlen=maxlen)

    return data

def predict(text):
    text = preprocess(text)

    with graph.as_default():
        pred_prob = model.predict(text)[0][0]
        pred_class = model.predict_classes(text)[0][0]

    return pred_prob, pred_class
