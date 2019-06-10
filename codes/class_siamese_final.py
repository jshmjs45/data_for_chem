from __future__ import print_function

import os
import sys
import random
from time import strftime, gmtime, time
import pickle
from keras.layers import Embedding, LSTM, Dense, GRU, Bidirectional, Dropout, Input, Lambda, concatenate
from keras.models import Sequential, Model
from keras.metrics import mae
from keras.optimizers import RMSprop, SGD

random.seed(233)
import numpy as np
import argparse
import logging
from datetime import datetime
from keras import backend as K
from keras.layers.core import Dense, Dropout, Activation

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--maxlen', dest='maxlen', type=int, default=100)
parser.add_argument('--layer', dest='layer', type=str, default="biLSTM")
parser.add_argument('--rateid', dest='rateid', type=int, default=0)
parser.add_argument('--dim', dest='dim', type=int, default=64)
parser.add_argument('--epochs', dest='epochs', type=int, default=50)
parser.add_argument('--mode', dest='mode', type=int, default=0)
parser.add_argument('--folder', dest='folder', type=str, default="USPTO-real1")
parser.add_argument('--data', dest='data', type=str, default="USPTO-real1")

args = parser.parse_args()
params = vars(args)
print(params)
path = params['data']
mode = params['mode']
rate_id = params['rateid']
maxlength = params['maxlen']
layer = params['layer']
dim = params['dim']
epochs = params['epochs']
folder = params['folder']

if not os.path.exists('logs/'):  os.makedirs('logs/')
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=datetime.now().strftime('logs/'+folder + '_%H_%M_%d_%m_%Y.log'),
                    filemode='w')

logging.info(str(params))

def log(x):
    print(x)


def load(path, name):
    print("path:", os.path.join(path, name))
    return pickle.load(open(os.path.join(path, name), 'rb'))


def padq(data):
    return pad(data, maxlength)


def pada(data):
    return pad(data, maxlength)


def pad(data, len=None):
    from keras.preprocessing.sequence import pad_sequences
    return pad_sequences(data, maxlen=len, padding='post', truncating='post', value=0)


def get_time():
    return strftime('%Y-%m-%d %H:%M:%S', gmtime())


def output(predictions):
    out = []
    predictions = predictions.tolist()
    for i, d in enumerate(predictions):
        if d[0] > 1:
            out.append(0)
        else:
            out.append(1 - d[0])
    return out


vocab = load(path, 'vocabulary')
vocab_size = len(vocab) + 1


def save_epoch(epoch):
    foldername = "mse/" + str(rate_id)
    if folder != "":
        foldername += "/" + folder
    if not os.path.exists('models/' + foldername):
        os.makedirs('models/' + foldername)
    model.save_weights('models/' + foldername + '/weights_epoch_%d.h5' % epoch, overwrite=True)


def process(dataset):
    reactants = load(dataset, 'question')
    products = load(dataset, 'answer')
    steps = load(dataset, 'step')
    labels = load(dataset, 'label')
    new_reactants = []
    new_products = []
    new_steps = []
    new_labels = []
    pos_reactants = []
    pos_products = []
    pos_steps = []
    pos_labels = []
    neg_reactants = []
    neg_products = []
    neg_steps = []
    neg_labels = []

    new_reactants = reactants
    new_products = products
    new_steps = steps
    new_labels = labels
    
    print("reactants:" + str(len(reactants)))
    print("products:" + str(len(products)))
    print("steps:" + str(len(steps)))
    print("labels:" + str(len(labels)))

    logging.info("reactants:" + str(len(reactants)))
    logging.info("products:" + str(len(products)))
    logging.info("steps:" + str(len(steps)))
    logging.info("labels:" + str(len(labels)))

    reactants = padq(reactants)
    products = pada(products)
    steps = pada(new_steps)
    y = pad(new_labels, len=1)

    pos = np.sum(y == 1, axis=0)
    neg = np.sum(y == 0, axis=0)
    print("pos:" + str(pos))
    print("neg:" + str(neg))
    logging.info("pos:" + str(pos))
    logging.info("neg:" + str(neg))

    if mode == 0:
        r = np.concatenate((reactants, steps), axis=1)
        p = np.concatenate((products, steps), axis=1)
        print("r/p + step")
    else:
        r = reactants
        p = products
        print("r/p")
    print("cocat:" + str(len(r)))
    return r, p, y


