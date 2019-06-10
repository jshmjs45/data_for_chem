#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re,os
import random 
import SplitByElement
import Steps


# 细分文件	data-0808
def write_file(folder,fin):
	reader = open(folder+'/'+fin, 'r+')
	fout = 'test'
	writer1 = open(folder+'/'+fout+'.l', 'w')
	writer2 = open(folder+'/'+fout+'.r', 'w')
	writer3 = open(folder+'/'+fout+'.steps', 'w')
	writer4 = open(folder+'/'+fout+'.label', 'w')
	id = 0
	lines = reader.readlines()
	print(len(lines))
	for line in lines:	
		line = line.strip('\n\r')
		strs = line.split("\t");
		reaction = strs[0]
		label = '1'
		if strs[1]=='0': label = '0'
		strss = reaction.split(">")
		if not len(strss)==3: continue
		line_l = SplitByElement.split_line(strss[0]);
		line_r = SplitByElement.split_line(strss[2]);
		if line_l=='':continue
		if line_r=='':continue
		trans = Steps.trans_line(line_r,line_l);
			
		writer1.write(line_l+"\n");
		writer2.write(line_r+"\n");
		writer3.write(trans+"\n");
		writer4.write(label+'\n');


		writer1.flush()
		writer2.flush()
		writer3.flush()
		writer4.flush()

		id += 1
		if id%1000 == 0: print(id)
		
	print(id)
	print('write over!')

	
#切分
def segementation(folder, dict='~/segment/dlg_output_selected'):
	os.system('~/segment/split -fmm '+folder+'train.l '+dict+' '+folder+'train.dlg.l')
	os.system('~/segment/split -fmm '+folder+'train.r '+dict+' '+folder+'train.dlg.r')
	os.system('~/segment/split -fmm '+folder+'train.steps '+dict+' '+folder+'train.dlg.steps')
	# os.system('~/segment/split -fmm '+folder+'train.reagent '+dict+' '+folder+'train.dlg.reagent')
	os.system('~/segment/split -fmm '+folder+'test.l '+dict+' '+folder+'test.dlg.l')
	os.system('~/segment/split -fmm '+folder+'test.r '+dict+' '+folder+'test.dlg.r')
	os.system('~/segment/split -fmm '+folder+'test.steps '+dict+' '+folder+'test.dlg.steps')
	# os.system('~/segment/split -fmm '+folder+'test.reagent '+dict+' '+folder+'test.dlg.reagent')
	os.system('mkdir '+folder+'train')
	os.system('mkdir '+folder+'test')
	
folder = 'data-25w/'
file = 'data-0808'
write_file(folder,file)
segementation(folder)	
