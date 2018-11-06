#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
This code is used to combine the positve data and negative data for practicality judgment.
Then split the combined file into train set and test set
'''

import re,os
import random 
import argparse

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--per', dest='per', type=int, default=10, help='ratio of test set (%)')
parser.add_argument('--file1', dest='file1', type=str, default='data_from_USPTO_utf8_converted_clear', help='positive data')
parser.add_argument('--file2', dest='file2', type=str, default='data_from_Chemical.AI_utf8_converted_clear', help='negative data')
args = parser.parse_args()
params = vars(args)
print(params)

test_percent = params['per']
file_pos = params['file1']
file_neg = params['file2']
file_out = file_pos.split('_')[2]+'_'+file_neg.split('_')[2]
print('positive data: '+file_pos)
print('negative data: '+file_neg)
print('output data: '+file_out)


# combine and label the postive data and negative data
# output data format: 'reactant>>product\tlabel'
def combine_data(fin1,fin2,fout):
	lines1 = open(fin1,'r+').readlines()
	lines2 = open(fin2,'r+').readlines()
	writer = open(fout,'w')
	lines = []
	id = 0
	for line in lines1:
		lines.append('\t'.join([re.split('§|\t',line)[0],'1\n']))
		id += 1
		if id%100000==0:print(id)
	print(id)
	id = 0	
	for line in lines2[:-1]:
		lines.append('\t'.join([line.strip('\n\r'),'0\n']))
		id += 1
		if id%100000==0:print(id)
	print(id)
	writer.writelines(lines)
	
# select n% as test set	
def select_file(fin,test_p):
	lines = open(fin,'r+').readlines()
	writer1= open(fin+'_train', 'w')
	writer2= open(fin+'_test', 'w')
	all_num = len(lines)
	test_num = int(all_num*(test_p*0.01))
	
	print('all num: %d' %all_num)
	print('test num: %d' %test_num)
	print('train num: %d' %(all_num-test_num))
	print('slecting...')
	test_set = random.sample(lines, test_num)
	for item in test_set:
		lines.remove(item)
	print('selected')
	
	writer1.writelines(lines)
	writer2.writelines(test_set)	
	
	
combine_data(file_pos,file_neg,file_out)
select_file(file_out, test_percent)