r, p, y = process(path + "/train/")
tr, tp, ty = process(path + "/test/")

print('Build model...')
input_dim = r.shape[1]


def create_base_network(input_dim):
    '''Base network to be shared (eq. to feature extraction).
    '''
    print('Build model...')

    model = Sequential()
    embedding = Embedding(input_dim=vocab_size,
                          output_dim=128,
                          mask_zero=True)
    model.add(embedding)
    model.add(LSTM(256))
    model.add(Dropout(0.3))
    model.add(Dense(1))
    model.add(Activation('sigmoid'))
    return model


base_network = create_base_network(input_dim)
input_a = Input(shape=(input_dim,))
input_b = Input(shape=(input_dim,))

processed_a = base_network(input_a)
processed_b = base_network(input_b)

joint = concatenate([processed_a, processed_b], axis=1)
joint_den = Dense(256, init='normal', activation='relu')(joint)
distance = Dense(1, init='normal', activation='sigmoid')(joint_den)

model = Model([input_a, input_b], distance)



def compute_accuracy(predictions, labels, threshod):
    '''Compute classification accuracy with a fixed threshold on distances.
    '''
    TP, TN, predict_true, predict_false = 0., 0., 0., 0.
    actual = np.sum(labels == 1, axis=0)
    for i, d in enumerate(predictions):
        if d >= threshod:
            predict_true += 1
            if labels[i] == 1:
                TP += 1
        else:
            predict_false += 1
            if labels[i] == 0:
                TN += 1

    precision = TP / float(predict_true)
    acc =  (TP+TN) / float(len(labels))
    recall = TP / float(actual)
    fscore = (2 * precision * recall) / float(precision + recall)
    return precision, recall, fscore, acc


def compute_accuracy_neg(predictions, labels, threshold):
    '''Compute classification accuracy with a fixed threshold on distances.
    '''
    right, predict = 0, 0
    actual = np.sum(labels == 0, axis=0)
    for i, d in enumerate(predictions):
        if d < threshold:
            predict += 1
            if labels[i] == 0:
                right += 1
    print("neg evaluation")
    print("all: " + str(len(labels)))
    print("actual: " + str(actual[0]))
    print("predict: " + str(predict))
    print("right: " + str(right))
    if not predict == 0:
        precision = right / float(predict)
    else:
        precision = 0
    if not actual == 0:
        recall = right / float(actual)
    else:
        recall = 0
    if predict == 0 or actual == 0:
        fscore = 0
    else:
        fscore = (2 * precision * recall) / float(precision + recall)
    return precision, recall, fscore

rms = RMSprop()
model.compile(loss='binary_crossentropy', optimizer=rms, metrics=['accuracy'])
val_loss = {'loss': 1., 'epoch': 0}
for i in range(1, epochs):
        log('%s -- Epoch %d ' % (get_time(), i))
        logging.info('%s -- Epoch %d ' % (get_time(), i))
        hist = model.fit([r, p], y, batch_size=512, shuffle=True, epochs=1)
        pred = model.predict([tr, tp], batch_size=512)
        te_acc, te_rr, te_f, acc = compute_accuracy(pred, ty, 0.5)
        n_acc, n_rr, n_f = compute_accuracy_neg(pred, ty, 0.5)
        print('* accuracy on test set: %0.2f%%' % (100 * acc))
        logging.info('* accuracy on test set: %0.2f%%' % (100 * acc))
        print('* precision on test set: %0.2f%%' % (100 * te_acc))
        logging.info('* acc on test set: %0.2f%%' % (100 * te_acc))
        print('* recall on test set: %0.2f%%' % (100 * te_rr))
        logging.info('* recall on test set: %0.2f%%' % (100 * te_rr))
        print('* Fscore on test set: %0.2f%%' % (100 * te_f))
        logging.info('* Fscore on test set: %0.2f%%' % (100 * te_f))
        print('* neg precision: %0.2f%%' % (100 * n_acc))
        logging.info('* Fscore on neg test set: %0.2f%%' % (100 * n_acc))
        print('* neg recall: %0.2f%%' % (100 * n_rr))
        logging.info('* recall on neg test set: %0.2f%%' % (100 * n_rr))
        print('* neg Fscore: %0.2f%%' % (100 * n_f))
        logging.info('* Fscore on neg test set: %0.2f%%' % (100 * n_f))
        save_epoch(i)