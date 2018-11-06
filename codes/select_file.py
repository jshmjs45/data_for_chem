#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re,os,sys
import random
import argparse 

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--per', dest='per', type=int, default=10, help='ratio of test set (%)')
parser.add_argument('--file', dest='file', type=str, default='data_from_USPTO_utf8_converted_clear', help='input file')
args = parser.parse_args()
params = vars(args)
print(params)
file = params['file']
test_percent = params['per']

# select n% as test set	
def select_file(fin,test_p):
	lines = open(fin,'r+').readlines()[1:] #remove the first title line and the last blank line
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
	
select_file(file, test_percent)