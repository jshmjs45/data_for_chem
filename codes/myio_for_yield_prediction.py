# -*- coding: utf-8 -*-

'''
myio_for_yield_prediction.py

This file is used to preprocess data and generate embeddings for our paper
	"When SMILES smiles, yield prediction of organic reaction via deep chemical language processing"
Using python 2.7
Shanghai Jiao Tong University, Mar 30, 2018
'''

from __future__ import print_function
from gensim import models
from gensim.models import Word2Vec
import os, sys, timeit, random, operator, pickle, logging
import numpy as np
import progressbar
import argparse




parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('--mode', dest='mode', type=int, default=0, help='0:CJHIF 1:USPTO')					
parser.add_argument('--folder', dest='folder', type=str, default="/data/CJHIF")
parser.add_argument('--seg', dest='seg', type=str, default='dlg', help='segmentation method: \'dlg\' or \'atom\'') 		
parser.add_argument('--iter', dest='iter', type=int, default=10, help='number of times to run')
parser.add_argument('--size', dest='size', type=int, default=100, help='dimensions in embedding')

args = parser.parse_args()
params = vars(args)
print(params)

folder = params['folder']
mode = params['mode']
seg = params['seg']+'.'
if seg == 'atom': seg = '' # atom-wise

if not os.path.exists(folder):
	print('ERROR: Path '+folder+'dose not exist!')
	exit()


	
train_file = list()
test_file = list()
	
train_l = folder+'/train.'+seg+'l'
train_r = folder+'/train.'+seg+'r'
train_sp =  folder+'/train.'+seg+'steps'
train_file.extend([train_l,train_r,train_sp])

test_l = folder+'/test.dlg.l'
test_r = folder+'/test.dlg.r'
test_sp =  folder+'/test.dlg.steps'
test_file.extend([test_l,test_r,test_sp])

if mode ==0:
	train_mid =  folder+'/train.m'
	test_mid =  folder+'/test.m'
	train_rate = folder+'/train.yield'
	test_rate = folder+'/test.yield'
	train_file.extend([train_mid,train_rate])
	test_file.extend([test_mid,test_rate])

if mode ==1:
	train_mid =  folder+'/train.'+seg+'m'
	test_mid =  folder+'/test.'+seg+'m'
	train_rate1 = fold+'/train.yield1'
	train_rate2 = fold+'/train.yield2'
	test_rate1 = fold+'/test.yield1'
	test_rate2 = fold+'/test.yield2'
	train_file.extend([train_mid,train_rate1,train_rate2])
	test_file.extend([test_mid,test_rate1,test_rate2])



def build_vocab():
	vocabulary_file = open(folder+ "/vocabulary", 'wb')
	vocabulary_reverse_file = open(folder+ "/vocabulary_reverse", 'wb')
	num = 1
	vocab={}
	vocab_re = {}
	vocab_set = set()
	sentences = list()	
	for file in train_file+test_file:
		if not os.path.exists(file):
			print('ERROR: File '+file+'dose not exist!')
			continue
		print('Processing file: ' +file)
		reader = open(file,'r+')
		lines = reader.readlines()
		p = progressbar.ProgressBar()
		p.start(len(lines))
		i = 0
		for line in lines:
			
			line = line.strip()
			i+=1
			p.update(i)
			if mode == 0 and ('train.m' in file or 'test.m' in file):
				sentences += [line.split('\t')]
				items = line.split('\t')
			else:
				items = line.split(' ')
				sentences += [line.split()]
			for word in items:
				if len(word) <= 0:
					continue
				vocab_set.add(word)			
		p.finish()
	print(len(vocab_set))
	
	for word in vocab_set:
		vocab[num] = word
		vocab_re[word] = num
		num += 1
	print(len(vocab))
	pickle.dump(vocab, vocabulary_file)
	vocabulary_file.close()
	pickle.dump(vocab_re, vocabulary_reverse_file)
	vocabulary_reverse_file.close()
	return vocab,vocab_re,sentences

