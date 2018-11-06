#!/usr/bin/env python

"""
Command-line script for generating embeddings
Useful if you want to generate larger embeddings for some models
"""

from __future__ import print_function
from gensim import models
import numpy as np

import os
import sys
import random
import pickle
import argparse
import logging

random.seed(42)
# parse arguments
parser = argparse.ArgumentParser(description='Generate embeddings for the InsuranceQA dataset')
parser.add_argument('--iter', metavar='N', type=int, default=10, help='number of times to run')
parser.add_argument('--size', metavar='D', type=int, default=100, help='dimensions in embedding')
parser.add_argument('--ID', metavar='ID', type=str, default="1117", help='fold name')
parser.add_argument('--path', metavar='P', type=str, default="", help='path')
args = parser.parse_args()


fold = args.ID

data_path = args.path

if not os.path.exists(data_path):
		print('ERROR: Path '+data_path+'dose not exist!')
		exit()


def load(path, name):
    return pickle.load(open(os.path.join(data_path, name), 'rb'))


def revert(vocab, indices):
    return [vocab.get(i, 'X') for i in indices]



# configure logging
logger = logging.getLogger(os.path.basename(sys.argv[0]))
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
logging.root.setLevel(level=logging.INFO)
logger.info('running %s' % ' '.join(sys.argv))

# imports go down here because they are time-consuming
from gensim.models import Word2Vec
# from models import *

vocab = load(data_path,'vocabulary')

files = os.listdir(data_path)
sentences= []

corpus_l = data_path+'/train.dlg.l'
corpus_r = data_path+'/train.dlg.r'
corpus_sp =  data_path+'/train.dlg.steps'
# corpus_id =  data_path+'/train.reagent'
corpus_rate = data_path+'/train.label'

test_l = data_path+'/test.dlg.l'
test_r = data_path+'/test.dlg.r'
test_sp =  data_path+'/test.dlg.steps'
# test_id =  data_path+'/test.reagent'
test_rate = data_path+'/test.label'

for file in [corpus_l, corpus_r, test_l, test_r, corpus_sp, test_sp, corpus_rate, test_rate]:
	if not os.path.exists(file):
		print('ERROR: File '+file+'dose not exist!')
		exit()


for file in [corpus_l, corpus_r, test_l, test_r, corpus_sp, test_sp, corpus_rate, test_rate]:
    for line in open(file):
        sentences += [line.split()]

# run model
model = Word2Vec(sentences, size=args.size, min_count=5, window=5, sg=1, iter=args.iter)
weights = model.wv.syn0
d = dict([(k, v.index) for k, v in model.wv.vocab.items()])
emb = np.zeros(shape=(len(vocab)+1, args.size), dtype='float32')

for i, w in vocab.items():
    if w not in d: continue
    emb[i, :] = weights[d[w], :]

np.save(open(data_path +'/word2vec_%d_dim.embeddings' % args.size, 'wb'), emb)
logger.info('saved to "word2vec_%d_dim.embeddings"' % args.size)

