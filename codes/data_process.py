#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re,os,sys
import random 
import SplitByElement
import Steps
import argparse
import progressbar

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--folder', dest='folder', type=str, default='USPTO_real1', help='folder of the output files')
parser.add_argument('--data', dest='data', type=str, default='data/data_for_practicality_judgment/USPTO_real1', help='input dataset')

args = parser.parse_args()
params = vars(args)
print(params)
folder = params['folder']
data = params['data']
if not os.path.exists(folder): os.mkdir(folder)

# split the file    
def write_file(folder,fin):
    reader = open(fin, 'r+')
    fout = 'train'
    if 'test' in fin:
        fout = 'test'
        
    writer1 = open(folder+'/'+fout+'.l', 'w')
    writer2 = open(folder+'/'+fout+'.r', 'w')
    writer3 = open(folder+'/'+fout+'.steps', 'w')
    writer4 = open(folder+'/'+fout+'.label', 'w')

    lines = reader.readlines()
    print(len(lines))
    p = progressbar.ProgressBar()
    for i in p(range(len(lines))):  
        line = lines[i].strip()
        strs = line.split("\t");
        reaction = strs[0]
        label = strs[1]
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

    print('over!')

    
#segementation
def segementation(folder, dict='codes/dlg_output_selected'):
    os.system('chmod 777 codes/split')
    os.system('codes/split -fmm '+folder+'/train.l '+dict+' '+folder+'/train.dlg.l')
    os.system('codes/split -fmm '+folder+'/train.r '+dict+' '+folder+'/train.dlg.r')
    os.system('codes/split -fmm '+folder+'/train.steps '+dict+' '+folder+'/train.dlg.steps')

    os.system('codes/split -fmm '+folder+'/test.l '+dict+' '+folder+'/test.dlg.l')
    os.system('codes/split -fmm '+folder+'/test.r '+dict+' '+folder+'/test.dlg.r')
    os.system('codes/split -fmm '+folder+'/test.steps '+dict+' '+folder+'/test.dlg.steps')

    

write_file(folder,data+'_train')
write_file(folder,data+'_test')
segementation(folder)    
