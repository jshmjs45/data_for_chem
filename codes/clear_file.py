#!/usr/bin/python
# -*- coding: UTF-8 -*-


import re,sys
import argparse

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--mode', dest='mode', type=int, default=0, help='0:CJHIF 1:USPTO 2:Chemical.AI')
parser.add_argument('--file', dest='file', type=str, default='data_from_USPTO_utf8_converted')
args = parser.parse_args()
params = vars(args)
print(params)
mode = params['mode']
file = params['file']

def remove_duplicates(lines):
	new_lines = set()
	for line in lines:
		new_lines.add(line)
	return list(new_lines)
	


# for USPTO			
def clear_file_for_USPTO(fin):
	id = 0
	reader = open(fin, 'r+')
	writer = open(fin+'_clear','w')
	writer.write('reactant>reagent>product'+'\t'+'TextMinedYield'+'\t'+'CalculatedYield'+'\n')
	lines = remove_duplicates(reader.readlines()[1:])
	for line in lines:
		line = line.strip()
		strs = line.split('\t');		
		if not len(strs) == 3: continue
		reaction = strs[0]
		try:
			TextMinedYield = float(strs[1].strip('%'))
			CalculatedYield = float(strs[2].strip('%'))
		except ValueError:
			# print(strs[1])
			# print(strs[2])
			continue
		if TextMinedYield<0 or TextMinedYield>100: continue
		if CalculatedYield<0 or CalculatedYield>100: continue
		writer.write(reaction+'\t'+str(TextMinedYield)+'\t'+str(CalculatedYield)+'\n')
		writer.flush()
		id += 1
		if id%10000 == 0: print(id)
	print(id)
	print('over')
	return   	

def clear_file_for_CJHIF(fin):
	id = 0
	reader = open(fin, 'r+')
	writer = open(fin+'_clear','w')
	writer.write('reactant>>product'+'\t'+'reagent'+'\t'+'solvent'+'\t'+'catalyst'+'\t'+'yield'+'\n')
	lines = remove_duplicates(reader.readlines()[1:])
	for line in lines:
		line = line.strip()
		strs = line.split('\t')	
		if not len(strs) == 5: continue
		reaction = strs[0]
		reagent = strs[1]
		solvent = strs[2]
		catalyst = strs[3]
		rate = float(strs[4])
		# print(rate)
		if rate<=0: continue
		writer.write(reaction+'\t'+reagent+'\t'+solvent+'\t'+catalyst+'\t'+str(rate)+'\n')
		writer.flush()
		id += 1
		if id%10000 == 0: print(id)
	print(id)
	print('over')
	return  	
	
def clear_file_for_Chemical_AI(fin):
	id = 0
	reader = open(fin, 'r+')
	writer = open(fin+'_clear','w')
	writer.write('reactant>>product'+'\n')
	lines = remove_duplicates(reader.readlines()[1:])
	for line in lines:
		id += 1
		if id%1000 == 0: print(id)
		writer.write(line)
		writer.flush()

	print(id)
	print('over')
	return  
	
if(mode==0): clear_file_for_USPTO(file)	
if(mode==1): clear_file_for_CJHIF(file)
if(mode==2): clear_file_for_Chemical_AI(file)










