import os
dict = 'dlg_dict'
folder = './'


def segementation(folder, dict):
	os.system('~/segment/split -fmm '+folder+'train.l '+dict+' '+folder+'train.dlg.l')
	os.system('~/segment/split -fmm '+folder+'train.r '+dict+' '+folder+'train.dlg.r')
	os.system('~/segment/split -fmm '+folder+'train.steps '+dict+' '+folder+'train.dlg.steps')
	# os.system('~/segment/split -fmm '+folder+'train.reagent '+dict+' '+folder+'train.dlg.m')
	os.system('~/segment/split -fmm '+folder+'test.l '+dict+' '+folder+'test.dlg.l')
	os.system('~/segment/split -fmm '+folder+'test.r '+dict+' '+folder+'test.dlg.r')
	os.system('~/segment/split -fmm '+folder+'test.steps '+dict+' '+folder+'test.dlg.steps')
	# os.system('~/segment/split -fmm '+folder+'test.reagent '+dict+' '+folder+'test.dlg.m')
	os.system('mkdir '+folder+'train')
	os.system('mkdir '+folder+'test')


segementation(folder,dict)