def sentence_process(vocab_re, corpus):
	sentences = list()
	for line in open(corpus):
		line = line.strip('\n')
		if mode == 0 and ('train.m' in corpus or 'test.m' in corpus):
			words = line.split('\t')
		else: words = line.split(' ')
		words_indics = []
		for word in words:
			if len(word) <= 0: continue
			words_indics.append(vocab_re[word])
		sentences.append(words_indics)
	return sentences

def read_rate(corpus):
    sentences = list()
    for line in open(corpus):
		line = line.strip('\r\n')
		sentences.append([float(line)])
    return sentences	

	
def format_data(dataset, vocab_re):
	print (dataset+" set processing")
	reactant = sentence_process(vocab_re,folder+'/'+dataset+'.'+seg+'l')
	product = sentence_process(vocab_re,folder+'/'+dataset+'.'+seg+'r')
	step = sentence_process(vocab_re, folder+'/'+dataset+'.'+seg+'steps')
	if mode ==0:
		condition = sentence_process(vocab_re, folder+'/'+dataset+'.m')
		rate = read_rate(folder+'/'+dataset+'.yield')
	if mode ==1:
		condition = sentence_process(vocab_re, folder+'/'+dataset+'.'+seg+'m')
		rate1 = read_rate(folder+'/'+dataset+'.yield1')
		rate2 = read_rate(folder+'/'+dataset+'.yield2')
		
	if not os.path.exists(os.path.join(folder,dataset)): os.mkdir(os.path.join(folder,dataset))
	if not os.path.exists(os.path.join(folder,dataset)): os.mkdir(os.path.join(folder,dataset))
	
	print ("saving "+dataset+" set")
	reactant_file = open(os.path.join(folder,dataset,'reactant'), 'wb')
	condition_file = open(os.path.join(folder,dataset,'m'), 'wb')
	step_file = open(os.path.join(folder,dataset,'step'), 'wb')
	product_file = open(os.path.join(folder,dataset,'product'), 'wb')
	print('reactant size: ' + str(len(reactant)))
	print('condition size: ' + str(len(condition)))
	print('step size: ' + str(len(step)))
	print('product size: ' + str(len(product)))
	
	pickle.dump(reactant, reactant_file)
	pickle.dump(condition, condition_file)
	pickle.dump(step, step_file)
	pickle.dump(product, product_file)
	
	if mode ==0:
		rate_file = open(os.path.join(folder,dataset,'rate'), 'wb')
		print('rate size: ' + str(len(rate)))
		pickle.dump(rate, rate_file)
	if mode ==1:
		rate_file1 = open(os.path.join(folder,dataset,'rate1'), 'wb')
		rate_file2 = open(os.path.join(folder,dataset,'rate2'), 'wb')
		print('rate1 size: ' + str(len(rate)))
		print('rate2 size: ' + str(len(rate)))
		pickle.dump(rate1, rate_file1)
		pickle.dump(rate2, rate_file2)

def generate_embeddings(vocab,sentences):
	# configure logging
	logger = logging.getLogger(os.path.basename(sys.argv[0]))
	logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
	logging.root.setLevel(level=logging.INFO)
	logger.info('running %s' % ' '.join(sys.argv))

	# run model
	model = Word2Vec(sentences, size=args.size, min_count=5, window=5, sg=1, iter=args.iter)
	weights = model.wv.syn0
	d = dict([(k, v.index) for k, v in model.wv.vocab.items()])
	emb = np.zeros(shape=(len(vocab)+1, args.size), dtype='float32')

	for i, w in vocab.items():
		if w not in d: continue
		emb[i, :] = weights[d[w], :]

	np.save(open(folder +'/word2vec_%d_dim.embeddings' % args.size, 'wb'), emb)
	logger.info('saved to "word2vec_%d_dim.embeddings"' % args.size)
		
print("processing folder "+folder)
vocab,vocab_re,sentences = build_vocab()
print("vocab built")
format_data('train',vocab_re)
format_data('test',vocab_re)
print("corpus built")
generate_embeddings(vocab,sentences)
print("embeddings built")




