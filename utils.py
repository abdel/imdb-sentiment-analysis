import os
import re
import bcolz
import keras
import itertools
import numpy as np
import _pickle as pickle

from itertools import chain
from matplotlib import pyplot as plt
from keras.utils.data_utils import get_file
from numpy.random import normal

def plot_confusion_matrix(cm, classes, normalize=False, title='Confusion matrix', cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    (This function is copied from the scikit docs.)
    """
    plt.figure()
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    print(cm)
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j], horizontalalignment="center", color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    
def load_array(fname):
    return bcolz.open(fname)[:]

def get_glove_dataset(dataset):
    """Download the requested glove dataset from files.fast.ai
    and return a location that can be passed to load_vectors.
    """
    md5sums = {'6B.50d': '8e1557d1228decbda7db6dfd81cd9909',
               '6B.100d': 'c92dbbeacde2b0384a43014885a60b2c',
               '6B.200d': 'af271b46c04b0b2e41a84d8cd806178d',
               '6B.300d': '30290210376887dcc6d0a5a6374d8255'}
    glove_path = os.path.abspath('data/glove/results')
    return get_file(dataset,
                    'http://files.fast.ai/models/glove/' + dataset + '.tgz',
                    cache_subdir=glove_path,
                    md5_hash=md5sums.get(dataset, None),
                    untar=True)

def load_vectors(loc):
    return (load_array(loc+'.dat'),
        pickle.load(open(loc+'_words.pkl','rb'), encoding='latin1'),
        pickle.load(open(loc+'_idx.pkl','rb'), encoding='latin1'))

def create_embeddings(max_features, vecs, wordidx, idx2word):
    n_fact = vecs.shape[1]
    emb = np.zeros((max_features, n_fact))

    for i in range(1,len(emb)):
        word = idx2word[i]
        if word and re.match(r"^[a-zA-Z0-9\-]*$", word):
            src_idx = wordidx[word]
            emb[i] = vecs[src_idx]
        else:
            # If we can't find the word in glove, randomly initialize
            emb[i] = normal(scale=0.6, size=(n_fact,))

    # This is our "rare word" id - we want to randomly initialize
    emb[-1] = normal(scale=0.6, size=(n_fact,))
    emb/=3
    return emb