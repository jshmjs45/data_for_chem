# -*- coding: utf-8 -*-
import os, sys, timeit, random, operator
import numpy as np
import random
import pickle
import progressbar


folder = ''
if len(sys.argv)>1: folder = sys.argv[1]
if not os.path.exists(folder):
		print('ERROR: Path '+folder+'dose not exist!')
		exit()

corpus_l = folder+'/train.dlg.l'
corpus_r = folder+'/train.dlg.r'
corpus_sp =  folder+'/train.dlg.steps'
# corpus_id =  folder+'/train.reagent'
corpus_rate = folder+'/train.label'

test_l = folder+'/test.dlg.l'
test_r = folder+'/test.dlg.r'
test_sp =  folder+'/test.dlg.steps'
# test_id =  folder+'/test.reagent'
test_rate = folder+'/test.label'

if not os.path.exists(folder+'/train'): os.mkdir(folder+'/train')
if not os.path.exists(folder+'/test'): os.mkdir(folder+'/test')
for file in [corpus_l, corpus_r, test_l, test_r, corpus_sp, test_sp, corpus_rate, test_rate]:
	if not os.path.exists(file):
		print('ERROR: File '+file+'dose not exist!')
		exit()

def build_vocab():
	vocabulary_file = open(folder+ "/vocabulary", 'wb')
	vocabulary_reverse_file = open(folder+ "/vocabulary_reverse", 'wb')
	num = 1
	vocab={}
	vocab_re = {}
	vocab_set = set()
	for file in [corpus_l, corpus_r, test_l, test_r, corpus_sp, test_sp, corpus_rate, test_rate]:
		print('Processing file: ' +file)
		# if not os.path.exists(file): continue
		reader = open(file,'r+')
		lines = reader.readlines()
		p = progressbar.ProgressBar()
		p.start(len(lines))
		i = 0
		for line in lines:
			i+=1
			p.update(i)
			items = line.split(' ')
			for word in items:
				if len(word) <= 0:
					continue
				vocab_set.add(word)
				# if not word in vocab_set:
					# vocab[num] = word
					# vocab_re[word] = num
					# num += 1
			
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
	return vocab,vocab_re

def sentence_process(vocab_re, corpus):
    sentences = list()
    for line in open(corpus):
        words = line.split(' ')
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

def getCorpus(vocab_re):
	print ("training set processing")
	question = sentence_process(vocab_re,corpus_r)
	# id = sentence_process(vocab_re, corpus_id)
	step = sentence_process(vocab_re, corpus_sp)
	answer = sentence_process(vocab_re,corpus_l)
	rate = read_rate(corpus_rate)

	print ("saving training set")
	question_file = open(folder + "/train/question", 'wb')
	# id_file = open(folder + "/train/id", 'wb')
	step_file = open(folder + "/train/step", 'wb')
	answer_file = open(folder + "/train/answer", 'wb')
	rate_file = open(folder + "/train/label", 'wb')

	pickle.dump(question, question_file)
	# pickle.dump(id, id_file)
	pickle.dump(step, step_file)
	pickle.dump(answer, answer_file)
	pickle.dump(rate, rate_file)

	print('question'+str(len(question)))
	print('step'+str(len(step)))
	print('answer'+str(len(answer)))
	print('rate'+str(len(rate)))

	print ("test set processing")
	question = sentence_process(vocab_re, test_r)
	# id = sentence_process(vocab_re, test_id)
	step = sentence_process(vocab_re, test_sp)
	answer = sentence_process(vocab_re, test_l)
	rate = read_rate(test_rate)

	print ("saving training set")
	question_file = open(folder + "/test/question", 'wb')
	# id_file = open(folder + "/test/id", 'wb')
	step_file = open(folder + "/test/step", 'wb')
	answer_file = open(folder + "/test/answer", 'wb')
	rate_file = open(folder + "/test/label", 'wb')

	pickle.dump(question, question_file)
	# pickle.dump(id, id_file)
	pickle.dump(step, step_file)
	pickle.dump(answer, answer_file)
	pickle.dump(rate, rate_file)

	print('question'+str(len(question)))
	print('step'+str(len(step)))
	print('answer'+str(len(answer)))
	print('rate'+str(len(rate)))


print ("processing fold " + folder)
vocab,vocab_re = build_vocab()
print ("vocab built")
getCorpus(vocab_re)
print ("corpus built")




