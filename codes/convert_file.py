#!/usr/bin/python
# -*- coding: UTF-8 -*-

from __future__ import print_function
from rdkit import Chem

import re,sys
import argparse

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--mode', dest='mode', type=int, default=0, help='0:CJHIF 1:USPTO 2:Chemical.AI')
parser.add_argument('--file', dest='file', type=str, default='data_from_USPTO', help='input file')
args = parser.parse_args()
params = vars(args)
print(params)
mode = params['mode']
file = params['file']

# for USPTO
def atom_mapping_removal(line):
	strinfo = re.compile('\|(\^[0-9]|f):.*\|')
	line = strinfo.sub('',line)
	mol = Chem.MolFromSmiles(line)
	if mol is None: return None
	nmol = Chem.Mol(mol)
	for at in nmol.GetAtoms(): at.SetAtomMapNum(0)
	line = Chem.MolToSmiles(mol,True)
	new_line = Chem.MolToSmiles(nmol,True)
	return new_line
	
			
def convert_file_for_USPTO(fin):
	id = 0
	reader = open(fin, 'r+')
	writer = open(fin+'_converted','w')
	writer.write('reactant>reagent>product'+'\t'+'TextMinedYield'+'\t'+'CalculatedYield'+'\n')
	for line in reader.readlines():
		id += 1
		if id%1000 == 0: print(id)
		line = line.strip()
		strs = line.split('\t');		
		if not len(strs) == 6: continue
		if strs[0] == 'ReactionSmiles': continue
		reaction = strs[0]
		strss = reaction.split('>')
		if not len(strss) == 3: continue
		reactant = atom_mapping_removal(strss[0])
		reagent = atom_mapping_removal(strss[1])
		product = atom_mapping_removal(strss[2])			
		if reactant is None or product is None or reagent is None: continue 
		writer.write(reactant+'>'+reagent+'>'+product+'\t'+strs[4]+'\t'+strs[5]+'\n')
		writer.flush()

	print(id)
	print('over')
	return  

	
def canonicalize_SMILES(line):
	mol = Chem.MolFromSmiles(line)
	if mol is None: return None
	nmol = Chem.Mol(mol)
	for at in nmol.GetAtoms(): at.SetAtomMapNum(0)
	line = Chem.MolToSmiles(mol,True)
	new_line = Chem.MolToSmiles(nmol,True)
	return new_line	

def convert_file_for_CJHIF(fin):
	id = 0
	reader = open(fin, 'r+')
	writer = open(fin+'_converted','w')
	writer.write('reactant>>product'+'\n')
	for line in reader.readlines():
		id += 1
		if id%1000 == 0: print(id)
		line = line.strip()
		strs = line.split('§')	
		if not len(strs) == 7: continue
		reaction = strs[0]
		rate = float(strs[6])
		reagent = strs[3]
		solvent = strs[4]
		catalyst = strs[5]
		
		strss = reaction.split('>>')
		if not len(strss) == 2: continue
		reactant = canonicalize_SMILES(strss[0])
		product = canonicalize_SMILES(strss[1])			
		if reactant is None or product is None: continue
		writer.write(reactant+'>>'+product+'\t'+reagent+'\t'+solvent+'\t'+catalyst+'\t'+str(rate)+'\n')
		writer.flush()

	print(id)
	print('over')
	return  	
	
def convert_file_for_Chemical_AI(fin):
	id = 0
	reader = open(fin, 'r+')
	writer = open(fin+'_converted','w')
	writer.write('reactant>>product'+'\t'+'reagent'+'\t'+'solvent'+'\t'+'catalyst'+'\t'+'yield'+'\n')
	for line in reader.readlines():
		id += 1
		if id%1000 == 0: print(id)
		line = line.strip()
		strs = line.split('>>')
		if not len(strs)==2:continue
		reactant = canonicalize_SMILES(strs[0])
		product = canonicalize_SMILES(strs[1])
		if reactant is None or product is None: continue
		writer.write(reactant+'>>'+product+'\n')
		writer.flush()

	print(id)
	print('over')
	return  
	
if(mode==0): convert_file_for_USPTO(file)	
if(mode==1): convert_file_for_CJHIF(file)
if(mode==2): convert_file_for_Chemical_AI(file)










